/* Konfigurasi situs — satu tempat untuk tautan dan identitas. */
window.CONFIG = {
  judul: "Penilaian Kerusakan Lahan Pertanian Terdampak Bencana",
  judulPendek: "Lahan Terdampak",
  penulis: "Rafliansyah Dwi Setiawan Tondau",
  nim: "222212827",
  pembimbing: "Dr. Eng. Arie Wahyu Wijayanto, S.S.T., M.T.",
  kampus: "Politeknik Statistika STIS",
  prodi: "D-IV Komputasi Statistik, peminatan Sains Data",
  tahun: 2026,
  // Hugging Face Space (backend demo unggah) dan dataset contoh citra
  spaceId: "ZaXira/lahan-pertanian-terdampak",
  spaceUrl: "https://huggingface.co/spaces/ZaXira/lahan-pertanian-terdampak",
  datasetUrl: "https://huggingface.co/datasets/ZaXira/palu-tsunami-lahan-pertanian",
  datasetFile: (tile, fase) =>
    `https://huggingface.co/datasets/ZaXira/palu-tsunami-lahan-pertanian/resolve/main/tif/palu-tsunami_${tile}_${fase}_disaster.tif`,
  resolusiPalu: 0.4984
};
