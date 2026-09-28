"""
Tahap 2 — Ekstraksi 6 layer fitur per poligon (pre vs post).

Fungsi di bawah garis "SALINAN VERBATIM" disalin baris-per-baris dari
reference/Tujuan 3 code.txt (CELL 3-10, identik dgn Tujuan 2 part 1) oleh
skrip, TANPA perubahan logika. Yang ditambahkan di file ini hanya:
  - SAM_CHECKPOINT_PATH (env var) & konstanta SAC final
  - normalize_rgb_percentile(): versi array dari load_raster_rgb (citra upload
    tidak punya file GeoTIFF)
  - compute_features(): wrapper ruang piksel (transform = Affine.identity())

Preprocessing tahap ini: percentile 2-98 PER BAND (beda dgn tahap deteksi).
"""
import os

import numpy as np
import pandas as pd
import rasterio
import cv2
from affine import Affine
from rasterio.features import geometry_mask

from pipeline.model_paths import PROJECT_ROOT, SAM_FILE, resolve  # noqa: F401

# Parameter SAC/AnyChange final (Tujuan 2) — jangan diubah
SAC_PARAMS_FINETUNED = {
    "points_per_side"            : 64,
    "stability_score_thresh"     : 0.7,
    "change_confidence_threshold": 145,
    "use_normalized_feature"     : True,
    "bitemporal_match"           : False,
}
SAC_BIN_THR_BEST = 2

PIXEL_TRANSFORM = Affine.identity()


# ================================================================
# SALINAN VERBATIM dari reference/Tujuan 3 code.txt
# ================================================================
# ---- CELL 3 — utilitas (normalize_*, load_raster_rgb, get_poly_mask) (baris 110-158) ----
def normalize_for_display(img):
    """Normalisasi array ke [0,1]."""
    img = img.astype(np.float32)
    mn, mx = img.min(), img.max()
    if mx == mn:
        return np.zeros_like(img)
    return (img - mn) / (mx - mn)


def normalize_to_uint8(img):
    """Normalisasi array ke uint8 [0,255]."""
    return (normalize_for_display(img) * 255).astype(np.uint8)


def normalize_01(arr):
    return normalize_for_display(arr)


def load_raster_rgb(path, clip_percentiles=(2, 98)):
    """
    Load citra GeoTIFF sebagai numpy HxWx3 float32 ternormalisasi [0,1].

    Returns:
        img_hwc, meta, transform, crs, raster_shape
    """
    with rasterio.open(path) as src:
        arr          = src.read()[:3].astype(np.float32)
        meta         = src.meta.copy()
        transform    = src.transform
        crs          = src.crs
        raster_shape = (src.height, src.width)

    img_hwc = np.transpose(arr, (1, 2, 0))
    lo, hi  = clip_percentiles
    out     = np.zeros_like(img_hwc, dtype=np.float32)

    for c in range(3):
        band         = img_hwc[..., c]
        p_lo, p_hi   = np.percentile(band[~np.isnan(band)], [lo, hi])
        band_clipped = np.clip(band, p_lo, p_hi)
        out[..., c]  = (band_clipped - p_lo) / (p_hi - p_lo + 1e-6)

    return out, meta, transform, crs, raster_shape


def get_poly_mask(geom, raster_shape, transform):
    """Boolean mask numpy dari satu geometri polygon."""
    return geometry_mask([geom], out_shape=raster_shape,
                          transform=transform, invert=True)

# ---- CELL 3 — nama kelas final & classify_pct (baris 161-187) ----
# ── Nama kelas FINAL (WAJIB dipakai konsisten di seluruh project) ──
LABELS_ORD = ["Tidak Terdampak", "Terdampak Sedang", "Terdampak Berat"]
ORDINAL_MAP = {
    "Tidak Terdampak" : 1,
    "Terdampak Sedang": 2,
    "Terdampak Berat" : 3,
}


