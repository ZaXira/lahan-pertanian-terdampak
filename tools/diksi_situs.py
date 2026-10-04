# -*- coding: utf-8 -*-
"""Revisi diksi dosen (Oktober 2026) pada teks tampilan situs (web/) dan aplikasi Gradio (space/).
Hanya teks yang dilihat pengguna yang diubah; kunci data, nama variabel, dan logika pipeline tidak disentuh
(keluaran numerik aplikasi tetap identik dengan hasil resmi 526/526).
Jalankan ulang setelah tools/bangun_aset.py (yang membangkitkan web/assets/data/data.js dari tabel lama):
  python -X utf8 artefak_fix/tools/diksi_situs.py"""
import io
import json
import re
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]              # artefak_fix
SKRIP = ROOT.parent / "Kelengkapan sidang" / "_skrip"
sys.path.insert(0, str(SKRIP))
from diksi_aturan import ganti  # noqa: E402
from tambal_teks import baris_tinta, ganti as tambal  # noqa: E402

M = "Mask R-CNN–RF"


def ganti_berkas(rel, pasangan):
    p = ROOT / rel
    s = p.read_text(encoding="utf-8")
    for a, b in pasangan:
        if a not in s:
            if b in s:
                continue                      # sudah diterapkan sebelumnya
            raise SystemExit(f"{rel}: tidak ditemukan: {a!r}")
        s = s.replace(a, b)
    p.write_text(s, encoding="utf-8")
    print("diperbarui", rel)


# ================================================================ halaman situs
ganti_berkas("web/index.html", [
    ("Mask R-CNN membentuk poligon petak", "Mask R-CNN membentuk segmen petak"),
    ("Satu alur <em>end-to-end</em> yang berjalan", f"Satu model {M} yang berjalan"),
    ("<h3>Bentuk poligon petak</h3>", "<h3>Segmentasi petak</h3>"),
    ('alt="Hasil pipeline end-to-end pada tile 00000195"', f'alt="Hasil model {M} pada tile 00000195"'),
    ('<div class="who">Pipeline <em>end-to-end</em></div>', f'<div class="who">Model {M}</div>'),
    ("F1 tingkat instans pembentukan poligon", "F1 tingkat instans segmentasi"),
    ("Kappa berbobot kuadratik", "Kappa tertimbang kuadratik"),
    ("poligon keluaran aplikasi identik", "segmen keluaran aplikasi identik"),
    ('toLocaleString("id-ID")} poligon`', 'toLocaleString("id-ID")} segmen`'),
])
ganti_berkas("web/hasil.html", [
    ("pipeline end-to-end, dan validasi aplikasi web", f"model {M}, dan validasi aplikasi web"),
    ("<small>Tujuan 1</small>Poligon</button>", "<small>Tujuan 1</small>Segmentasi</button>"),
    ("<small>Tujuan 3</small>End-to-end</button>", f"<small>Tujuan 3</small>{M}</button>"),
    ("jauh lebih sedikit poligon keliru", "jauh lebih sedikit segmen keliru"),
    ("Mask R-CNN juga tidak kolaps pada", "Mask R-CNN juga tidak gagal pada"),
    ("YOLOv8-seg kolaps pada", "YOLOv8-seg gagal pada"),
    ("Kappa berbobot kuadratik", "Kappa tertimbang kuadratik"),
    ("<h2>Kinerja pipeline per tile</h2>", f"<h2>Kinerja model {M} per tile</h2>"),
    ("(skenario <em>oracle</em>)", "(model pembanding)"),
    ("seluruh 526 poligon keluaran aplikasi", "seluruh 526 segmen keluaran aplikasi"),
    ('label: "Akurasi klasifikasi (matched)"', f'label: "Akurasi model {M}"'),
    ("F1-<em>macro matched-only</em>", f"F1-<em>macro</em> {M}"),
])
ganti_berkas("web/metode.html", [
    ("dan evaluasi end-to-end.", f"dan evaluasi model {M}."),
    ("<em>pipeline end-to-end</em>", f"model {M}"),
    ("Kappa berbobot kuadratik", "Kappa tertimbang kuadratik"),
    ("skenario <em>oracle</em>", "model pembanding"),
    ("jumlah poligon per <em>fold</em>", "jumlah segmen per <em>fold</em>"),
    ("Tujuan 1: pembentukan poligon", "Tujuan 1: segmentasi"),
    ("Tujuan 3: <em>end-to-end</em>", f"Tujuan 3: model {M}"),
    ("F1 per kelas (<em>matched-only</em>)", f"F1 {M}"),
    ("Kesetaraan poligon, fitur", "Kesetaraan segmen, fitur"),
])
ganti_berkas("web/demo.html", [
    ("<th>Jumlah poligon</th>", "<th>Jumlah segmen</th>"),
])
ganti_berkas("web/unggah.html", [
    ("<caption>Jumlah poligon dan luas per kelas</caption>", "<caption>Jumlah segmen dan luas per kelas</caption>"),
    ("${headers.map((h) => `<", "${headers.map((h) => LABEL_KOLOM[h] || h).map((h) => `<"),
    ("(${g.resmi.n_pred} poligon)", "(${g.resmi.n_pred} segmen)"),
    ("Terdampak Sedang dan poligon kecil", "Terdampak Sedang dan segmen kecil"),
])
# label tampilan untuk kunci kolom lama (hasil tersimpan dan Space versi lama memakai "Jumlah Poligon")
p = ROOT / "web" / "unggah.html"
s = p.read_text(encoding="utf-8")
if "const LABEL_KOLOM" not in s:
    s = s.replace("/* ---------- cara 1:", 'const LABEL_KOLOM = { "Jumlah Poligon": "Jumlah Segmen" };\n\n/* ---------- cara 1:', 1)
    assert "const LABEL_KOLOM" in s
    p.write_text(s, encoding="utf-8")

