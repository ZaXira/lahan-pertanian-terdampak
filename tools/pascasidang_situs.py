# -*- coding: utf-8 -*-
"""Revisi pascasidang situs (9 Oktober 2026):
  1. tabel lokasi administratif 18 tile terpilih di halaman Metode (catatan penguji);
  2. sisa diksi lama pada teks tampilan: "instans", "end-to-end", "jaring pengaman".
Kunci data dan logika tidak diubah. Jalankan setelah tools/bangun_aset.py dan tools/diksi_situs.py:
  python -X utf8 artefak_fix/tools/pascasidang_situs.py"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M = "Mask R-CNN–RF"


def ganti_berkas(rel, pasangan):
    p = ROOT / rel
    s = p.read_text(encoding="utf-8")
    for a, b in pasangan:
        if a not in s:
            if b in s:
                continue
            raise SystemExit(f"{rel}: tidak ditemukan: {a!r}")
        s = s.replace(a, b)
    p.write_text(s, encoding="utf-8")
    print("diperbarui", rel)


# ------------------------------------------------------------------ 1. lokasi administratif 18 tile
# (tile, peran, desa/kelurahan, kecamatan, kabupaten/kota, jumlah segmen ground truth)
# Irisan batas tile dengan batas desa/kelurahan (pembaruan 13 Juni 2023); desa < 10% luas tile tidak dicantumkan.
TILE = [
    ("00000065", "Latih", "Talise", "Mantikulore", "Kota Palu", 433),
    ("00000117", "Latih", "Talise", "Mantikulore", "Kota Palu", 511),
    ("00000163", "Uji", "Petobo", "Palu Selatan", "Kota Palu", 113),
    ("00000168", "Latih", "Petobo", "Palu Selatan", "Kota Palu", 105),
    ("00000169", "Uji", "Mpanau (85%), Petobo (15%)", "Sigi Biromaru, Palu Selatan", "Sigi, Kota Palu", 155),
    ("00000170", "Latih", "Petobo", "Palu Selatan", "Kota Palu", 59),
    ("00000182", "Latih", "Petobo", "Palu Selatan", "Kota Palu", 57),
    ("00000183", "Latih", "Petobo", "Palu Selatan", "Kota Palu", 212),
    ("00000184", "Uji", "Langaleso", "Dolo", "Sigi", 243),
    ("00000185", "Latih", "Langaleso (66%), Jono Oge (34%)", "Dolo, Sigi Biromaru", "Sigi", 140),
    ("00000186", "Latih", "Jono Oge (60%), Langaleso (37%)", "Sigi Biromaru, Dolo", "Sigi", 142),
    ("00000187", "Latih", "Pombewe", "Sigi Biromaru", "Sigi", 60),
    ("00000188", "Latih", "Jono Oge (61%), Sidera (39%)", "Sigi Biromaru", "Sigi", 170),
    ("00000189", "Latih", "Sidera (59%), Jono Oge (33%)", "Sigi Biromaru", "Sigi", 216),
    ("00000191", "Latih", "Langaleso", "Dolo", "Sigi", 93),
    ("00000193", "Latih", "Jono Oge (60%), Pombewe (40%)", "Sigi Biromaru", "Sigi", 268),
    ("00000194", "Latih", "Langaleso", "Dolo", "Sigi", 201),
    ("00000195", "Uji", "Pombewe", "Sigi Biromaru", "Sigi", 93),
]
assert sum(t[-1] for t in TILE) == 3271

baris = "\n".join(
    f'          <tr><td class="mono">{t}</td><td>{peran}</td><td class="l">{desa}</td><td class="l">{kec}</td>'
    f'<td class="l">{kab}</td><td>{n}</td></tr>'
    for t, peran, desa, kec, kab, n in TILE)

SEKSI = f'''<section class="alt" id="lokasi">
  <div class="wrap">
    <div class="head rv"><h2>Lokasi 18 tile terpilih</h2>
      <p class="muted">Tujuh tile berada di Kota Palu (Kelurahan Talise dan Petobo) dan sebelas di Kabupaten Sigi (Kecamatan Dolo dan Sigi Biromaru). Empat tile uji adalah 00000163, 00000169, 00000184, dan 00000195.</p></div>
    <div class="rv table-wrap"><table class="data">
      <caption>Lokasi administratif setiap tile</caption>
      <thead><tr><th>Tile</th><th>Peran</th><th>Desa/Kelurahan</th><th>Kecamatan</th><th>Kabupaten/Kota</th><th>Segmen</th></tr></thead>
      <tbody>
{baris}
      </tbody></table></div>
    <p class="muted small rv" style="margin-top:12px">Lokasi diperoleh dari irisan batas tile dengan peta batas desa/kelurahan (pembaruan 13 Juni 2023). Desa/kelurahan yang mencakup kurang dari 10% luas tile tidak dicantumkan; persentase menunjukkan porsi luas tile. Sekitar 34% luas tile 00000065 berupa perairan Teluk Palu. Segmen = jumlah petak <em>ground truth</em> (total 3.271).</p>
  </div>
</section>

'''

p = ROOT / "web" / "metode.html"
s = p.read_text(encoding="utf-8")
if 'id="lokasi"' not in s:
    anchor = '<section>\n  <div class="wrap grid g2" style="gap:56px;align-items:start">'
    assert anchor in s, "jangkar seksi blok spasial tidak ditemukan"
    s = s.replace(anchor, SEKSI + anchor, 1)
    p.write_text(s, encoding="utf-8")
    print("ditambahkan: seksi lokasi 18 tile di metode.html")

# ------------------------------------------------------------------ 2. sisa diksi pada teks tampilan
ganti_berkas("web/metode.html", [
    ("dan integrasi <em>end-to-end</em> (Tujuan 3).", f"dan model {M} (Tujuan 3)."),
    ("Metrik piksel dan instans,", "Metrik tingkat piksel dan segmen,"),
    ("jaring pengaman bagi bentuk kerusakan lain.", "penangkap perubahan umum bagi bentuk kerusakan lain."),
    ("IoU tingkat piksel dan instans (pencocokan", "IoU tingkat piksel dan segmen (pencocokan"),
])
ganti_berkas("web/index.html", [
    ("F1 tingkat instans segmentasi", "F1 tingkat segmen"),
])

p = ROOT / "web" / "assets" / "data" / "data.js"
s = p.read_text(encoding="utf-8")
i = s.index("window.DATA = ")
data = json.loads(s[i + len("window.DATA = "):].rstrip().rstrip(";"))
n = [0]


def ubah(t):
    baru = re.sub(r"\binstans\b", "segmen", t)
    baru = re.sub(r"\bInstans\b", "Segmen", baru)
    if baru != t:
        n[0] += 1
    return baru


def jalan(o):
    if isinstance(o, dict):
        return {k: jalan(v) for k, v in o.items()}          # kunci tidak diubah
    if isinstance(o, list):
        return [jalan(v) for v in o]
    if isinstance(o, str):
        return ubah(o)
    return o


data = jalan(data)
p.write_text(s[:i] + "window.DATA = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
print(f"data.js: {n[0]} teks 'instans' -> 'segmen'")
