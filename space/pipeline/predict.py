"""
Orkestrator pipeline penilaian kerusakan lahan pertanian (Tujuan 3):

  PRE            -> [1] Deteksi Mask R-CNN        -> poligon (pred_id)
  PRE + POST     -> [2] Ekstraksi 6 layer fitur   -> f_*_cont per pred_id
                 -> [3] Klasifikasi Random Forest -> damage_pred per pred_id
                 -> [4] Luas per kelas (ha)
                 -> [5] Overlay di atas citra POST
"""
import time
import traceback

import cv2
import numpy as np

from pipeline.area import DEFAULT_RESOLUSI_M, add_area_columns, area_table
from pipeline.classify import FEATURE_COLS_MODEL, classify_polygons
from pipeline.detect import detect_polygons
from pipeline.features import compute_features
from pipeline.visualize import render_overlay

MAX_SIDE_PX = 2048   # batas sisi citra (Mask R-CNN + SAM di CPU sangat berat untuk citra besar)

# Beda ukuran pre vs post yang masih ditoleransi (post di-resize ke ukuran pre).
# Sengaja kecil: menyamakan ukuran TIDAK meluruskan isi citra, sedangkan semua
# layer fitur mengasumsikan piksel (x,y) pre & post menunjuk lokasi yang sama.
TOLERANSI_UKURAN = 0.05

TAHAP = [
    "1. Deteksi lahan (Mask R-CNN)",
    "2. Ekstraksi 6 layer fitur",
    "3. Klasifikasi kerusakan (Random Forest)",
    "4. Perhitungan luas",
    "5. Visualisasi overlay",
]


class PipelineError(Exception):
    """Error yang pesannya aman ditampilkan langsung ke pengguna."""


def _to_rgb(img, nama):
    if img is None:
        raise PipelineError(f"Citra {nama} belum diunggah.")
    arr = np.asarray(img)
    if arr.ndim == 2:
        arr = np.stack([arr] * 3, axis=-1)
    if arr.ndim != 3 or arr.shape[2] < 3:
        raise PipelineError(f"Citra {nama} harus berupa citra RGB (bentuk array: {arr.shape}).")
    return arr[:, :, :3]


def validate_inputs(img_pre, img_post, resolusi, toleransi=TOLERANSI_UKURAN):
    """Kembalikan (pre, post, resolusi, peringatan). Beda ukuran <= toleransi
    diperbaiki dengan me-resize citra post ke ukuran citra pre."""
    pre = _to_rgb(img_pre, "pre-disaster")
    post = _to_rgb(img_post, "post-disaster")
    peringatan = []

    if pre.shape[:2] != post.shape[:2]:
        h_pre, w_pre = pre.shape[:2]
        h_post, w_post = post.shape[:2]
        selisih = max(abs(h_pre - h_post) / max(h_pre, h_post),
                      abs(w_pre - w_post) / max(w_pre, w_post))
        if selisih > toleransi:
            raise PipelineError(
                f"Ukuran citra pre ({w_pre}x{h_pre} px) dan post ({w_post}x{h_post} px) "
                f"berbeda {selisih * 100:.1f}% — melebihi batas {toleransi * 100:.0f}%. "
                f"Fitur perubahan dihitung per piksel pada lokasi yang sama, jadi kedua "
                f"citra harus meliput area yang sama.")
        interp = cv2.INTER_AREA if (w_post > w_pre) else cv2.INTER_LINEAR
        post = cv2.resize(post, (w_pre, h_pre), interpolation=interp)
        peringatan.append(
            f"Ukuran citra post ({w_post}x{h_post} px) disamakan ke ukuran citra pre "
            f"({w_pre}x{h_pre} px); beda {selisih * 100:.1f}%. Penyamaan ini hanya mengubah "
            f"ukuran, BUKAN meluruskan isi citra — bila kedua citra tidak persis area & "
            f"zoom yang sama, nilai fitur perubahan (dan kelas kerusakan) bisa keliru.")

    if max(pre.shape[:2]) > MAX_SIDE_PX:
        raise PipelineError(
            f"Citra terlalu besar ({pre.shape[1]}x{pre.shape[0]} px). Sisi maksimum "
            f"{MAX_SIDE_PX} px; potong citra menjadi tile yang lebih kecil.")
    if resolusi is None or not np.isfinite(resolusi) or resolusi <= 0:
        raise PipelineError(f"Resolusi harus angka > 0 m/piksel (diberikan: {resolusi}).")
    return pre, post, float(resolusi), peringatan


