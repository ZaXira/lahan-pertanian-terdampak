"""
Validasi regresi (Fase 6): pipeline aplikasi web vs hasil resmi Tujuan 3
(tujuan3_bundle.zip -> poligon_prediksi_4tile.gpkg).

Untuk tiap tile uji:
  1. Jalur TIF  : array float32 dari GeoTIFF Kaggle (EPSG:32751) -> run_pipeline()
                  -> harus (nyaris) identik dengan bundle.
  2. Jalur PNG  : (opsional, --png) tile dikonversi ke PNG uint8 seperti yang
                  diunggah pengguna -> run_pipeline() -> ukur efek kuantisasi 8-bit.

Yang dibandingkan per tile: jumlah poligon, geometri (IoU, pasangan Hungarian),
6 fitur f_*_cont, damage_pred, dan luas per kelas.

Contoh:
  python tests/test_regresi.py                                  # lokal, default path
  python tests/test_regresi.py --gambar-dir /kaggle/input/.../Gambar \
      --bundle-gpkg /kaggle/input/.../poligon_prediksi_4tile.gpkg --png --out /kaggle/working/regresi
"""
import argparse
import glob
import json
import os
import sys
import time

import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from PIL import Image
from scipy.optimize import linear_sum_assignment
from shapely.affinity import affine_transform

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from pipeline.classify import FEATURE_COLS_MODEL, LABELS_ORD  # noqa: E402
from pipeline.predict import format_log, run_pipeline  # noqa: E402

TEST_TILES = ["00000163", "00000169", "00000184", "00000195"]
IOU_MATCH = 0.5


def find_tile(gambar_dir, tile_id, fase):
    hits = glob.glob(os.path.join(gambar_dir, "**", f"*{tile_id}_{fase}_disaster.tif"), recursive=True)
    if not hits:
        raise FileNotFoundError(f"Tidak ada *{tile_id}_{fase}_disaster.tif di {gambar_dir}")
    return hits[0]


def read_tif_rgb(path):
    with rasterio.open(path) as src:
        return np.transpose(src.read([1, 2, 3]), (1, 2, 0)), src.transform, float(src.res[0])


PNG_MODES = ("minmax", "perband", "perband_minmax")


def to_png_uint8(arr, out_path, mode="minmax"):
    """Simulasi citra yang diunggah pengguna: skalakan ke 0-255 uint8, simpan PNG, baca ulang.

    mode:
      minmax          — min-max GABUNGAN 3 band (skala relatif antar band terjaga)
      perband         — percentile 2-98 PER BAND (seperti stretch default QGIS)
      perband_minmax  — min-max PER BAND
    """
    a = arr.astype(np.float32)
    if mode == "minmax":
        out = (a - a.min()) / max(float(a.max() - a.min()), 1e-12)
    elif mode in ("perband", "perband_minmax"):
        out = np.zeros_like(a)
        for c in range(a.shape[2]):
            band = a[..., c]
            lo, hi = (np.percentile(band, [2, 98]) if mode == "perband"
                      else (float(band.min()), float(band.max())))
            out[..., c] = np.clip((band - lo) / max(float(hi - lo), 1e-12), 0, 1)
    else:
        raise ValueError(f"mode PNG tidak dikenal: {mode}")
    Image.fromarray(np.round(out * 255).astype(np.uint8)).save(out_path)
    return np.asarray(Image.open(out_path).convert("RGB"))


def load_bundle_tile(gpkg, tile_id, transform):
    ref = gpd.read_file(gpkg)
    ref = ref[ref["tile_id"].astype(str).str.zfill(8) == tile_id].reset_index(drop=True)
    inv = ~transform   # tif Kaggle & bundle sama-sama EPSG:32751 -> langsung ke piksel
    ref["geometry"] = [affine_transform(g, [inv.a, inv.b, inv.d, inv.e, inv.xoff, inv.yoff])
                       for g in ref.geometry]
    return ref