def classify_pct(pct, low=10, high=50):
    """
    Klasifikasi persentase kontinu -> label ordinal 3 kelas FINAL.

    NOTE: nilai *_pct kontinu tetap dipertahankan sebagai fitur UTAMA
    model (lihat extract_all_features, skema hybrid) — klasifikasi ini
    hanya menghasilkan versi ordinal untuk keperluan pelaporan Bab IV.

    Returns:
        score (int) : 1=Tidak Terdampak, 2=Terdampak Sedang, 3=Terdampak Berat
        kelas (str) : nama kelas final
    """
    if pct < low:
        return 1, "Tidak Terdampak"
    elif pct < high:
        return 2, "Terdampak Sedang"
    else:
        return 3, "Terdampak Berat"

# ---- CELL 4-9 — extract_layer1..6 + maskdata_to_score (baris 205-753) ----
# ============================================================
# CELL 4 — Layer 1: Kehilangan Batas Lahan (Canny Edge)
# ============================================================

def extract_layer1_batas(gdf, img_pre, img_post, raster_transform, raster_shape,
                          return_raw_mask=False):
    """
    Kehilangan batas lahan per polygon via Canny edge detection.

    Args:
        return_raw_mask: jika True, langsung return array boolean tile-penuh
            (edge yang hilang dari pre->post, TANPA dibatasi buffer polygon)
            untuk keperluan visualisasi/QC — skip loop per-polygon.

    Returns:
        pd.DataFrame: polygon_id, batas_loss_pct, batas_score, kelas_batas_pred
        ATAU np.ndarray (H,W) bool jika return_raw_mask=True
    """
    def _canny_edge(img_float):
        img_u8 = normalize_to_uint8(img_float)
        gray   = cv2.cvtColor(img_u8, cv2.COLOR_RGB2GRAY)
        blur   = cv2.GaussianBlur(gray, (3, 3), 0)
        return cv2.Canny(blur, 50, 150)

    edges_pre  = _canny_edge(img_pre)
    edges_post = _canny_edge(img_post)

    if return_raw_mask:
        # Edge hilang dari pre->post, tile-penuh (TIDAK dibatasi buffer
        # polygon seperti perhitungan per-polygon di bawah — pendekatan
        # kasar untuk gambaran umum, khusus visualisasi).
        return (edges_pre > 0) & (edges_post == 0)

    empty_df = pd.DataFrame(columns=["polygon_id", "batas_loss_pct",
                                      "batas_score", "kelas_batas_pred"])
    if len(gdf) == 0:
        return empty_df

    kernel        = np.ones((3, 3), np.uint8)
    buffer_kernel = np.ones((7, 7), np.uint8)
    hasil         = []

    for _, row in gdf.iterrows():
        poly_mask = get_poly_mask(row.geometry, raster_shape, raster_transform)

        poly_u8      = poly_mask.astype(np.uint8)
        bagian_dalam = cv2.erode(poly_u8, kernel, iterations=2)
        batas_poly   = poly_u8 - bagian_dalam
        batas_buffer = cv2.dilate(batas_poly, buffer_kernel, iterations=1)

        edge_pre_di_batas  = (edges_pre  > 0) & (batas_buffer > 0)
        edge_post_di_batas = (edges_post > 0) & (batas_buffer > 0)
        jumlah_edge_pre    = int(edge_pre_di_batas.sum())

        if jumlah_edge_pre == 0:
            batas_loss_pct = 0.0
        else:
            edge_masih_ada = int((edge_pre_di_batas & edge_post_di_batas).sum())
            batas_loss_pct = (1 - edge_masih_ada / jumlah_edge_pre) * 100

        score, kelas = classify_pct(batas_loss_pct, low=10, high=50)

        hasil.append({
            "polygon_id"      : int(row["polygon_id"]),
            "batas_loss_pct"  : round(batas_loss_pct, 2),
            "batas_score"     : score,
            "kelas_batas_pred": kelas,
        })

    return pd.DataFrame(hasil)


# ============================================================
# CELL 5 — Layer 2: Material Asing (CVA + HSV Color Filter)
# ============================================================

