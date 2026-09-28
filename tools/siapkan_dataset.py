# -*- coding: utf-8 -*-
"""Siapkan dan (opsional: --unggah) unggah contoh citra GeoTIFF 4 tile uji ke HF Dataset.
  python -X utf8 artefak_fix/tools/siapkan_dataset.py [--unggah]"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DS = ROOT / "artefak_fix" / "dataset"
REPO = "ZaXira/palu-tsunami-lahan-pertanian"
TILES = ["00000163", "00000169", "00000184", "00000195"]

# perbaiki komentar ber-encoding rusak di requirements Space
req = ROOT / "artefak_fix" / "space" / "requirements.txt"
t = req.read_text(encoding="utf-8")
if "â€”" in t:
    req.write_text(t.replace("â€”", "—"), encoding="utf-8")
    print("requirements.txt: komentar diperbaiki")

(DS / "tif").mkdir(parents=True, exist_ok=True)
for tile in TILES:
    for fase in ("pre", "post"):
        nama = f"palu-tsunami_{tile}_{fase}_disaster.tif"
        src = ROOT / "artefak" / "tests" / "Gambar" / nama
        dst = DS / "tif" / nama
        if not dst.exists() or dst.stat().st_size != src.stat().st_size:
            shutil.copy2(src, dst)
        print(f"{nama}  {dst.stat().st_size / 1048576:.1f} MB")

try:
    import rasterio
    with rasterio.open(DS / "tif" / "palu-tsunami_00000195_pre_disaster.tif") as s:
        print("contoh metadata:", s.crs, s.res, s.width, "x", s.height, s.count, "band", s.dtypes[0])
except ImportError:
    print("rasterio tidak terpasang — pemeriksaan metadata dilewati")

(DS / "README.md").write_text("""---
license: cc-by-nc-sa-4.0
pretty_name: Contoh Citra Lahan Pertanian Terdampak Tsunami Palu 2018
task_categories:
- image-segmentation
language:
- id
tags:
- remote-sensing
- disaster
- agriculture
- xbd
size_categories:
- n<1K
---

# Contoh Citra Lahan Pertanian Terdampak Tsunami Palu 2018

Delapan citra GeoTIFF (pasangan **sebelum** dan **sesudah** bencana) untuk **4 tile uji** penelitian
*"Penilaian Kerusakan Lahan Pertanian Terdampak Bencana Menggunakan Citra Satelit Resolusi Sangat Tinggi
dengan Metode Deep Learning dan Machine Learning: Studi Kasus Tsunami Palu 2018"*
(Rafliansyah Dwi Setiawan Tondau, Politeknik Statistika STIS, 2026).

Citra ini dapat diunggah langsung ke aplikasi
[ZaXira/lahan-pertanian-terdampak](https://huggingface.co/spaces/ZaXira/lahan-pertanian-terdampak);
jalur GeoTIFF mereproduksi hasil resmi penelitian secara identik.

| Tile | Petak ground truth | Berkas |
|---|---|---|
| 00000163 | 113 | `tif/palu-tsunami_00000163_{pre,post}_disaster.tif` |
| 00000169 | 155 | `tif/palu-tsunami_00000169_{pre,post}_disaster.tif` |
| 00000184 | 243 | `tif/palu-tsunami_00000184_{pre,post}_disaster.tif` |
| 00000195 | 93 | `tif/palu-tsunami_00000195_{pre,post}_disaster.tif` |

**Spesifikasi:** 3 band float32, EPSG:32751 (WGS 84 / UTM 51S), resolusi 0,4984 m/piksel,
sekitar 1028 × 1022 piksel (±26 ha per tile). Citra telah digeoreferensi ulang dari chip xBD.

## Sumber dan lisensi

Citra berasal dari subset *palu-tsunami* pada dataset **xBD** (Gupta dkk., 2019), yang bersumber dari
Maxar/DigitalGlobe Open Data Program dan dirilis dengan lisensi **CC BY-NC-SA 4.0**. Dataset turunan ini
mengikuti lisensi yang sama: hanya untuk penggunaan non-komersial, dengan atribusi, dan dibagikan dengan
lisensi serupa.

> Gupta, R., Hosfelt, R., Sajeev, S., Patel, N., Goodman, B., Doshi, J., Heim, E., Choset, H., & Gaston, M.
> (2019). xBD: A dataset for assessing building damage from satellite imagery. arXiv:1911.09296.
""", encoding="utf-8")
print("README dataset ditulis")

if "--unggah" in sys.argv:
    from huggingface_hub import HfApi
    api = HfApi()
    api.create_repo(REPO, repo_type="dataset", exist_ok=True)
    api.upload_folder(repo_id=REPO, repo_type="dataset", folder_path=str(DS),
                      commit_message="Contoh citra GeoTIFF 4 tile uji (Tsunami Palu 2018)")
    print("diunggah:", f"https://huggingface.co/datasets/{REPO}")