def hungarian_match(pred_geoms, ref_geoms):
    n, m = len(pred_geoms), len(ref_geoms)
    iou = np.zeros((n, m), dtype=np.float64)
    for i, g in enumerate(pred_geoms):
        for j, r in enumerate(ref_geoms):
            if g.intersects(r):
                u = g.union(r).area
                iou[i, j] = g.intersection(r).area / u if u > 0 else 0.0
    if n == 0 or m == 0:
        return [], iou
    ri, ci = linear_sum_assignment(-iou)
    return [(i, j, iou[i, j]) for i, j in zip(ri, ci) if iou[i, j] >= IOU_MATCH], iou


def compare(gdf, ref, resolusi):
    pairs, _ = hungarian_match(list(gdf.geometry), list(ref.geometry))
    li = [p[0] for p in pairs]
    rj = [p[1] for p in pairs]
    ious = np.array([p[2] for p in pairs]) if pairs else np.array([])

    res = {
        "n_lokal": int(len(gdf)), "n_bundle": int(len(ref)), "n_pasangan_iou50": len(pairs),
        "n_iou_ge_0999": int((ious >= 0.999).sum()), "mean_iou_pasangan": float(ious.mean()) if len(ious) else 0.0,
    }
    # urutan pred_id sama -> cek kesamaan geometri per indeks (bukti deterministik terkuat)
    if len(gdf) == len(ref):
        res["geometri_identik_per_indeks"] = int(sum(
            g.equals_exact(r, tolerance=1e-6) for g, r in zip(gdf.geometry, ref.geometry)))

    if pairs:
        dp_l = gdf["damage_pred"].to_numpy()[li]
        dp_r = ref["damage_pred"].to_numpy()[rj]
        res["damage_pred_sama"] = int((dp_l == dp_r).sum())
        res["damage_pred_sama_pct"] = float((dp_l == dp_r).mean() * 100)
        res["fitur"] = {}
        for c in FEATURE_COLS_MODEL:
            d = np.abs(gdf[c].to_numpy(dtype=float)[li] - ref[c].to_numpy(dtype=float)[rj])
            res["fitur"][c] = {"max_beda": float(d.max()), "mean_beda": float(d.mean()),
                               "identik": int((d < 1e-6).sum())}

    # luas per kelas: pipeline (piksel*res^2) vs bundle (geometri resmi, dihitung dgn rumus sama)
    luas_ref = (ref.geometry.area * resolusi ** 2 / 10000).groupby(ref["damage_pred"]).sum()
    luas_lok = (gdf.geometry.area * resolusi ** 2 / 10000).groupby(gdf["damage_pred"]).sum()
    res["luas_ha"] = {k: {"lokal": round(float(luas_lok.get(k, 0)), 4),
                          "bundle": round(float(luas_ref.get(k, 0)), 4)} for k in LABELS_ORD}
    res["jumlah_per_kelas"] = {k: {"lokal": int((gdf["damage_pred"] == k).sum()),
                                   "bundle": int((ref["damage_pred"] == k).sum())} for k in LABELS_ORD}
    return res


def run_one(tile_id, pre, post, resolusi, ref, out_dir, label):
    t = time.time()
    overlay, tabel, log, gdf = run_pipeline(pre, post, resolusi, return_gdf=True)
    print(format_log(log))
    if log["status"] != "sukses":
        return {"status": "gagal", "error": log["error"]}
    Image.fromarray(overlay).save(os.path.join(out_dir, f"overlay_{tile_id}_{label}.png"))
    tabel.to_csv(os.path.join(out_dir, f"tabel_luas_{tile_id}_{label}.csv"), index=False)
    gdf.drop(columns=["geometry"]).to_csv(os.path.join(out_dir, f"prediksi_{tile_id}_{label}.csv"), index=False)
    hasil = compare(gdf, ref, resolusi)
    hasil["status"] = "sukses"
    hasil["waktu_detik"] = {k: round(v, 1) for k, v in log["waktu_detik"].items()}
    hasil["waktu_total_detik"] = round(time.time() - t, 1)
    print(tabel.to_string(index=False))
    return hasil