def extract_layer2_material(gdf, img_post, raster_transform, raster_shape,
                             img_pre=None, return_raw_mask=False):
    """
    Deteksi material asing (lumpur/abu) per polygon via CVA + filter HSV.

    Args:
        return_raw_mask: jika True, return array boolean tile-penuh
            material_mask untuk visualisasi/QC — skip loop per-polygon.

    Returns:
        pd.DataFrame: polygon_id, material_pct, material_score, kelas_material_pred
        ATAU np.ndarray (H,W) bool jika return_raw_mask=True
    """
    if img_pre is not None:
        diff        = normalize_01(img_post) - normalize_01(img_pre)
        cva_mag     = np.sqrt(np.sum(diff ** 2, axis=2))
        cva_u8      = (normalize_01(cva_mag) * 255).astype(np.uint8)
        _, change_mask = cv2.threshold(cva_u8, 0, 1,
                                        cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    else:
        change_mask = np.ones(raster_shape, dtype=np.uint8)

    img_post_u8 = normalize_to_uint8(img_post)
    hsv         = cv2.cvtColor(img_post_u8, cv2.COLOR_RGB2HSV)
    mask_mud    = cv2.inRange(hsv, np.array([5,   20,  60]),
                                    np.array([40, 170, 220]))
    mask_gray   = cv2.inRange(hsv, np.array([0,   0,  80]),
                                    np.array([180, 50, 210]))

    material_color = ((mask_mud > 0) | (mask_gray > 0)).astype(np.uint8)
    material_mask  = material_color & change_mask.astype(np.uint8)

    kernel        = np.ones((3, 3), np.uint8)
    material_mask = cv2.morphologyEx(material_mask, cv2.MORPH_OPEN,  kernel)
    material_mask = cv2.morphologyEx(material_mask, cv2.MORPH_CLOSE, kernel)

    if return_raw_mask:
        return material_mask.astype(bool)

    empty_df = pd.DataFrame(columns=["polygon_id", "material_pct",
                                      "material_score", "kelas_material_pred"])
    if len(gdf) == 0:
        return empty_df

    hasil = []
    for _, row in gdf.iterrows():
        poly_mask    = get_poly_mask(row.geometry, raster_shape, raster_transform)
        luas_polygon = int(poly_mask.sum())

        if luas_polygon == 0:
            material_pct = 0.0
        else:
            material_di_poly = int(((material_mask > 0) & poly_mask).sum())
            material_pct     = (material_di_poly / luas_polygon) * 100

        score, kelas = classify_pct(material_pct, low=10, high=50)

        hasil.append({
            "polygon_id"         : int(row["polygon_id"]),
            "material_pct"       : round(material_pct, 2),
            "material_score"     : score,
            "kelas_material_pred": kelas,
        })

    return pd.DataFrame(hasil)


# ============================================================
# CELL 6 — Layer 3: Kehilangan Tanaman (Excess Green Index)
# ============================================================

def extract_layer3_tanaman(gdf, img_pre, img_post, raster_transform, raster_shape,
                            exg_thr=0.05, return_raw_mask=False):
    """
    Kehilangan vegetasi per polygon menggunakan Excess Green (ExG) index.
    ExG = 2g - r - b. Vegetasi hilang = ada vegetasi di pre, tidak di post.

    Args:
        return_raw_mask: jika True, return array boolean tile-penuh vegetasi
            yang hilang (pre punya, post tidak) untuk visualisasi/QC.

    Returns:
        pd.DataFrame: polygon_id, tanaman_loss_pct, tanaman_score, kelas_tanaman_pred
        ATAU np.ndarray (H,W) bool jika return_raw_mask=True
    """
    def _exg(img_hwc):
        img   = img_hwc.astype(np.float32)
        total = img.sum(axis=2) + 1e-6
        r = img[:, :, 0] / total
        g = img[:, :, 1] / total
        b = img[:, :, 2] / total
        return (2 * g) - r - b

    def _veg_mask(exg):
        mask   = (exg > exg_thr).astype(np.uint8)
        kernel = np.ones((3, 3), np.uint8)
        return cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    veg_pre  = _veg_mask(_exg(img_pre))
    veg_post = _veg_mask(_exg(img_post))

    if return_raw_mask:
        return (veg_pre > 0) & (veg_post == 0)

    empty_df = pd.DataFrame(columns=["polygon_id", "tanaman_loss_pct",
                                      "tanaman_score", "kelas_tanaman_pred"])
    if len(gdf) == 0:
        return empty_df

    hasil = []

    for _, row in gdf.iterrows():
        poly_mask = get_poly_mask(row.geometry, raster_shape, raster_transform)
        pre_in    = int((veg_pre  & poly_mask).sum())
        post_in   = int((veg_post & poly_mask).sum())

        if pre_in == 0:
            tanaman_loss_pct = 0.0
        else:
            loss             = max(0, pre_in - post_in)
            tanaman_loss_pct = (loss / pre_in) * 100

        score, kelas = classify_pct(tanaman_loss_pct, low=10, high=50)

        hasil.append({
            "polygon_id"        : int(row["polygon_id"]),
            "tanaman_loss_pct"  : round(tanaman_loss_pct, 2),
            "tanaman_score"     : score,
            "kelas_tanaman_pred": kelas,
        })

    return pd.DataFrame(hasil)


# ============================================================
# CELL 7 — Layer 4: Perubahan Radiometri (CVA Magnitude + Otsu)
# ============================================================

def extract_layer4_radiometri(gdf, img_pre, img_post, raster_transform, raster_shape,
                               return_raw_mask=False):
    """
    Persentase pixel dengan perubahan radiometri signifikan per polygon
    via Change Vector Analysis (CVA) + Otsu thresholding.

    Args:
        return_raw_mask: jika True, return array boolean tile-penuh radio_mask
            untuk visualisasi/QC.

    Returns:
        pd.DataFrame: polygon_id, radiometri_pct, radiometri_score, kelas_radiometri_pred
        ATAU np.ndarray (H,W) bool jika return_raw_mask=True
    """
    diff     = img_post.astype(np.float32) - img_pre.astype(np.float32)
    cva_mag  = np.sqrt(np.sum(diff ** 2, axis=2))
    cva_u8   = (normalize_01(cva_mag) * 255).astype(np.uint8)

    _, change_mask = cv2.threshold(cva_u8, 0, 255,
                                    cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    radio_mask = (change_mask > 0).astype(np.uint8)

    if return_raw_mask:
        return radio_mask.astype(bool)

    empty_df = pd.DataFrame(columns=["polygon_id", "radiometri_pct",
                                      "radiometri_score", "kelas_radiometri_pred"])
    if len(gdf) == 0:
        return empty_df

    hasil = []
    for _, row in gdf.iterrows():
        poly_mask = get_poly_mask(row.geometry, raster_shape, raster_transform)
        luas      = int(poly_mask.sum())

        if luas == 0:
            radiometri_pct = 0.0
        else:
            berubah        = int((radio_mask & poly_mask).sum())
            radiometri_pct = (berubah / luas) * 100

        score, kelas = classify_pct(radiometri_pct, low=10, high=50)

        hasil.append({
            "polygon_id"           : int(row["polygon_id"]),
            "radiometri_pct"       : round(radiometri_pct, 2),
            "radiometri_score"     : score,
            "kelas_radiometri_pred": kelas,
        })

    return pd.DataFrame(hasil)


# ============================================================
# CELL 8 — Layer 5: Genangan Air Baru (Water Index RGB)
# ============================================================

def extract_layer5_genangan(gdf, img_pre, img_post, raster_transform, raster_shape,
                             water_thr=0.1, return_raw_mask=False):
    """
    Genangan air baru per polygon menggunakan Water Index RGB.
    WI = (B-R)/(B+R+eps). Genangan baru = air di post tapi bukan di pre.

    Args:
        return_raw_mask: jika True, return array boolean tile-penuh flood_new
            untuk visualisasi/QC.

    Returns:
        pd.DataFrame: polygon_id, genangan_pct, genangan_score, kelas_genangan_pred
        ATAU np.ndarray (H,W) bool jika return_raw_mask=True
    """
    def _wi(img_hwc):
        img = img_hwc.astype(np.float32)
        R   = img[:, :, 0]
        B   = img[:, :, 2]
        return (B - R) / (B + R + 1e-6)

    def _water_mask(wi):
        mask   = (wi > water_thr).astype(np.uint8)
        kernel = np.ones((5, 5), np.uint8)
        mask   = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  kernel)
        mask   = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        return mask

    water_pre  = _water_mask(_wi(img_pre))
    water_post = _water_mask(_wi(img_post))
    flood_new  = ((water_post > 0) & (water_pre == 0)).astype(np.uint8)

    if return_raw_mask:
        return flood_new.astype(bool)

    empty_df = pd.DataFrame(columns=["polygon_id", "genangan_pct",
                                      "genangan_score", "kelas_genangan_pred"])
    if len(gdf) == 0:
        return empty_df

    hasil = []
    for _, row in gdf.iterrows():
        poly_mask = get_poly_mask(row.geometry, raster_shape, raster_transform)
        luas      = int(poly_mask.sum())

        if luas == 0:
            genangan_pct = 0.0
        else:
            genang       = int((flood_new & poly_mask).sum())
            genangan_pct = (genang / luas) * 100

        score, kelas = classify_pct(genangan_pct, low=10, high=50)

        hasil.append({
            "polygon_id"         : int(row["polygon_id"]),
            "genangan_pct"       : round(genangan_pct, 2),
            "genangan_score"     : score,
            "kelas_genangan_pred": kelas,
        })

    return pd.DataFrame(hasil)


# ============================================================
# CELL 9 — Layer 6: SAC/AnyChange (SAM-based Change Detection)
# Hyperparameter & bin_thr hasil finetuning skala 1-tile (lihat catatan
# di CELL 2). Ini bagian PALING LAMBAT dari seluruh pipeline.
# ============================================================

def maskdata_to_score(md, H, W):
    """
    Konversi MaskData AnyChange menjadi score map (H, W) uint16 — tiap piksel
    = jumlah mask "berubah" yang menutupinya. Berdasarkan struktur ASLI yang
    dikonfirmasi dari dir(changemasks): key tersedia adalah 'rles' (mask
    terkompresi RLE), BUKAN 'masks'/'mask' mentah — jadi jalur RLE ini yang
    dipakai, bukan tebakan multi-key seperti versi sebelumnya.
    """
    score = np.zeros((H, W), dtype=np.uint16)

    def _as_np(x):
        return x.detach().cpu().numpy() if hasattr(x, "detach") else np.asarray(x)

    try:
        d = dict(md.items())
    except Exception as e:
        print(f"  ⚠ [SAC] Gagal memanggil md.items(): {e}")
        return score

    rles = d.get("rles", None)
    n_mask = len(rles) if rles is not None else 0
    print(f"  [SAC] MaskData keys: {list(d.keys())} | jumlah mask (rles): {n_mask}")

    # Diagnostik paling penting: skala change_confidence vs threshold yang dipakai.
    if "change_confidence" in d and d["change_confidence"] is not None:
        cc = _as_np(d["change_confidence"])
        if cc.size > 0:
            print(f"  [SAC] change_confidence -> min={cc.min():.3f}, "
                  f"max={cc.max():.3f}, mean={cc.mean():.3f}, n={cc.size}")
        else:
            print("  [SAC] change_confidence KOSONG (0 mask lolos filter "
                  "internal AnyChange dengan change_confidence_threshold saat ini).")

    if not rles:
        print("  ⚠ [SAC] Tidak ada RLE mask sama sekali -- kemungkinan besar "
              "change_confidence_threshold terlalu tinggi untuk skala skor "
              "yang dihasilkan (lihat baris change_confidence di atas), "
              "sehingga SEMUA kandidat mask sudah difilter habis SEBELUM "
              "sampai ke tahap ini.")
        return score

    try:
        from pycocotools import mask as maskUtils
        _HAS_PYCOCO = True
    except ImportError as e:
        print(f"  ⚠ [SAC] pycocotools tidak tersedia: {e} -- pakai decode manual saja.")
        _HAS_PYCOCO = False

    def _decode_rle_manual(rle, H, W):
        """
        Fallback decode RLE ketika pycocotools.decode() gagal (format
        uncompressed: 'counts' berupa list angka, bukan bytes terkompresi).
        Sama seperti _decode_coco_rle di kode referensi Anda.
        """
        if not isinstance(rle, dict) or "counts" not in rle or "size" not in rle:
            raise ValueError("Format RLE tidak dikenali untuk decode manual.")
        counts = rle["counts"]
        size   = rle["size"]
        h, w   = int(size[0]), int(size[1])
        flat   = np.zeros(h * w, dtype=np.uint8)
        idx, val = 0, 0
        for run in counts:
            run = int(run)
            if run > 0 and val == 1:
                flat[idx:idx + run] = 1
            idx += run          # tetap maju walau run == 0
            val = 1 - val       # tetap toggle walau run == 0 (bug lama: skip toggle)
        m = flat.reshape((w, h)).T
        if m.shape != (H, W):
            m = cv2.resize(m.astype(np.uint8), (W, H), interpolation=cv2.INTER_NEAREST)
        return m

    n_decoded, n_failed = 0, 0
    for rle in rles:
        m2 = None
        if _HAS_PYCOCO:
            try:
                m2 = maskUtils.decode(rle)
                if m2.ndim == 3:
                    m2 = m2[:, :, 0]
                if m2.shape != (H, W):
                    m2 = cv2.resize(m2.astype(np.uint8), (W, H),
                                     interpolation=cv2.INTER_NEAREST)
            except Exception:
                m2 = None
        if m2 is None:
            try:
                m2 = _decode_rle_manual(rle, H, W)
            except Exception as e:
                n_failed += 1
                if n_failed == 1:
                    print(f"  ⚠ [SAC] Gagal decode RLE (contoh error): {e}")
                continue
        score += (m2 > 0).astype(np.uint16)
        n_decoded += 1

    print(f"  [SAC] RLE berhasil di-decode: {n_decoded}/{n_mask} "
          f"(gagal: {n_failed})")
    return score


def extract_layer6_sac(gdf, img_pre, img_post, raster_transform, raster_shape,
                        sam_checkpoint, sac_params=None, bin_thr=None,
                        do_morph=True, return_raw_mask=False):
    """
    Perubahan per polygon menggunakan AnyChange (Segment Any Change).

    Args:
        return_raw_mask: jika True, return array boolean tile-penuh change_bin
            (setelah bin_thr) untuk visualisasi/QC.

    Returns:
        pd.DataFrame: polygon_id, sac_change_pct, sac_score, kelas_sac_pred
        ATAU np.ndarray (H,W) bool jika return_raw_mask=True
    """
    if sac_params is None:
        sac_params = SAC_PARAMS_FINETUNED
    if bin_thr is None:
        bin_thr = SAC_BIN_THR_BEST

    empty_df = pd.DataFrame(columns=["polygon_id", "sac_change_pct",
                                      "sac_score", "kelas_sac_pred"])
    if len(gdf) == 0 and not return_raw_mask:
        return empty_df

    from torchange.models.segment_any_change import AnyChange

    H, W = raster_shape

    def _to_uint8(img_float):
        img = img_float.astype(np.float32)
        mn, mx = img.min(), img.max()
        if mx == mn:
            return np.zeros_like(img, dtype=np.uint8)
        return ((img - mn) / (mx - mn) * 255).astype(np.uint8)

    img1 = _to_uint8(img_pre)
    img2 = _to_uint8(img_post)

    model = AnyChange('vit_b', sam_checkpoint=sam_checkpoint)
    model.make_mask_generator(
        points_per_side        = sac_params["points_per_side"],
        stability_score_thresh = sac_params["stability_score_thresh"],
    )
    try:
        model.set_hyperparameters(
            change_confidence_threshold = sac_params["change_confidence_threshold"],
            use_normalized_feature      = sac_params["use_normalized_feature"],
            bitemporal_match            = sac_params["bitemporal_match"],
        )
    except TypeError:
        model.set_hyperparameters(
            change_confidence_threshold = sac_params["change_confidence_threshold"],
            use_normalized_feature      = sac_params["use_normalized_feature"],
        )
        print("  ⚠ [SAC] bitemporal_match tidak didukung versi ini, di-skip.")

    print(f"  [SAC] Inference AnyChange (points_per_side="
          f"{sac_params['points_per_side']}) ...")
    changemasks, _, _ = model.forward(img1, img2)

    score_raw = maskdata_to_score(changemasks, H, W)
    score_8u  = np.clip(score_raw, 0, 255).astype(np.uint8)

    print(f"  [SAC] Score map (SEBELUM bin_thr) — min={score_8u.min()}, "
          f"max={score_8u.max()}, mean={score_8u.mean():.3f}, "
          f"pixel>0: {(score_8u > 0).sum():,} / {H*W:,}")
    if score_8u.max() == 0:
        print("  ⚠⚠ Score map SELURUHNYA 0 — tidak ada mask yang menandai "
              "perubahan sama sekali. Ini bukan soal bin_thr, tapi "
              "model.forward()/set_hyperparameters() tidak menghasilkan "
              "mask 'berubah' apa pun untuk pasangan citra ini.")
    elif score_8u.max() < bin_thr:
        print(f"  ⚠ Score map max ({score_8u.max()}) < bin_thr ({bin_thr}) "
              f"— seluruh hasil akan 0 setelah dibinarisasi. Pertimbangkan "
              f"menurunkan bin_thr.")

    kernel     = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    change_bin = (score_8u >= bin_thr).astype(np.uint8)
    if do_morph:
        change_bin = cv2.morphologyEx(change_bin, cv2.MORPH_OPEN,  kernel, iterations=1)
        change_bin = cv2.morphologyEx(change_bin, cv2.MORPH_CLOSE, kernel, iterations=1)

    if return_raw_mask:
        return change_bin.astype(bool)

    if len(gdf) == 0:
        return empty_df

    hasil = []
    for _, row in gdf.iterrows():
        poly_mask = get_poly_mask(row.geometry, raster_shape, raster_transform)
        luas      = int(poly_mask.sum())

        if luas == 0:
            sac_change_pct = 0.0
        else:
            changed        = int((change_bin & poly_mask).sum())
            sac_change_pct = (changed / luas) * 100

        score_val, kelas = classify_pct(sac_change_pct, low=10, high=50)

        hasil.append({
            "polygon_id"    : int(row["polygon_id"]),
            "sac_change_pct": round(sac_change_pct, 2),
            "sac_score"     : score_val,
            "kelas_sac_pred": kelas,
        })

    return pd.DataFrame(hasil)

# ---- CELL 10 — orkestrator extract_all_features (hybrid) (baris 765-829) ----
FEATURE_LAYERS = [
    ("batas",      "batas_loss_pct",  "kelas_batas_pred"),
    ("material",   "material_pct",     "kelas_material_pred"),
    ("tanaman",    "tanaman_loss_pct", "kelas_tanaman_pred"),
    ("radiometri", "radiometri_pct",   "kelas_radiometri_pred"),
    ("genangan",   "genangan_pct",     "kelas_genangan_pred"),
    ("sac",        "sac_change_pct",   "kelas_sac_pred"),
]

CONT_COLS = [f"f_{name}_cont" for name, _, _ in FEATURE_LAYERS]
ORD_COLS  = [f"f_{name}_ord"  for name, _, _ in FEATURE_LAYERS]


def extract_all_features(gdf, img_pre, img_post, raster_transform, raster_shape,
                          sam_checkpoint, sac_params=None):
    """
    Jalankan keenam layer, gabungkan jadi fitur HYBRID.

    Returns:
        pd.DataFrame: polygon_id,
            f_batas_cont, f_material_cont, f_tanaman_cont,
            f_radiometri_cont, f_genangan_cont, f_sac_cont   (float %, untuk model)
            f_batas_ord, f_material_ord, f_tanaman_ord,
            f_radiometri_ord, f_genangan_ord, f_sac_ord      (int 1-3, pelaporan)
    """
    _empty = pd.DataFrame(columns=["polygon_id"] + CONT_COLS + ORD_COLS)
    if len(gdf) == 0:
        return _empty

    print("  [Layer 1] Batas lahan (edge detection) ...")
    df_l1 = extract_layer1_batas(gdf, img_pre, img_post, raster_transform, raster_shape)

    print("  [Layer 2] Material asing (CVA + HSV) ...")
    df_l2 = extract_layer2_material(gdf, img_post, raster_transform, raster_shape,
                                     img_pre=img_pre)

    print("  [Layer 3] Kehilangan tanaman (ExG) ...")
    df_l3 = extract_layer3_tanaman(gdf, img_pre, img_post, raster_transform, raster_shape)

    print("  [Layer 4] Perubahan radiometri (CVA) ...")
    df_l4 = extract_layer4_radiometri(gdf, img_pre, img_post, raster_transform, raster_shape)

    print("  [Layer 5] Genangan (Water Index) ...")
    df_l5 = extract_layer5_genangan(gdf, img_pre, img_post, raster_transform, raster_shape)

    print("  [Layer 6] SAC/AnyChange — ini yang paling lama ...")
    df_l6 = extract_layer6_sac(gdf, img_pre, img_post, raster_transform, raster_shape,
                                sam_checkpoint, sac_params)

    dfs = {"batas": df_l1, "material": df_l2, "tanaman": df_l3,
           "radiometri": df_l4, "genangan": df_l5, "sac": df_l6}

    df_feat = pd.DataFrame({"polygon_id": gdf["polygon_id"].values})
    for name, pct_col, kelas_col in FEATURE_LAYERS:
        df_layer = dfs[name][["polygon_id", pct_col, kelas_col]].copy()
        df_layer = df_layer.rename(columns={pct_col: f"f_{name}_cont"})
        df_layer[f"f_{name}_ord"] = df_layer[kelas_col].map(ORDINAL_MAP)
        df_layer = df_layer.drop(columns=[kelas_col])
        df_feat  = df_feat.merge(df_layer, on="polygon_id", how="inner")

    df_feat = df_feat[["polygon_id"] + CONT_COLS + ORD_COLS]  # rapikan urutan kolom
    n_valid = df_feat[CONT_COLS + ORD_COLS].notna().all(axis=1).sum()
    print(f"\n  ✅ extract_all_features (hybrid) selesai: {len(df_feat)} polygon,"
          f" {n_valid} valid (tidak ada NaN).")
    return df_feat


# ================================================================
# ADAPTASI APLIKASI WEB (ruang piksel, input array)
# ================================================================
def normalize_rgb_percentile(img_rgb, clip_percentiles=(2, 98)):
    """Logika normalisasi load_raster_rgb (percentile 2-98 per band) untuk
    array HxWx3 — dipakai untuk citra upload yang tidak berupa GeoTIFF."""
    img_hwc = np.asarray(img_rgb)[:, :, :3].astype(np.float32)
    lo, hi  = clip_percentiles
    out     = np.zeros_like(img_hwc, dtype=np.float32)

    for c in range(3):
        band         = img_hwc[..., c]
        p_lo, p_hi   = np.percentile(band[~np.isnan(band)], [lo, hi])
        band_clipped = np.clip(band, p_lo, p_hi)
        out[..., c]  = (band_clipped - p_lo) / (p_hi - p_lo + 1e-6)

    return out


def compute_features(gdf_pred, img_pre_rgb, img_post_rgb, sam_checkpoint=None):
    """Hitung 6 fitur f_*_cont (+ f_*_ord) untuk poligon hasil deteksi.

    Args:
        gdf_pred: GeoDataFrame koordinat piksel, wajib punya kolom polygon_id.
        img_pre_rgb, img_post_rgb: array HxWx3 RGB mentah, ukuran sama.
        sam_checkpoint: default -> dicari lewat pipeline.model_paths
            (env SAM_CHECKPOINT_PATH, models/, atau HF_MODEL_REPO).
    """
    sam_checkpoint = sam_checkpoint or resolve(SAM_FILE, "SAM_CHECKPOINT_PATH")
    img_pre  = normalize_rgb_percentile(img_pre_rgb)
    img_post = normalize_rgb_percentile(img_post_rgb)
    raster_shape = img_pre.shape[:2]
    return extract_all_features(gdf_pred, img_pre, img_post, PIXEL_TRANSFORM,
                                raster_shape, sam_checkpoint=sam_checkpoint)
