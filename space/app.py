"""
Aplikasi web (Gradio) — Penilaian Kerusakan Lahan Pertanian Terdampak Bencana.

Artefak skripsi: Mask R-CNN (deteksi lahan, citra pre) + 6 layer fitur
perubahan (pre vs post) + Random Forest (klasifikasi kerusakan 3 kelas).

Versi tampilan baru (artefak_fix). Logika pemrosesan (muat_berkas, proses, pipeline/)
TIDAK diubah dari versi yang telah divalidasi (526/526 poligon identik).
Endpoint API: /proses — dipanggil juga oleh situs pendamping.
"""
import base64
import os
import traceback

import gradio as gr
import pandas as pd

try:
    # Hugging Face Spaces ZeroGPU: GPU dialokasikan hanya selama fungsi ber-dekorator
    # berjalan. Di luar Spaces paket ini tidak ada, dan dekoratornya tidak dipakai.
    import spaces

    def gpu_task(fn):
        # Durasi dipesan di muka & dicek terhadap sisa kuota harian, jadi jangan
        # berlebihan: 1024x1024 px butuh ~25 detik di ZeroGPU.
        return spaces.GPU(duration=int(os.environ.get("ZEROGPU_DURATION", "90")))(fn)
except ImportError:
    def gpu_task(fn):
        return fn

from pipeline.area import COL_JUMLAH, COL_KELAS, COL_LUAS, DEFAULT_RESOLUSI_M
from pipeline.io_citra import EKSTENSI_DIDUKUNG, baca_citra, pratinjau_uint8
from pipeline.predict import MAX_SIDE_PX, TOLERANSI_UKURAN, format_log, run_pipeline

JUDUL = "Penilaian Kerusakan Lahan Pertanian Terdampak Bencana"
SITUS = os.environ.get("SITUS_URL", "https://lahan-terdampak-palu.vercel.app")
DATASET = "https://huggingface.co/datasets/ZaXira/palu-tsunami-lahan-pertanian"
TABEL_KOSONG = pd.DataFrame(columns=[COL_KELAS, COL_JUMLAH, COL_LUAS])
TILE_CONTOH = ["00000163", "00000169", "00000184", "00000195"]


def _siapkan_contoh():
    """Unduh 4 pasang GeoTIFF tile uji dari dataset ke folder aplikasi (untuk gr.Examples).
    Gagal unduh tidak boleh menghentikan aplikasi: contoh cukup tidak ditampilkan."""
    try:
        from huggingface_hub import hf_hub_download
        folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "contoh")
        unduh = lambda t, fase: hf_hub_download(  # noqa: E731
            "ZaXira/palu-tsunami-lahan-pertanian", f"tif/palu-tsunami_{t}_{fase}_disaster.tif",
            repo_type="dataset", local_dir=folder)
        return [[unduh(t, "pre"), unduh(t, "post"), DEFAULT_RESOLUSI_M] for t in TILE_CONTOH]
    except Exception as e:
        print(f"[contoh] GAGAL mengunduh contoh: {type(e).__name__}: {e}", flush=True)
        return []


CONTOH = _siapkan_contoh()


