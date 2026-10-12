/* Konfigurasi situs — satu tempat untuk tautan dan identitas. */
window.CONFIG = {
  judul: "Penilaian Kerusakan Lahan Pertanian Terdampak Bencana",
  judulPendek: "Lahan Terdampak",
  judulLengkap: "PENILAIAN KERUSAKAN LAHAN PERTANIAN TERDAMPAK BENCANA MENGGUNAKAN CITRA SATELIT RESOLUSI SANGAT TINGGI DENGAN METODE DEEP LEARNING DAN MACHINE LEARNING (Studi Kasus: Bencana Palu Tahun 2018)",
  penulis: "Rafliansyah Dwi Setiawan Tondau",
  nim: "222212827",
  pembimbing: "Dr. Eng. Arie W. Wijayanto, S.S.T., M.T.",
  kampus: "Politeknik Statistika STIS",
  prodi: "D-IV Komputasi Statistik, peminatan Sains Data",
  tahun: 2026,
  tahunLulus: 2026,
  // Hugging Face Space (backend demo unggah) dan dataset contoh citra
  spaceId: "ZaXira/lahan-pertanian-terdampak",
  spaceUrl: "https://huggingface.co/spaces/ZaXira/lahan-pertanian-terdampak",
  datasetUrl: "https://huggingface.co/datasets/ZaXira/palu-tsunami-lahan-pertanian",
  datasetFile: (tile, fase) =>
    `https://huggingface.co/datasets/ZaXira/palu-tsunami-lahan-pertanian/resolve/main/tif/palu-tsunami_${tile}_${fase}_disaster.tif`,
  // Login "Masuk dengan Hugging Face" (OAuth app di huggingface.co/settings/applications).
  // Kosong = tombol login disembunyikan.
  hfOauthClientId: "fd0a6d91-3022-483b-972b-71ef0c74494b",
  hfOauthScopes: "openid profile inference-api",
  githubUrl: "https://github.com/ZaXira/lahan-pertanian-terdampak",
  resolusiPalu: 0.4984
};
