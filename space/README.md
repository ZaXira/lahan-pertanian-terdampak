---
title: Lahan Pertanian Terdampak Bencana
emoji: 🌾
colorFrom: green
colorTo: yellow
sdk: gradio
sdk_version: 6.28.0
python_version: "3.12.12"
app_file: app.py
pinned: false
license: apache-2.0
short_description: Penilaian kerusakan lahan pertanian dari citra pre/post
---

# Penilaian Kerusakan Lahan Pertanian Terdampak Bencana

Artefak skripsi **"PENILAIAN KERUSAKAN LAHAN PERTANIAN TERDAMPAK BENCANA MENGGUNAKAN CITRA SATELIT RESOLUSI SANGAT
TINGGI DENGAN METODE DEEP LEARNING DAN MACHINE LEARNING (Studi Kasus: Bencana Palu Tahun 2018)"**
— Rafliansyah Dwi Setiawan Tondau (NIM 222212827), Politeknik Statistika STIS, lulus 2026.
Dosen pembimbing: Dr. Eng. Arie W. Wijayanto, S.S.T., M.T.

- Situs penelitian: https://lahan-terdampak-palu.vercel.app
- Contoh citra GeoTIFF (4 tile uji): https://huggingface.co/datasets/ZaXira/palu-tsunami-lahan-pertanian

Aplikasi ini menjalankan model PKLPTB (model penilaian kerusakan lahan pertanian terdampak bencana, Tujuan 3) secara interaktif dengan bobot final penelitian (tanpa pelatihan
ulang): Mask R-CNN mendeteksi petak lahan pada citra sebelum bencana, enam layer fitur mengukur perubahan
sebelum–sesudah, lalu Random Forest menilai kerusakan ke dalam tiga kelas dan luas per kelas dihitung.

## API

Endpoint `/proses` menerima `(citra_pre, citra_post, resolusi_m_per_piksel)` dan mengembalikan
`(overlay, tabel_luas, log)`. Contoh dengan klien Python:

```python
from gradio_client import Client, handle_file
c = Client("ZaXira/lahan-pertanian-terdampak")
overlay, tabel, log = c.predict(handle_file("pre.tif"), handle_file("post.tif"), 0.4984, api_name="/proses")
```

## Catatan

- Logika pemrosesan identik dengan versi yang divalidasi: jalur GeoTIFF mereproduksi hasil resmi penelitian
  (526/526 segmen identik). JPG/PNG 8-bit menggeser sebagian prediksi; gunakan skala min–max gabungan 3 band.
- Presisi dikunci ke FP32 (TF32 dimatikan) dan versi pustaka dikunci di `requirements.txt`.
- Bobot model diunduh saat startup dari model repo yang ditunjuk variabel `HF_MODEL_REPO`.
- Berjalan di ZeroGPU: kuota GPU harian terbatas.

Kredit: [detectron2](https://github.com/facebookresearch/detectron2), [Segment Anything](https://github.com/facebookresearch/segment-anything),
[pytorch-change-models / AnyChange](https://github.com/Z-Zheng/pytorch-change-models). Citra: xBD / xView2 (Gupta dkk., 2019).
