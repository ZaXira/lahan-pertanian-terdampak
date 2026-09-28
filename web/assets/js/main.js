/* Komponen bersama: navigasi, footer, tema, reveal, slider pembanding, lightbox, tabel. */
(function () {
  const C = window.CONFIG;
  const halaman = document.body.dataset.page || "";
  if (new URLSearchParams(location.search).has("shot")) document.documentElement.classList.add("shot");  // uji tangkapan layar

  /* ---------- ikon (Phosphor, dimuat di <head>) ---------- */
  const IK = { sun: '<i class="ph ph-sun" aria-hidden="true"></i>', moon: '<i class="ph ph-moon" aria-hidden="true"></i>',
    menu: '<i class="ph ph-list" aria-hidden="true"></i>', x: '<i class="ph ph-x" aria-hidden="true"></i>' };

  /* ---------- lewati ke isi ---------- */
  const main = document.querySelector("main");
  if (main) main.id = main.id || "isi";
  const skip = document.createElement("a");
  skip.className = "skip"; skip.href = "#isi"; skip.textContent = "Langsung ke isi";
  document.body.prepend(skip);

  /* ---------- navigasi ---------- */
  const MENU = [
    ["index.html", "Beranda", "beranda"], ["metode.html", "Metode", "metode"], ["hasil.html", "Hasil", "hasil"],
    ["demo.html", "Demo Galeri", "demo"], ["unggah.html", "Coba Citra Sendiri", "unggah"]
  ];
  const nav = document.createElement("header");
  nav.className = "nav";
  nav.innerHTML = `<div class="wrap">
      <a class="brand" href="index.html"><img src="assets/img/logo-stis.png" alt="Logo Politeknik Statistika STIS">
        <span>${C.judulPendek}<small>Studi kasus Tsunami Palu 2018</small></span></a>
      <button class="icon-btn burger" aria-label="Buka menu" aria-expanded="false">${IK.menu}</button>
      <ul class="menu">${MENU.map(([h, t, k]) => `<li><a href="${h}"${k === halaman ? ' aria-current="page"' : ""}>${t}</a></li>`).join("")}
        <li><button class="icon-btn theme" aria-label="Ganti tema terang/gelap"></button></li></ul>
    </div>`;
  skip.after(nav);
  const burger = nav.querySelector(".burger"), menu = nav.querySelector(".menu");
  burger.addEventListener("click", () => {
    const buka = menu.classList.toggle("open");
    burger.setAttribute("aria-expanded", String(buka));
    burger.innerHTML = buka ? IK.x : IK.menu;
  });

  /* ---------- tema ---------- */
  const root = document.documentElement, tb = nav.querySelector(".theme");
  const gelap = () => root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
  try { const s = localStorage.getItem("tema"); if (s) root.dataset.theme = s; } catch (e) { /* tanpa storage */ }
  const ikonTema = () => { tb.innerHTML = gelap() ? IK.sun : IK.moon; };
  ikonTema();
  tb.addEventListener("click", () => {
    root.dataset.theme = gelap() ? "light" : "dark";
    try { localStorage.setItem("tema", root.dataset.theme); } catch (e) { /* abaikan */ }
    ikonTema();
    document.dispatchEvent(new CustomEvent("tema"));
  });

  /* ---------- footer ---------- */
  const ft = document.createElement("footer");
  ft.innerHTML = `<div class="wrap"><div class="cols">
      <div><div class="id"><img class="logo-inv" src="assets/img/logo-stis.png" alt="">
        <div><h4>${C.judul}</h4><p class="small" style="margin:0">Studi kasus Tsunami Palu 2018. Skripsi ${C.prodi}, ${C.kampus}, ${C.tahun}.</p></div></div></div>
      <div><h4>Penulis</h4><ul class="small"><li>${C.penulis}</li><li>NIM ${C.nim}</li>
        <li style="margin-top:6px">Pembimbing:<br>${C.pembimbing}</li></ul></div>
      <div><h4>Tautan</h4><ul class="small">
        <li><a href="${C.spaceUrl}" target="_blank" rel="noopener">Aplikasi di Hugging Face Spaces</a></li>
        <li><a href="${C.datasetUrl}" target="_blank" rel="noopener">Contoh citra GeoTIFF (dataset)</a></li>
        <li><a href="https://xview2.org" target="_blank" rel="noopener">Sumber citra: xBD / xView2</a></li></ul></div>
    </div>
    <div class="fine">Citra: xBD (Gupta dkk., 2019), lisensi CC BY-NC-SA 4.0. Angka pada situs ini diambil langsung dari keluaran resmi penelitian.
      Hasil model bersifat indikatif dan perlu verifikasi lapangan sebelum dipakai sebagai dasar keputusan.</div></div>`;
  document.body.append(ft);

  /* ---------- reveal ---------- */
  const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }),
    { rootMargin: "0px 0px -8% 0px" });
  document.querySelectorAll(".rv").forEach((el) => {
    const sib = [...el.parentElement.children].filter((x) => x.classList.contains("rv"));
    if (sib.length > 1) el.style.setProperty("--i", Math.min(sib.indexOf(el), 5));   // muncul berurutan
    io.observe(el);
  });

  /* ---------- slider pembanding ---------- */
  window.pasangCompare = function (el) {
    const r = el.querySelector("input[type=range]");
    const set = () => el.style.setProperty("--pos", r.value + "%");
    r.addEventListener("input", set); set();
  };
  document.querySelectorAll(".compare").forEach(window.pasangCompare);

  /* ---------- lightbox ---------- */
  const lb = document.createElement("div");
  lb.className = "lb"; lb.setAttribute("role", "dialog"); lb.setAttribute("aria-label", "Pratinjau gambar");
  lb.innerHTML = `<img alt=""><button class="icon-btn" aria-label="Tutup">${IK.x}</button>`;
  document.body.append(lb);
  const tutup = () => lb.classList.remove("open");
  lb.addEventListener("click", tutup);
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") tutup(); });
  window.bukaGambar = (src, alt) => { lb.querySelector("img").src = src; lb.querySelector("img").alt = alt || ""; lb.classList.add("open"); };
  document.addEventListener("click", (e) => {
    const t = e.target.closest("[data-zoom]");
    if (t) { e.preventDefault(); window.bukaGambar(t.dataset.zoom || t.currentSrc || t.src, t.alt); }
  });

  /* ---------- format teks & angka ---------- */
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  window.md = (s) => esc(s).replace(/`([^`]+)`/g, "<code>$1</code>").replace(/\*\*(.+?)\*\*/g, "<b>$1</b>").replace(/\*([^*]+)\*/g, "<em>$1</em>");
  window.fmt = (x, d = 4) => Number(x).toLocaleString("id-ID", { minimumFractionDigits: d, maximumFractionDigits: d });

  /* ---------- tabel dari data resmi ---------- */
  window.tabel = function (kode, opsi = {}) {
    const T = window.DATA.tabel[kode];
    const kiri = new Set(opsi.kiri || [0]);
    let h = `<div class="table-wrap"><table class="data"><caption>${md(opsi.judul || T.judul)}</caption><thead>`;
    T.kepala.forEach((baris) => {
      h += "<tr>" + baris.map(([t, cs, rs]) => `<th colspan="${cs}" rowspan="${rs}">${md(t)}</th>`).join("") + "</tr>";
    });
    h += "</thead><tbody>";
    T.rows.forEach((r, i) => {
      if (T.panel.includes(i)) { h += `<tr class="panel"><td colspan="${r.length}">${md(r[0].replace(/^§/, ""))}</td></tr>`; return; }
      h += `<tr${T.tebal.includes(i) ? ' class="b"' : ""}>` + r.map((c, j) => `<td${kiri.has(j) ? ' class="l"' : ""}>${md(c)}</td>`).join("") + "</tr>";
    });
    h += "</tbody></table>";
    if (T.keterangan && !opsi.tanpaKet) h += `<p class="tnote">${md(T.keterangan)}</p>`;
    return h + "</div>";
  };
  document.querySelectorAll("[data-tabel]").forEach((el) => {
    el.innerHTML = window.tabel(el.dataset.tabel, { kiri: (el.dataset.kiri || "0").split(",").map(Number) });
  });

  /* ---------- tab ---------- */
  document.querySelectorAll(".tabs").forEach((tabs) => {
    const btn = [...tabs.querySelectorAll(".tab")];
    btn.forEach((b) => b.addEventListener("click", () => {
      btn.forEach((x) => { x.setAttribute("aria-selected", String(x === b)); document.getElementById(x.dataset.pane).hidden = x !== b; });
      document.dispatchEvent(new CustomEvent("tab", { detail: b.dataset.pane }));
    }));
  });

  /* ---------- warna grafik mengikuti tema ---------- */
  window.warna = () => {
    const cs = getComputedStyle(root);
    const v = (n) => cs.getPropertyValue(n).trim();
    return { ink: v("--ink-2"), line: v("--line"), accent: v("--accent"), s2: v("--series-2"), s3: v("--series-3"),
      none: v("--cls-none"), mid: v("--cls-mid"), sev: v("--cls-sev"), font: v("--font-body") };
  };
})();
