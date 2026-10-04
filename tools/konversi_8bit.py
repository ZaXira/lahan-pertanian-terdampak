# -*- coding: utf-8 -*-
"""Buat versi PNG dan JPG 8-bit dari 8 GeoTIFF contoh (4 tile uji), plus paket zip per format.
Konversi = min-max GABUNGAN 3 band -> uint8, rumus sama persis dengan pipeline/detect.py
(rgb_to_model_bgr) dan jalur "PNG 8-bit (minmax)" pada uji Tabel B.
  python -X utf8 artefak_fix/tools/konversi_8bit.py"""
import zipfile
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image

DS = Path(__file__).resolve().parents[1] / "dataset"
(DS / "png").mkdir(exist_ok=True)
(DS / "jpg").mkdir(exist_ok=True)
(DS / "unduh").mkdir(exist_ok=True)

meta = ["file_name,tile,fase"]
for tif in sorted((DS / "tif").glob("*.tif")):
    arr = tifffile.imread(tif)
    if arr.ndim == 3 and arr.shape[0] in (3, 4) and arr.shape[-1] not in (3, 4):
        arr = np.moveaxis(arr, 0, -1)                      # (band, H, W) -> (H, W, band)
    arr = arr[:, :, :3].astype(np.float32)
    u8 = ((arr - arr.min()) / max(arr.max() - arr.min(), 1) * 255).astype(np.uint8)
    im = Image.fromarray(u8, "RGB")
    im.save(DS / "png" / f"{tif.stem}.png", optimize=True)
    im.save(DS / "jpg" / f"{tif.stem}.jpg", quality=95)
    _, tile, fase, _ = tif.stem.split("_")
    meta.append(f"{tif.stem}.jpg,{tile},{fase}")
    print(f"{tif.name}: {arr.shape[1]}x{arr.shape[0]}, rentang {arr.min():.1f}–{arr.max():.1f} -> png/jpg")
(DS / "jpg" / "metadata.csv").write_text("\n".join(meta) + "\n", encoding="utf-8")

for fmt, ext in (("tif", "tif"), ("png", "png"), ("jpg", "jpg")):
    z = DS / "unduh" / f"palu-tsunami_4tile_{fmt}.zip"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as f:
        for p in sorted((DS / fmt).glob(f"*.{ext}")):
            f.write(p, p.name)
    print(f"{z.name}: {z.stat().st_size / 1048576:.1f} MB")
