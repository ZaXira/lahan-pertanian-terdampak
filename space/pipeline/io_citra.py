"""
Pembacaan citra unggahan (JPG/PNG/TIF) lewat rasterio/GDAL.

Dipakai supaya GeoTIFF 16/32-bit bisa diproses apa adanya — jalur inilah yang
terbukti mereproduksi hasil resmi skripsi 100% identik, sedangkan JPG/PNG 8-bit
kehilangan sebagian informasi (lihat kaggle/Output uji konversi 8-bit.txt).

Bonus GeoTIFF: resolusi (meter/piksel) bisa dibaca dari metadata, sehingga
pengguna tidak perlu menebaknya.
"""
import math
import os

import numpy as np
import rasterio

EKSTENSI_DIDUKUNG = (".jpg", ".jpeg", ".png", ".tif", ".tiff")


def _resolusi_meter(src):
    """Resolusi meter/piksel dari metadata raster; None kalau tidak bergeoreferensi."""
    if src.crs is None:
        return None
    res_x = abs(src.transform.a)
    if res_x == 0:
        return None
    if src.crs.is_projected:
        # CRS proyeksi (mis. UTM) sudah dalam meter
        return float(res_x)
    if src.crs.is_geographic:
        # Derajat -> meter, dikoreksi lintang tengah citra
        lat = src.bounds.bottom + (src.bounds.top - src.bounds.bottom) / 2
        return float(res_x * 111320 * math.cos(math.radians(lat)))
    return None


def baca_citra(path):
    """Baca file citra menjadi (array HxWx3 nilai asli, meta).

    meta: {"resolusi_m", "crs", "dtype", "ukuran", "n_band_asli", "nama"}
    Nilai piksel TIDAK dinormalisasi di sini — tiap tahap pipeline punya
    normalisasinya sendiri.
    """
    if path is None:
        return None, {}
    ext = os.path.splitext(str(path))[1].lower()
    if ext not in EKSTENSI_DIDUKUNG:
        raise ValueError(
            f"Format '{ext or path}' tidak didukung. Gunakan: "
            f"{', '.join(EKSTENSI_DIDUKUNG)}.")

    with rasterio.open(path) as src:
        n = src.count
        if n >= 3:
            arr = src.read([1, 2, 3])
        elif n == 1:
            arr = np.repeat(src.read(1)[None], 3, axis=0)
        else:
            raise ValueError(f"Citra punya {n} band; butuh 1 band (abu-abu) atau minimal 3 (RGB).")
        meta = {
            "resolusi_m": _resolusi_meter(src),
            "crs": str(src.crs) if src.crs else None,
            "dtype": str(src.dtypes[0]),
            "ukuran": (src.width, src.height),
            "n_band_asli": n,
            "nama": os.path.basename(str(path)),
        }
    return np.transpose(arr, (1, 2, 0)), meta


def pratinjau_uint8(img_rgb):
    """Versi 8-bit untuk ditampilkan di UI (stretch percentile 2-98 gabungan band).
    Hanya untuk tampilan — pipeline tetap memakai nilai asli."""
    arr = np.asarray(img_rgb)[:, :, :3].astype(np.float32)
    lo, hi = np.percentile(arr, 2), np.percentile(arr, 98)
    arr = np.clip((arr - lo) / max(float(hi - lo), 1e-6), 0, 1)
    return (arr * 255).astype(np.uint8)
