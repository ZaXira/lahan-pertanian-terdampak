---
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
configs:
- config_name: default
  data_files:
  - split: train
    path:
    - jpg/*.jpg
    - jpg/metadata.csv
---

# Contoh Citra Lahan Pertanian Terdampak Tsunami Palu 2018

Delapan citra (pasangan **sebelum** dan **sesudah** bencana) untuk **4 tile uji** penelitian
*"Penilaian Kerusakan Lahan Pertanian Terdampak Bencana Menggunakan Citra Satelit Resolusi Sangat Tinggi
dengan Metode Deep Learning dan Machine Learning: Studi Kasus Tsunami Palu 2018"*
(Rafliansyah Dwi Setiawan Tondau, Politeknik Statistika STIS, 2026).

Citra ini dapat diunggah langsung ke aplikasi
[ZaXira/lahan-pertanian-terdampak](https://huggingface.co/spaces/ZaXira/lahan-pertanian-terdampak);
jalur GeoTIFF mereproduksi hasil resmi penelitian secara identik.

## Unduh

| Paket (8 citra: pre + post untuk 4 tile) | Ukuran | Kegunaan |
|---|---|---|
| [GeoTIFF (float32)](https://huggingface.co/datasets/ZaXira/palu-tsunami-lahan-pertanian/resolve/main/unduh/palu-tsunami_4tile_tif.zip?download=true) | 82,9 MB | **Disarankan.** Hasil identik dengan penelitian; resolusi terisi otomatis |
| [PNG 8-bit](https://huggingface.co/datasets/ZaXira/palu-tsunami-lahan-pertanian/resolve/main/unduh/palu-tsunami_4tile_png.zip?download=true) | 9,7 MB | Tanpa georeferensi; isi resolusi 0,4984 m/piksel secara manual |
| [JPG 8-bit (kualitas 95)](https://huggingface.co/datasets/ZaXira/palu-tsunami-lahan-pertanian/resolve/main/unduh/palu-tsunami_4tile_jpg.zip?download=true) | 2,2 MB | Paling ringan; kompresi lossy |

Berkas satuan ada di folder `tif/`, `png/`, dan `jpg/` (tab *Files and versions*).

| Tile | Petak ground truth | Nama berkas (pre dan post) |
|---|---|---|
| 00000163 | 113 | `palu-tsunami_00000163_{pre,post}_disaster.{tif,png,jpg}` |
| 00000169 | 155 | `palu-tsunami_00000169_{pre,post}_disaster.{tif,png,jpg}` |
| 00000184 | 243 | `palu-tsunami_00000184_{pre,post}_disaster.{tif,png,jpg}` |
| 00000195 | 93 | `palu-tsunami_00000195_{pre,post}_disaster.{tif,png,jpg}` |

**Konversi PNG/JPG:** ketiga band diskalakan dengan **satu skala min-max gabungan** ke 0–255, sama dengan
normalisasi yang dipakai model deteksi. Pada uji aplikasi, jalur PNG 8-bit dengan konversi ini mendeteksi
509 dari 526 poligon (96,8%) dengan 469 kelas sama (89,2%), sedangkan GeoTIFF mereproduksi 526/526 secara
identik. Jalur JPG tidak diuji secara terpisah. *Dataset viewer* menampilkan versi JPG karena GeoTIFF
float32 tidak dapat dibaca oleh pratinjau Hugging Face; berkas GeoTIFF-nya sendiri tidak rusak.

**Spesifikasi:** 3 band float32, EPSG:32751 (WGS 84 / UTM 51S), resolusi 0,4984 m/piksel,
sekitar 1028 × 1022 piksel (±26 ha per tile). Citra telah digeoreferensi ulang dari chip xBD.

## Sumber dan lisensi

Citra berasal dari subset *palu-tsunami* pada dataset **xBD** (Gupta dkk., 2019), yang bersumber dari
Maxar/DigitalGlobe Open Data Program dan dirilis dengan lisensi **CC BY-NC-SA 4.0**. Dataset turunan ini
mengikuti lisensi yang sama: hanya untuk penggunaan non-komersial, dengan atribusi, dan dibagikan dengan
lisensi serupa.

> Gupta, R., Hosfelt, R., Sajeev, S., Patel, N., Goodman, B., Doshi, J., Heim, E., Choset, H., & Gaston, M.
> (2019). xBD: A dataset for assessing building damage from satellite imagery. arXiv:1911.09296.