# ================================================================ data.js (hanya nilai teks)
p = ROOT / "web" / "assets" / "data" / "data.js"
s = p.read_text(encoding="utf-8")
i = s.index("window.DATA = ")
data = json.loads(s[i + len("window.DATA = "):].rstrip().rstrip(";"))
ISTILAH = ["pipeline end-to-end", "matched-only", "Matched-only", "matched", "Oracle", "oracle", "pipeline",
           "Pipeline"]
KHUSUS = [("Pasangan *matched* (TP)", "Pasangan TP"), ("§Klasifikasi pasangan *matched*", "§Klasifikasi pasangan TP"),
          ("§Komposisi kelas GT pasangan *matched*", "§Komposisi kelas GT pasangan TP"),
          ("§*Recall* klasifikasi per kelas GT pada pasangan *matched*",
           "§*Recall* klasifikasi per kelas GT pada pasangan TP"),
          ("Prediksi *pipeline*", f"Prediksi model {M}")]
n_ubah = [0]


def ganti_md(t):
    asli = t
    for a, b in KHUSUS:
        t = t.replace(a, b)
    for k in ISTILAH:                      # lepas tanda miring Markdown di sekitar istilah yang akan diganti
        t = t.replace(f"*{k}*", k)
    t = re.sub(r"\*(Oracle|oracle)\* ", r"\1 ", t)
    t = ganti(t)
    t = re.sub(r"(?<![*\w-])(end-to-end|matched)(?![*\w-])", r"*\1*", t)   # istilah asing yang tersisa tetap miring
    if t != asli:
        n_ubah[0] += 1
    return t


def jalan(o):
    if isinstance(o, dict):
        return {k: jalan(v) for k, v in o.items()}
    if isinstance(o, list):
        return [jalan(v) for v in o]
    if isinstance(o, str) and not re.fullmatch(r"[-\d.,%]*", o):
        return ganti_md(o)
    return o


data = jalan(data)
p.write_text(s[:i] + "window.DATA = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
print(f"diperbarui web/assets/data/data.js ({n_ubah[0]} teks)")

# ================================================================ gambar overlay (judul legenda)
IMG = ROOT / "web" / "assets" / "img"
SUDAH = IMG / ".diksi_overlay_selesai"          # penanda: overlay sudah ditambal, jangan ditambal ulang
for t in (() if SUDAH.exists() else ("00000163", "00000169", "00000184", "00000195")):
    f = IMG / f"tile_{t}_overlay.jpg"
    im = Image.open(f).convert("RGB")
    W, H = im.size
    rows = baris_tinta(im, (int(W * .3), H - 75, int(W * .7), H - 2))
    if not rows:
        continue
    y0, y1 = rows[0]
    try:
        tambal(im, (int(W * .3), y0 - 2, int(W * .7), y1 + 2), "Kelas kerusakan (jumlah poligon)",
               "Kelas kerusakan (jumlah segmen)", rata="tengah")
    except ValueError:
        continue
    im.save(f, quality=90)
    im.save(f.with_suffix(".webp"), quality=85)
    print("diperbarui", f.name, "+ .webp")
SUDAH.write_text("judul legenda overlay sudah: jumlah segmen\n", encoding="utf-8")

# ================================================================ aplikasi Gradio (teks tampilan saja)
ganti_berkas("space/app.py", [
    ("hasil resmi penelitian secara identik (526/526 poligon).", "hasil resmi penelitian secara identik (526/526 segmen)."),
    ("- **Terdampak Sedang** dan poligon kecil", "- **Terdampak Sedang** dan segmen kecil"),
    ("| jumlah piksel × resolusi² | poligon + resolusi |", "| jumlah piksel × resolusi² | segmen + resolusi |"),
    ('label="Jumlah poligon & luas per kelas kerusakan"', 'label="Jumlah segmen & luas per kelas kerusakan"'),
])
ganti_berkas("space/pipeline/area.py", [('COL_JUMLAH = "Jumlah Poligon"', 'COL_JUMLAH = "Jumlah Segmen"')])
ganti_berkas("space/pipeline/predict.py", [('lines.append(f"Poligon lahan terdeteksi:', 'lines.append(f"Segmen lahan terdeteksi:')])
ganti_berkas("space/pipeline/visualize.py", [('title="Kelas kerusakan (jumlah poligon)"', 'title="Kelas kerusakan (jumlah segmen)"')])
ganti_berkas("space/README.md", [
    ("Aplikasi ini menjalankan pipeline Tujuan 3", f"Aplikasi ini menjalankan model {M} (Tujuan 3)"),
    ("(526/526 poligon identik)", "(526/526 segmen identik)"),
])

# ================================================================ lokalisasi -> segmentasi (teks tampilan HTML)
# kunci data (f1_lokalisasi, recall_lokalisasi) tidak tersentuh: huruf kecil dan diawali garis bawah
LOK = [(re.compile(r"\bF1_lokalisasi\b"), "F1_segmentasi"), (re.compile(r"\bLokalisasi\b"), "Segmentasi"),
       (re.compile(r"\blokalisasi\b"), "segmentasi")]
for nama in ("index.html", "hasil.html", "metode.html", "demo.html", "unggah.html"):
    p = ROOT / "web" / nama
    s = p.read_text(encoding="utf-8")
    s2 = s
    for pola, g in LOK:
        s2 = pola.sub(g, s2)
    if s2 != s:
        p.write_text(s2, encoding="utf-8")
        print("lokalisasi -> segmentasi:", nama)