def run_pipeline(img_pre, img_post, resolusi=DEFAULT_RESOLUSI_M, return_gdf=False):
    """Jalankan tahap 1-5.

    Returns:
        (overlay_rgb | None, tabel_luas | None, log) — ditambah gdf_pred
        (poligon + fitur + damage_pred + luas) kalau return_gdf=True.
        log = {"status", "waktu_detik": {tahap: detik}, "n_poligon", "ukuran", "error"}
    """
    log = {"status": "gagal", "waktu_detik": {}, "n_poligon": None,
           "ukuran": None, "error": None, "peringatan": []}
    overlay, tabel, gdf = None, None, None
    t_total = time.time()
    tahap_aktif = "Validasi input"
    try:
        pre, post, resolusi, peringatan = validate_inputs(img_pre, img_post, resolusi)
        log["peringatan"].extend(peringatan)
        log["ukuran"] = f"{pre.shape[1]}x{pre.shape[0]} px"

        tahap_aktif = TAHAP[0]
        t = time.time()
        gdf = detect_polygons(pre)
        log["waktu_detik"][tahap_aktif] = time.time() - t
        log["n_poligon"] = len(gdf)

        if len(gdf) > 0:
            tahap_aktif = TAHAP[1]
            t = time.time()
            df_feat = compute_features(gdf, pre, post)
            log["waktu_detik"][tahap_aktif] = time.time() - t

            tahap_aktif = TAHAP[2]
            t = time.time()
            df_feat = classify_polygons(df_feat)
            gdf = gdf.merge(df_feat[["polygon_id", "damage_pred"] + FEATURE_COLS_MODEL],
                            on="polygon_id", how="left")
            log["waktu_detik"][tahap_aktif] = time.time() - t
        else:
            gdf["damage_pred"] = []

        tahap_aktif = TAHAP[3]
        t = time.time()
        gdf = add_area_columns(gdf, resolusi)
        tabel = area_table(gdf, resolusi)
        log["waktu_detik"][tahap_aktif] = time.time() - t

        tahap_aktif = TAHAP[4]
        t = time.time()
        overlay = render_overlay(post, gdf)
        log["waktu_detik"][tahap_aktif] = time.time() - t

        log["status"] = "sukses"
    except PipelineError as e:
        log["error"] = f"[{tahap_aktif}] {e}"
    except Exception as e:
        log["error"] = f"[{tahap_aktif}] {type(e).__name__}: {e}"
        traceback.print_exc()
    log["waktu_detik"]["Total"] = time.time() - t_total

    if return_gdf:
        return overlay, tabel, log, gdf
    return overlay, tabel, log


def format_log(log):
    """Log ringkas (teks) untuk ditampilkan di UI."""
    lines = [f"Status      : {log['status'].upper()}"]
    if log.get("ukuran"):
        lines.append(f"Ukuran citra: {log['ukuran']}")
    if log.get("n_poligon") is not None:
        lines.append(f"Segmen lahan terdeteksi: {log['n_poligon']}")
        if log["n_poligon"] == 0:
            lines.append("  (tidak ada lahan pertanian terdeteksi -> tahap 2-3 dilewati)")
    lines.append("Waktu proses:")
    for tahap, detik in log["waktu_detik"].items():
        lines.append(f"  {tahap:<42s} {detik:8.1f} s")
    for p in log.get("peringatan", []):
        lines.append(f"PERINGATAN: {p}")
    if log.get("error"):
        lines.append(f"ERROR: {log['error']}")
    return "\n".join(lines)
