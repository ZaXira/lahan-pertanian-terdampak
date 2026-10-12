# Penilaian Kerusakan Lahan Pertanian Terdampak Bencana

Kode artefak skripsi **"Penilaian Kerusakan Lahan Pertanian Terdampak Bencana Menggunakan Citra Satelit Resolusi
Sangat Tinggi dengan Metode Deep Learning dan Machine Learning: Studi Kasus Tsunami Palu 2018"**.

Rafliansyah Dwi Setiawan Tondau (NIM 222212827), D-IV Komputasi Statistik peminatan Sains Data,
Politeknik Statistika STIS, 2026. Dosen pembimbing: Dr. Eng. Arie W. Wijayanto, S.S.T., M.T. Tahun lulus: 2026.

| | Tautan |
|---|---|
| Situs penelitian (*web story*) | https://lahan-terdampak-palu.vercel.app |
| Aplikasi (Hugging Face Spaces, ZeroGPU) | https://huggingface.co/spaces/ZaXira/lahan-pertanian-terdampak |
| Contoh citra GeoTIFF (4 tile uji) | https://huggingface.co/datasets/ZaXira/palu-tsunami-lahan-pertanian |

## Isi repositori

```
web/       Situs statis (HTML/CSS/JS tanpa build) yang di-deploy ke Vercel.
           assets/data/data.js dibangkitkan dari tabel resmi Bab IV oleh tools/bangun_aset.py.
space/     Aplikasi Gradio untuk Hugging Face Spaces: app.py, pipeline/ (deteksi Mask R-CNN,
           enam layer fitur, klasifikasi Random Forest, luas per kelas), third_party/detectron2.
dataset/   Kartu dataset contoh GeoTIFF (berkas .tif sendiri di-host di Hugging Face).
tools/     Skrip pembangun aset, unggah dataset, deploy Space, dan uji regresi/ujung-ke-ujung.
```

Alur pipeline: Mask R-CNN (detectron2 R50-FPN, `DETECTIONS_PER_IMAGE = 500`) membentuk poligon petak pada
citra sebelum bencana, enam *layer* fitur mengukur perubahan sebelum dan sesudah bencana, lalu Random Forest
menilai setiap petak ke dalam tiga kelas: Tidak Terdampak, Terdampak Sedang, dan Terdampak Berat.

## Menjalankan

**Situs** (tanpa build):

```bash
cd web
python -m http.server 8099      # buka http://127.0.0.1:8099
```

**Aplikasi** (butuh GPU atau CPU yang cukup kuat; bobot model diunduh dari repo yang ditunjuk `HF_MODEL_REPO`):

```bash
cd space
pip install -r requirements.txt
HF_MODEL_REPO=ZaXira/artefak-kerusakan-lahan python app.py
```

**Uji regresi** terhadap hasil resmi penelitian (tile 00000195: 115 poligon, 10/7/98, 10,0101 ha):

```bash
python -X utf8 tools/uji_space.py
```

## Validasi

Pada jalur GeoTIFF dengan presisi FP32, keluaran aplikasi identik dengan hasil resmi Tujuan 3 (526/526 poligon,
kelas 100% sama). Presisi dikunci ke FP32 (TF32 dimatikan) dan versi pustaka dikunci di `space/requirements.txt`
(scikit-learn 1.6.1). Citra JPG/PNG 8-bit perlu dikonversi dengan satu skala min-max gabungan untuk ketiga kanal.

## Lisensi dan kredit

Kode aplikasi: Apache-2.0. Citra: xBD / xView2 (Gupta dkk., 2019), CC BY-NC-SA 4.0.
Pustaka pihak ketiga: [detectron2](https://github.com/facebookresearch/detectron2) (Apache-2.0),
[Segment Anything](https://github.com/facebookresearch/segment-anything),
[pytorch-change-models / AnyChange](https://github.com/Z-Zheng/pytorch-change-models).
