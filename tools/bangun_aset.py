# -*- coding: utf-8 -*-
"""
Menyiapkan aset situs dari SUMBER RESMI penelitian (satu sumber angka):
  - tabel Bab IV yang sudah diverifikasi (work/tabel/*.csv + .meta.json)
  - angka grafik dari data/ (keluaran Kaggle)
  - citra pre/post + overlay 4 tile uji dari artefak/kaggle/hasil_regresi.zip (jalur GeoTIFF = identik hasil resmi)
Keluaran: web/assets/data/data.js, web/assets/img/tile_*.jpg|webp
  python -X utf8 artefak_fix/tools/bangun_aset.py
"""
import csv
import io
import json
import zipfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]          # folder "Bab 4"
WEB = ROOT / "artefak_fix" / "web"
IMG = WEB / "assets" / "img"
TAB = ROOT / "work" / "tabel"
DATA = ROOT / "data"
TILES = ["00000163", "00000169", "00000184", "00000195"]


def tabel(kode):
    meta = json.loads((TAB / f"{kode}.meta.json").read_text(encoding="utf-8"))
    rows = list(csv.reader(io.StringIO((TAB / f"{kode}.csv").read_text(encoding="utf-8"))))[1:]
    return {"judul": meta["judul"], "kepala": meta["kepala"], "rows": rows,
            "keterangan": meta.get("keterangan", ""), "tebal": meta.get("baris_tebal", []),
            "panel": meta.get("baris_panel", [])}


def csv_dict(path):
    return list(csv.DictReader(io.StringIO(Path(path).read_text(encoding="utf-8"))))


out = {"tabel": {k: tabel(k) for k in (
    "T4.1.a", "T4.1.b", "T4.1.c", "T4.2.a", "T4.2.b", "T4.2.c", "T4.2.d", "T4.2.e", "T4.3.b", "T4.3.c2",
    "T4.3.d", "T4.3.f", "T4.3.g", "T4.3.i", "T4.3.j", "T4.3.k", "T4.4.a", "T4.4.b", "T4.4.c", "T4.4.d",
    "T4.4.e", "T4.5.b", "T4.5.c")}}

# ---- grafik
mc = {r[""]: r for r in csv_dict(DATA / "tujuan1" / "model_comparison_table.csv")}
kol = ["instance_precision", "instance_recall", "instance_f1", "instance_iou", "pixel_precision", "pixel_recall",
       "pixel_f1", "pixel_iou"]
out["t1"] = {"label": ["Precision instans", "Recall instans", "F1 instans", "IoU instans", "Precision piksel",
                       "Recall piksel", "F1 piksel", "IoU piksel"],
             "yolo": [round(float(mc["YOLOv8-seg"][k]), 4) for k in kol],
             "mrcnn": [round(float(mc["Mask R-CNN"][k]), 4) for k in kol]}
log = json.loads((DATA / "tujuan2" / "training_log.json").read_text(encoding="utf-8"))
uji = {r["model"]: r for r in log["results"] if r["split"] == "test"}
met = ["accuracy", "f1_macro", "precision_macro", "recall_macro", "kappa_quadratic"]
out["t2"] = {"label": ["Akurasi", "F1-macro", "Precision-macro", "Recall-macro", "Kappa kuadratik"],
             "rf": [round(uji["Random Forest"][k], 4) for k in met],
             "lgbm": [round(uji["LightGBM"][k], 4) for k in met]}
fi = csv_dict(DATA / "tujuan2" / "feature_importance.csv")
nama = {"Batas Lahan": "Batas lahan", "Material Asing": "Material asing", "Kehilangan Tanaman": "Kehilangan tanaman",
        "Radiometri": "Perubahan radiometri", "Genangan": "Genangan baru", "SAC": "Perubahan semantik (SAC)"}
out["fi"] = {"label": [nama[r["Fitur"]] for r in fi], "gini": [float(r["RF_Gini"]) for r in fi],
             "perm": [float(r["RF_Perm_Mean"]) for r in fi], "perm_sd": [float(r["RF_Perm_Std"]) for r in fi]}
s3 = json.loads((DATA / "tujuan3" / "summary_tujuan3.json").read_text(encoding="utf-8"))
out["t3"] = {"deteksi": s3["deteksi"], "f1_kelas": s3["klasifikasi_matched_only"]["f1_per_kelas"],
             "macro_f1": s3["klasifikasi_matched_only"]["macro_f1"],
             "hm": s3["klasifikasi_matched_only"]["damage_f1_harmonic"], "xview2": s3["skor_gabungan_xview2"]["nilai"],
             "miou": s3["mIoU"], "oracle_selisih": s3["kontribusi_error_geometri_deteksi"]["selisih_macro_f1_oracle_vs_matched"],
             "per_tile": csv_dict(DATA / "tujuan3" / "test_results_per_tile.csv")}
dist = list(csv.reader(io.StringIO((ROOT / "work" / "bab123" / "bab3" / "tabel" / "T3.6.csv").read_text(encoding="utf-8"))))
out["distribusi"] = {r[0]: r[1] for r in dist[1:4]}

# ---- galeri 4 tile (jalur GeoTIFF artefak, identik hasil resmi)
z = zipfile.ZipFile(ROOT / "artefak" / "kaggle" / "hasil_regresi.zip")


def simpan(nama_zip, dasar, lebar=1400, rasio=None):
    im = Image.open(io.BytesIO(z.read(nama_zip)))
    if im.mode != "RGB":
        latar = Image.new("RGB", im.size, "white")
        latar.paste(im, mask=im.convert("RGBA").split()[-1])
        im = latar
    if rasio:  # potong strip legenda di bawah agar sebangun dengan citra pre/post
        im = im.crop((0, 0, im.width, round(im.width * rasio)))
    if im.width > lebar:
        im = im.resize((lebar, round(im.height * lebar / im.width)), Image.LANCZOS)
    im.save(IMG / f"{dasar}.webp", "WEBP", quality=84, method=6)
    im.save(IMG / f"{dasar}.jpg", "JPEG", quality=84, optimize=True, progressive=True)
    return im.size


galeri = []
per_tile = {r["tile_id"].zfill(8): r for r in out["t3"]["per_tile"]}
for t in TILES:
    ukuran = simpan(f"{t}_pre.png", f"tile_{t}_pre", 1024)
    simpan(f"{t}_post.png", f"tile_{t}_post", 1024)
    simpan(f"overlay_{t}_tif.png", f"tile_{t}_overlay", 1400)
    simpan(f"overlay_{t}_tif.png", f"tile_{t}_overlay_crop", 1024, rasio=ukuran[1] / ukuran[0])
    luas = list(csv.DictReader(io.StringIO(z.read(f"tabel_luas_{t}_tif.csv").decode("utf-8"))))
    galeri.append({"tile": t, "ukuran_pre": ukuran, "luas": luas, "resmi": per_tile[t]})
out["galeri"] = galeri

(WEB / "assets" / "data").mkdir(parents=True, exist_ok=True)
(WEB / "assets" / "data" / "data.js").write_text(
    "/* Dibangkitkan otomatis oleh tools/bangun_aset.py dari data resmi penelitian — jangan disunting manual. */\n"
    "window.DATA = " + json.dumps(out, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
print("data.js:", len(out["tabel"]), "tabel;", "gambar:", len(list(IMG.glob("tile_*"))), "berkas")