def ringkas(semua):
    rows = []
    for (tile, label), h in semua.items():
        if h.get("status") != "sukses":
            rows.append({"tile": tile, "jalur": label, "status": "GAGAL"})
            continue
        rows.append({
            "tile": tile, "jalur": label,
            "n_lokal/bundle": f"{h['n_lokal']}/{h['n_bundle']}",
            "pasangan_IoU>=0.5": h["n_pasangan_iou50"],
            "IoU>=0.999": h["n_iou_ge_0999"],
            "damage_pred_sama_%": round(h.get("damage_pred_sama_pct", 0), 2),
            "max_beda_fitur": round(max(v["max_beda"] for v in h["fitur"].values()), 3) if "fitur" in h else None,
            "waktu_s": h["waktu_total_detik"],
        })
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gambar-dir", default=os.path.join(ROOT, "tests", "gambar"))
    ap.add_argument("--bundle-gpkg", default=os.path.join(ROOT, "tests", "_bundle", "Tujuan 3",
                                                          "poligon_prediksi_4tile.gpkg"))
    ap.add_argument("--tiles", nargs="+", default=TEST_TILES)
    ap.add_argument("--png", action="store_true", help="uji jalur PNG uint8 (mode minmax)")
    ap.add_argument("--png-modes", nargs="+", choices=PNG_MODES, default=None,
                    help=f"mode konversi 8-bit yang diuji (pilihan: {', '.join(PNG_MODES)})")
    ap.add_argument("--skip-tif", action="store_true", help="lewati jalur TIF (hemat waktu)")
    ap.add_argument("--out", default=os.path.join(ROOT, "tests", "_out", "regresi"))
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    png_modes = args.png_modes if args.png_modes else (["minmax"] if args.png else [])

    semua = {}
    for tile_id in args.tiles:
        print(f"\n{'=' * 70}\nTILE {tile_id}\n{'=' * 70}")
        pre, transform, resolusi = read_tif_rgb(find_tile(args.gambar_dir, tile_id, "pre"))
        post, _, _ = read_tif_rgb(find_tile(args.gambar_dir, tile_id, "post"))
        ref = load_bundle_tile(args.bundle_gpkg, tile_id, transform)
        print(f"ukuran={pre.shape} dtype={pre.dtype} resolusi={resolusi:.4f} m | poligon bundle={len(ref)}")

        if not args.skip_tif:
            print("\n--- Jalur TIF (float32) ---")
            semua[(tile_id, "tif")] = run_one(tile_id, pre, post, resolusi, ref, args.out, "tif")
        for mode in png_modes:
            print(f"\n--- Jalur PNG uint8, konversi '{mode}' (simulasi upload) ---")
            pre8 = to_png_uint8(pre, os.path.join(args.out, f"{tile_id}_pre_{mode}.png"), mode)
            post8 = to_png_uint8(post, os.path.join(args.out, f"{tile_id}_post_{mode}.png"), mode)
            label = "png" if mode == "minmax" else f"png_{mode}"
            semua[(tile_id, label)] = run_one(tile_id, pre8, post8, resolusi, ref, args.out, label)

    tabel = ringkas(semua)
    print(f"\n{'=' * 70}\nRINGKASAN REGRESI\n{'=' * 70}")
    print(tabel.to_string(index=False))
    tabel.to_csv(os.path.join(args.out, "ringkasan_regresi.csv"), index=False)
    with open(os.path.join(args.out, "hasil_regresi.json"), "w", encoding="utf-8") as f:
        json.dump({f"{t}_{j}": h for (t, j), h in semua.items()}, f, indent=2, ensure_ascii=False)
    print(f"\nDetail: {os.path.join(args.out, 'hasil_regresi.json')}")


if __name__ == "__main__":
    main()