def _logo_data_uri():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "logo-stis.png")
    if not os.path.exists(p):
        return ""
    with open(p, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


# ------------------------------------------------------------------ logika (tidak diubah)
def _info_citra(meta, label):
    w, h = meta["ukuran"]
    baris = f"**{label}**: `{meta['nama']}` · {w}×{h} px · {meta['dtype']} · {meta['n_band_asli']} band"
    if meta.get("crs"):
        baris += f" · {meta['crs']}"
    if meta.get("resolusi_m"):
        baris += f" · **{meta['resolusi_m']:.4f} m/piksel**"
    return baris


def muat_berkas(path, label, resolusi_sekarang):
    """Handler unggah: tampilkan pratinjau + info, isi resolusi dari metadata GeoTIFF."""
    if not path:
        return None, "", resolusi_sekarang
    try:
        img, meta = baca_citra(path)
    except Exception as e:
        return None, f"⚠️ **{label}**: {e}", resolusi_sekarang
    res = meta.get("resolusi_m")
    return pratinjau_uint8(img), _info_citra(meta, label), (res if res else resolusi_sekarang)


@gpu_task
def proses(berkas_pre, berkas_post, resolusi):
    try:
        img_pre, meta_pre = baca_citra(berkas_pre)
        img_post, meta_post = baca_citra(berkas_post)
    except Exception as e:
        return None, TABEL_KOSONG, f"Status      : GAGAL\nERROR: [Baca berkas] {e}"

    catatan = []
    r_pre, r_post = meta_pre.get("resolusi_m"), meta_post.get("resolusi_m")
    if r_pre and r_post and abs(r_pre - r_post) / max(r_pre, r_post) > 0.01:
        catatan.append(f"Resolusi metadata pre ({r_pre:.4f} m) dan post ({r_post:.4f} m) berbeda.")
    if meta_pre.get("crs") and meta_post.get("crs") and meta_pre["crs"] != meta_post["crs"]:
        catatan.append(f"CRS pre ({meta_pre['crs']}) dan post ({meta_post['crs']}) berbeda — "
                       f"citra mungkin tidak sejajar piksel-ke-piksel.")

    try:
        overlay, tabel, log = run_pipeline(img_pre, img_post, resolusi)
        log["peringatan"] = catatan + log.get("peringatan", [])
        return overlay, (tabel if tabel is not None else TABEL_KOSONG), format_log(log)
    except Exception as e:  # jaring pengaman terakhir: UI tidak boleh crash
        traceback.print_exc()
        return None, TABEL_KOSONG, f"Status      : GAGAL\nERROR: {type(e).__name__}: {e}"


# ------------------------------------------------------------------ tampilan
TEMA = gr.themes.Soft(
    primary_hue=gr.themes.colors.green, secondary_hue=gr.themes.colors.amber, neutral_hue=gr.themes.colors.stone,
    font=[gr.themes.GoogleFont("Plus Jakarta Sans"), "system-ui", "sans-serif"],
    font_mono=[gr.themes.GoogleFont("JetBrains Mono"), "monospace"],
).set(button_primary_background_fill="#2f5d27", button_primary_background_fill_hover="#24481e",
      button_primary_text_color="#ffffff", block_radius="14px")

CSS = """
.gradio-container { max-width: 1180px !important; margin: 0 auto; }
#kepala { display:flex; gap:16px; align-items:center; padding:18px 20px; border-radius:16px;
  background: linear-gradient(120deg, #2f5d27 0%, #3f7a33 55%, #d9a441 140%); color:#fff; }
#kepala img { width:64px; height:64px; filter: invert(1); flex:none; }
#kepala h1 { font-family: Georgia, serif; font-size: 1.55rem; margin:0 0 4px; color:#fff; }
#kepala p { margin:0; opacity:.92; font-size:.95rem; }
#kepala a { color:#fff; font-weight:700; }
.kelas { display:flex; gap:16px; flex-wrap:wrap; font-size:.9rem; margin-top:6px; }
.kelas span { display:inline-flex; gap:6px; align-items:center; }
.kelas i { width:12px; height:12px; border-radius:3px; display:inline-block; }
"""

KEPALA = f"""
<div id="kepala">
  {f'<img src="{_logo_data_uri()}" alt="Logo Politeknik Statistika STIS">' if _logo_data_uri() else ''}
  <div><h1>{JUDUL}</h1>
  <p>Studi kasus Tsunami Palu 2018 · Mask R-CNN + enam layer fitur perubahan + Random Forest ·
  <a href="{SITUS}" target="_blank">Situs penelitian ↗</a> · <a href="{DATASET}" target="_blank">Contoh citra GeoTIFF ↗</a></p></div>
</div>
"""

PANDUAN = f"""
### Cara pakai
1. Unggah citra **sebelum** (pre-disaster) dan **sesudah** (post-disaster) bencana pada lokasi yang sama.
2. Periksa **resolusi** (meter/piksel). Untuk GeoTIFF nilainya terisi otomatis dari metadata.
3. Klik **Proses citra** dan tunggu sekitar 20–60 detik.

### Agar hasil sesuai penelitian
- **GeoTIFF asli memberi hasil terbaik.** Uji regresi pada 4 tile uji menunjukkan jalur GeoTIFF mereproduksi
  hasil resmi penelitian secara identik (526/526 segmen).
- Bila hanya ada JPG/PNG, skalakan ketiga band dengan **satu skala min–max yang sama**. Peregangan per band
  membuat lebih dari separuh lahan tidak terdeteksi (hanya 37,8% kelas sama dengan hasil resmi).
- Kedua citra harus **sejajar piksel-ke-piksel**; hindari tangkapan layar. Beda ukuran pre/post sampai
  {TOLERANSI_UKURAN * 100:.0f}% disamakan otomatis, lebih dari itu ditolak.
- Format: {', '.join(EKSTENSI_DIDUKUNG)} · sisi maksimum {MAX_SIDE_PX} px.

### Membaca hasil
- **Terdampak Berat** paling andal dan dapat dipakai sebagai penunjuk prioritas.
- **Terdampak Sedang** dan segmen kecil yang terisolasi perlu diperiksa ulang di lapangan.
- Luas per kelas bersifat indikatif: aplikasi tidak memiliki *ground truth*, sehingga *false positive*
  tidak dapat dikenali dan petak kecil dapat terlewat.

Contoh pasangan citra GeoTIFF dari 4 tile uji dapat dipilih langsung di bawah tombol **Proses citra**,
dan juga tersedia di [dataset ini]({DATASET}).

### Kuota GPU
Aplikasi berjalan di ZeroGPU yang kuotanya dihitung per pengguna. Pengunjung tanpa login mendapat kuota
paling kecil; **login ke Hugging Face** agar pemrosesan memakai kuota akun Anda sendiri yang lebih besar.
"""

TENTANG = f"""
### Tentang aplikasi
Artefak skripsi **"PENILAIAN KERUSAKAN LAHAN PERTANIAN TERDAMPAK BENCANA MENGGUNAKAN CITRA SATELIT RESOLUSI SANGAT
TINGGI DENGAN METODE DEEP LEARNING DAN MACHINE LEARNING (Studi Kasus: Bencana Palu Tahun 2018)"**.
Aplikasi ini menjalankan **model PKLPTB** (model penilaian kerusakan lahan pertanian terdampak bencana).

- **Nama:** Rafliansyah Dwi Setiawan Tondau
- **NIM:** 222212827
- **Tahun lulus:** 2026
- **Dosen pembimbing:** Dr. Eng. Arie W. Wijayanto, S.S.T., M.T.
- **Program studi:** D-IV Komputasi Statistik, peminatan Sains Data, Politeknik Statistika STIS

| Tahap | Metode | Masukan |
|---|---|---|
| 1. Deteksi lahan pertanian | Mask R-CNN (detectron2, R50-FPN) | citra pre |
| 2. Enam layer fitur perubahan | Canny, CVA+HSV, ExG, CVA+Otsu, indeks air RGB, AnyChange (SAM) | citra pre + post |
| 3. Klasifikasi kerusakan | Random Forest (3 kelas) | 6 fitur kontinu |
| 4. Luas per kelas | jumlah piksel × resolusi² | segmen + resolusi |

Aplikasi murni inferensi dengan bobot final penelitian, berjalan di ZeroGPU dengan presisi FP32 (TF32
dimatikan). Kuota GPU harian terbatas; bila habis, coba lagi nanti atau login ke Hugging Face.

Citra: xBD / xView2 (Gupta dkk., 2019), CC BY-NC-SA 4.0. Kredit perangkat lunak: detectron2, Segment Anything,
pytorch-change-models (AnyChange).
"""

with gr.Blocks(title=JUDUL) as demo:
    gr.HTML(KEPALA)
    with gr.Tabs():
        with gr.Tab("Proses citra"):
            with gr.Row(equal_height=False):
                with gr.Column():
                    in_pre = gr.File(label="Citra sebelum bencana (pre)", file_types=list(EKSTENSI_DIDUKUNG), type="filepath")
                    pratinjau_pre = gr.Image(label="Pratinjau pre", interactive=False, height=260)
                    info_pre = gr.Markdown()
                with gr.Column():
                    in_post = gr.File(label="Citra sesudah bencana (post)", file_types=list(EKSTENSI_DIDUKUNG), type="filepath")
                    pratinjau_post = gr.Image(label="Pratinjau post", interactive=False, height=260)
                    info_post = gr.Markdown()
            with gr.Row():
                in_res = gr.Number(label="Resolusi citra (meter/piksel) — terisi otomatis dari GeoTIFF",
                                   value=DEFAULT_RESOLUSI_M, minimum=0.01, step=0.01, scale=3)
                btn = gr.Button("Proses citra", variant="primary", scale=1, size="lg")
            if CONTOH:
                gr.Examples(examples=CONTOH, inputs=[in_pre, in_post, in_res], cache_examples=False,
                            example_labels=[f"Tile {t}" for t in TILE_CONTOH],
                            label="Contoh: 4 tile uji Palu 2018 (GeoTIFF). Klik salah satu, lalu tekan Proses citra.")
            gr.HTML('<div class="kelas"><span><i style="background:#27ae60"></i>Tidak Terdampak</span>'
                    '<span><i style="background:#f39c12"></i>Terdampak Sedang</span>'
                    '<span><i style="background:#c0392b"></i>Terdampak Berat</span></div>')
            out_img = gr.Image(label="Overlay kelas kerusakan di atas citra sesudah bencana", type="numpy", interactive=False)
            with gr.Row():
                out_tabel = gr.Dataframe(label="Jumlah segmen & luas per kelas kerusakan", value=TABEL_KOSONG, interactive=False)
                out_log = gr.Textbox(label="Log proses", lines=12, max_lines=20, interactive=False)
        with gr.Tab("Panduan"):
            gr.Markdown(PANDUAN)
        with gr.Tab("Tentang"):
            gr.Markdown(TENTANG)

    in_pre.change(lambda p, r: muat_berkas(p, "Citra pre", r), inputs=[in_pre, in_res],
                  outputs=[pratinjau_pre, info_pre, in_res], api_visibility="private")
    in_post.change(lambda p, r: muat_berkas(p, "Citra post", r), inputs=[in_post, in_res],
                   outputs=[pratinjau_post, info_post, in_res], api_visibility="private")
    btn.click(proses, inputs=[in_pre, in_post, in_res], outputs=[out_img, out_tabel, out_log], api_name="proses")


def pramuat():
    """Unduh & load model sebelum request pertama (dipakai di Spaces: HF_MODEL_REPO di-set),
    supaya unduhan ~730 MB tidak terjadi saat pengguna menunggu."""
    from pipeline.classify import load_classifier
    from pipeline.detect import get_predictor
    from pipeline.model_paths import SAM_FILE, resolve

    print("[pramuat] Mask R-CNN ...", flush=True)
    get_predictor()
    print("[pramuat] Random Forest + label encoder ...", flush=True)
    load_classifier()
    print("[pramuat] checkpoint SAM ...", flush=True)
    resolve(SAM_FILE, "SAM_CHECKPOINT_PATH")
    print("[pramuat] selesai — model siap.", flush=True)


if __name__ == "__main__":
    # Di Spaces, model di-load saat startup (root level) — pola yang disarankan ZeroGPU.
    if os.environ.get("SPACE_ID") or os.environ.get("HF_MODEL_REPO") or os.environ.get("PRELOAD_MODELS"):
        try:
            pramuat()
        except Exception as e:
            print(f"[pramuat] GAGAL: {type(e).__name__}: {e} — dicoba lagi saat request.", flush=True)
    demo.launch(theme=TEMA, css=CSS)
