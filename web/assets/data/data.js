/* Dibangkitkan otomatis oleh tools/bangun_aset.py dari data resmi penelitian — jangan disunting manual. */
window.DATA = {
 "tabel": {
  "T4.1.a": {
   "judul": "Kinerja YOLOv8-seg dan Mask R-CNN pada data uji (rerata makro 4 *tile*)",
   "kepala": [
    [
     [
      "Model",
      1,
      2
     ],
     [
      "Tingkat piksel",
      4,
      1
     ],
     [
      "Tingkat instans",
      4,
      1
     ]
    ],
    [
     [
      "IoU",
      1,
      1
     ],
     [
      "*Precision*",
      1,
      1
     ],
     [
      "*Recall*",
      1,
      1
     ],
     [
      "F1",
      1,
      1
     ],
     [
      "IoU",
      1,
      1
     ],
     [
      "*Precision*",
      1,
      1
     ],
     [
      "*Recall*",
      1,
      1
     ],
     [
      "F1",
      1,
      1
     ]
    ]
   ],
   "rows": [
    [
     "YOLOv8-seg",
     "0,5399",
     "0,7643",
     "0,6748",
     "0,6963",
     "0,7492",
     "0,6092",
     "0,5943",
     "0,5973"
    ],
    [
     "Mask R-CNN",
     "0,5702",
     "0,8737",
     "0,6467",
     "0,7178",
     "0,8421",
     "0,8131",
     "0,5813",
     "0,6589"
    ]
   ],
   "keterangan": "Setiap nilai merupakan rerata makro dari empat *tile* uji (00000163, 00000169, 00000184, 00000195). Tingkat instans memakai pencocokan Hungarian dengan IoU ≥ 0,5.",
   "tebal": [],
   "panel": []
  },
  "T4.1.b": {
   "judul": "Kinerja YOLOv8-seg dan Mask R-CNN per *tile* uji dan gabungan mikro",
   "kepala": [
    [
     [
      "*Tile*",
      1,
      2
     ],
     [
      "n_pred",
      1,
      2
     ],
     [
      "n_GT",
      1,
      2
     ],
     [
      "TP",
      1,
      2
     ],
     [
      "Tingkat instans",
      3,
      1
     ],
     [
      "F1 piksel",
      1,
      2
     ],
     [
      "Segmen dilewati",
      1,
      2
     ]
    ],
    [
     [
      "*Precision*",
      1,
      1
     ],
     [
      "*Recall*",
      1,
      1
     ],
     [
      "F1",
      1,
      1
     ]
    ]
   ],
   "rows": [
    [
     "§YOLOv8-seg (*fold* 2)",
     "",
     "",
     "",
     "",
     "",
     "",
     "",
     ""
    ],
    [
     "00000163",
     "109",
     "113",
     "68",
     "0,6239",
     "0,6018",
     "0,6126",
     "0,5775",
     "9"
    ],
    [
     "00000169",
     "137",
     "155",
     "94",
     "0,6861",
     "0,6065",
     "0,6438",
     "0,7371",
     "20"
    ],
    [
     "00000184",
     "195",
     "243",
     "109",
     "0,5590",
     "0,4486",
     "0,4977",
     "0,6749",
     "55"
    ],
    [
     "00000195",
     "118",
     "93",
     "67",
     "0,5678",
     "0,7204",
     "0,6351",
     "0,7956",
     "22"
    ],
    [
     "Gabungan (mikro)",
     "559",
     "604",
     "338",
     "0,6047",
     "0,5596",
     "0,5813",
     "–",
     "106"
    ],
    [
     "§Mask R-CNN (*fold* 3)",
     "",
     "",
     "",
     "",
     "",
     "",
     "",
     ""
    ],
    [
     "00000163",
     "89",
     "113",
     "66",
     "0,7416",
     "0,5841",
     "0,6535",
     "0,6921",
     "–"
    ],
    [
     "00000169",
     "100",
     "155",
     "87",
     "0,8700",
     "0,5613",
     "0,6824",
     "0,7327",
     "–"
    ],
    [
     "00000184",
     "103",
     "243",
     "96",
     "0,9320",
     "0,3951",
     "0,5549",
     "0,5791",
     "–"
    ],
    [
     "00000195",
     "103",
     "93",
     "73",
     "0,7087",
     "0,7849",
     "0,7449",
     "0,8675",
     "–"
    ],
    [
     "Gabungan (mikro)",
     "395",
     "604",
     "322",
     "0,8152",
     "0,5331",
     "0,6446",
     "–",
     "–"
    ]
   ],
   "keterangan": "n_pred = jumlah segmen prediksi yang dievaluasi; n_GT = jumlah segmen *ground truth*; TP = pasangan dengan IoU ≥ 0,5. Baris gabungan (mikro) menjumlahkan TP, n_pred, dan n_GT keempat *tile* sebelum *precision*, *recall*, dan F1 dihitung (angka turunan). F1 piksel tidak dapat diagregasi mikro dari berkas yang tersedia (–). Segmen dilewati = segmen prediksi YOLOv8-seg yang geometrinya tidak dapat diperbaiki `safe_geometry`; segmen ini dibuang sebelum evaluasi dan tidak termasuk dalam n_pred.",
   "tebal": [
    5,
    11
   ],
   "panel": [
    0,
    6
   ]
  },
  "T4.1.c": {
   "judul": "Hasil *cross-validation* 4-*fold* YOLOv8-seg dan Mask R-CNN",
   "kepala": [
    [
     [
      "*Fold*",
      1,
      2
     ],
     [
      "*Tile* validasi terpadat (segmen)",
      1,
      2
     ],
     [
      "YOLOv8-seg",
      4,
      1
     ],
     [
      "Mask R-CNN",
      2,
      1
     ]
    ],
    [
     [
      "mAP50 *mask*",
      1,
      1
     ],
     [
      "mAP50-95 *mask*",
      1,
      1
     ],
     [
      "*Epoch* berhenti (terbaik)",
      1,
      1
     ],
     [
      "Durasi (detik)",
      1,
      1
     ],
     [
      "AP *mask*",
      1,
      1
     ],
     [
      "Durasi (detik)",
      1,
      1
     ]
    ]
   ],
   "rows": [
    [
     "0",
     "00000117 (511)",
     "0,2524",
     "0,0805",
     "75 (60)",
     "295,7",
     "10,80",
     "484,7"
    ],
    [
     "1",
     "00000065 (433)",
     "0,5073",
     "0,2056",
     "100 (92)",
     "336,4",
     "18,36",
     "468,9"
    ],
    [
     "2",
     "00000193 (268)",
     "0,5304",
     "0,2310",
     "75 (60)",
     "271,7",
     "30,42",
     "466,8"
    ],
    [
     "3",
     "00000189 (216)",
     "0,0001",
     "< 0,0001",
     "16 (1)",
     "75,0",
     "32,89",
     "464,7"
    ],
    [
     "Total durasi",
     "",
     "",
     "",
     "",
     "978,8",
     "",
     "1.885,1"
    ]
   ],
   "keterangan": "mAP50 dan mAP50-95 *mask* YOLOv8-seg berasal dari Ultralytics (rentang 0–1); AP *mask* Mask R-CNN berasal dari evaluator COCO detectron2 (rerata IoU 0,50–0,95, rentang 0–100), sehingga kedua kolom tidak dapat dibandingkan secara langsung. *Epoch* terbaik ditentukan dari `results.csv` (nilai *fitness* tertinggi). *Tile* validasi terpadat dan jumlah segmennya mengacu pada Tabel 3.4 dan Tabel 3.15. *Fold* yang diuji pada data uji: YOLOv8-seg *fold* 2, Mask R-CNN *fold* 3.",
   "tebal": [
    4
   ],
   "panel": []
  },
  "T4.2.a": {
   "judul": "Hasil *hyperparameter tuning* Random Forest dan LightGBM",
   "kepala": [
    [
     [
      "Model",
      1,
      1
     ],
     [
      "Ruang pencarian",
      1,
      1
     ],
     [
      "*Hyperparameter* terbaik",
      1,
      1
     ],
     [
      "F1-*macro cross-validation*",
      1,
      1
     ],
     [
      "Durasi (detik)",
      1,
      1
     ]
    ]
   ],
   "rows": [
    [
     "Random Forest",
     "`min_samples_leaf` ∈ {1, 2, 4, 8}; `max_depth` ∈ {None, 8, 12, 16} (16 kombinasi)",
     "`max_depth` = 8; `min_samples_leaf` = 1",
     "0,5539",
     "48,6"
    ],
    [
     "LightGBM",
     "`num_leaves` ∈ {15, 31, 63}; `min_child_samples` ∈ {5, 10, 20}; `max_depth` ∈ {−1, 6, 10} (27 kombinasi)",
     "`max_depth` = 10; `min_child_samples` = 10; `num_leaves` = 15",
     "0,5346",
     "56,2"
    ]
   ],
   "keterangan": "Penyetelan memakai `GridSearchCV` dengan `PredefinedSplit` 5-*fold* (kolom `cv_fold`) hanya pada data latih (n = 2.176) dan *scoring* F1-*macro*. Kedua model memakai 300 pohon; Random Forest dengan `class_weight='balanced_subsample'` dan LightGBM dengan `class_weight='balanced'`.",
   "tebal": [],
   "panel": []
  },
  "T4.2.b": {
   "judul": "Kinerja Random Forest dan LightGBM pada data validasi dan data uji",
   "kepala": [
    [
     [
      "Data",
      1,
      1
     ],
     [
      "Model",
      1,
      1
     ],
     [
      "Akurasi",
      1,
      1
     ],
     [
      "F1-*macro*",
      1,
      1
     ],
     [
      "*Precision*-*macro*",
      1,
      1
     ],
     [
      "*Recall*-*macro*",
      1,
      1
     ],
     [
      "κ tertimbang kuadratik",
      1,
      1
     ]
    ]
   ],
   "rows": [
    [
     "Validasi (n = 491)",
     "Random Forest",
     "0,6578",
     "0,5336",
     "0,5335",
     "0,5872",
     "0,4219"
    ],
    [
     "",
     "LightGBM",
     "0,7088",
     "0,5535",
     "0,5474",
     "0,5651",
     "0,4166"
    ],
    [
     "Uji (n = 604)",
     "Random Forest",
     "0,6639",
     "0,4903",
     "0,5467",
     "0,5069",
     "0,5556"
    ],
    [
     "",
     "LightGBM",
     "0,6507",
     "0,4849",
     "0,5228",
     "0,5063",
     "0,4566"
    ]
   ],
   "keterangan": "κ = Cohen's Kappa tertimbang kuadratik (Persamaan 2.21–2.22). Metrik utama Tujuan 2 adalah F1-*macro* dan κ; akurasi hanya pelengkap karena data uji timpang.",
   "tebal": [],
   "panel": []
  },
  "T4.2.c": {
   "judul": "*Precision*, *recall*, dan F1 per kelas pada data validasi dan data uji",
   "kepala": [
    [
     [
      "Kelas",
      1,
      2
     ],
     [
      "Data validasi",
      4,
      1
     ],
     [
      "Data uji",
      4,
      1
     ]
    ],
    [
     [
      "n (%)",
      1,
      1
     ],
     [
      "*Precision*",
      1,
      1
     ],
     [
      "*Recall*",
      1,
      1
     ],
     [
      "F1",
      1,
      1
     ],
     [
      "n (%)",
      1,
      1
     ],
     [
      "*Precision*",
      1,
      1
     ],
     [
      "*Recall*",
      1,
      1
     ],
     [
      "F1",
      1,
      1
     ]
    ]
   ],
   "rows": [
    [
     "§Random Forest",
     "",
     "",
     "",
     "",
     "",
     "",
     "",
     ""
    ],
    [
     "Tidak Terdampak",
     "89 (18,1%)",
     "0,4824",
     "0,4607",
     "0,4713",
     "306 (50,7%)",
     "0,9026",
     "0,4542",
     "0,6043"
    ],
    [
     "Terdampak Sedang",
     "48 (9,8%)",
     "0,2393",
     "0,5833",
     "0,3394",
     "30 (5,0%)",
     "0,0375",
     "0,1000",
     "0,0545"
    ],
    [
     "Terdampak Berat",
     "354 (72,1%)",
     "0,8789",
     "0,7175",
     "0,7900",
     "268 (44,4%)",
     "0,7000",
     "0,9664",
     "0,8119"
    ],
    [
     "§LightGBM",
     "",
     "",
     "",
     "",
     "",
     "",
     "",
     ""
    ],
    [
     "Tidak Terdampak",
     "89 (18,1%)",
     "0,5116",
     "0,4944",
     "0,5029",
     "306 (50,7%)",
     "0,8503",
     "0,4641",
     "0,6004"
    ],
    [
     "Terdampak Sedang",
     "48 (9,8%)",
     "0,2923",
     "0,3958",
     "0,3363",
     "30 (5,0%)",
     "0,0800",
     "0,1333",
     "0,1000"
    ],
    [
     "Terdampak Berat",
     "354 (72,1%)",
     "0,8382",
     "0,8051",
     "0,8213",
     "268 (44,4%)",
     "0,6382",
     "0,9216",
     "0,7542"
    ]
   ],
   "keterangan": "*Precision* dan *recall* per kelas diturunkan dari *confusion matrix* pada `training_log.json`; F1 per kelas identik dengan nilai resmi. n (%) = jumlah dan proporsi segmen aktual per kelas (Tabel 3.16); proporsi pada data latih: Tidak Terdampak 18,0%, Terdampak Sedang 9,8%, Terdampak Berat 72,2%.",
   "tebal": [],
   "panel": [
    0,
    4
   ]
  },
  "T4.2.d": {
   "judul": "*Confusion matrix* Random Forest dan LightGBM pada data uji",
   "kepala": [
    [
     [
      "Kelas aktual",
      1,
      2
     ],
     [
      "Prediksi Random Forest",
      3,
      1
     ],
     [
      "Jumlah aktual",
      1,
      2
     ],
     [
      "Prediksi LightGBM",
      3,
      1
     ]
    ],
    [
     [
      "TT",
      1,
      1
     ],
     [
      "TS",
      1,
      1
     ],
     [
      "TB",
      1,
      1
     ],
     [
      "TT",
      1,
      1
     ],
     [
      "TS",
      1,
      1
     ],
     [
      "TB",
      1,
      1
     ]
    ]
   ],
   "rows": [
    [
     "Tidak Terdampak",
     "139",
     "72",
     "95",
     "306",
     "142",
     "39",
     "125"
    ],
    [
     "Terdampak Sedang",
     "11",
     "3",
     "16",
     "30",
     "11",
     "4",
     "15"
    ],
    [
     "Terdampak Berat",
     "4",
     "5",
     "259",
     "268",
     "14",
     "7",
     "247"
    ],
    [
     "Jumlah prediksi",
     "154",
     "80",
     "370",
     "604",
     "167",
     "50",
     "387"
    ]
   ],
   "keterangan": "Baris = kelas aktual, kolom = kelas prediksi. TT = Tidak Terdampak; TS = Terdampak Sedang; TB = Terdampak Berat. Baris jumlah prediksi merupakan angka turunan (jumlah kolom).",
   "tebal": [
    3
   ],
   "panel": []
  },
  "T4.2.e": {
   "judul": "*Feature importance* Random Forest dan LightGBM",
   "kepala": [
    [
     [
      "*Layer* fitur",
      1,
      2
     ],
     [
      "Random Forest",
      2,
      1
     ],
     [
      "LightGBM",
      3,
      1
     ]
    ],
    [
     [
      "*Gini importance*",
      1,
      1
     ],
     [
      "*Permutation* (rerata ± SB)",
      1,
      1
     ],
     [
      "Frekuensi *split*",
      1,
      1
     ],
     [
      "Proporsi *split*",
      1,
      1
     ],
     [
      "*Permutation* (rerata ± SB)",
      1,
      1
     ]
    ]
   ],
   "rows": [
    [
     "Batas lahan",
     "0,2193",
     "0,0474 ± 0,0201",
     "4.138",
     "0,3284",
     "0,0915 ± 0,0244"
    ],
    [
     "Material asing",
     "0,1523",
     "0,0583 ± 0,0187",
     "1.774",
     "0,1408",
     "0,0627 ± 0,0163"
    ],
    [
     "Kehilangan tanaman",
     "0,1005",
     "0,0253 ± 0,0130",
     "1.159",
     "0,0920",
     "0,0305 ± 0,0164"
    ],
    [
     "Perubahan radiometri",
     "0,1913",
     "0,0415 ± 0,0108",
     "3.919",
     "0,3110",
     "0,0486 ± 0,0185"
    ],
    [
     "Genangan baru",
     "0,1617",
     "0,0581 ± 0,0134",
     "792",
     "0,0629",
     "0,0524 ± 0,0160"
    ],
    [
     "Perubahan semantik (SAC)",
     "0,1749",
     "0,0370 ± 0,0192",
     "818",
     "0,0649",
     "0,0448 ± 0,0164"
    ]
   ],
   "keterangan": "*Gini importance* dihitung dari data latih; *permutation importance* diukur pada data validasi (n = 491) dengan 20 ulangan dan *scoring* F1-*macro*; SB = simpangan baku antarulangan. Frekuensi *split* adalah *importance* bawaan LightGBM (jumlah pemakaian fitur sebagai pemisah), bukan *Gini importance*; proporsi *split* = frekuensi *split* dibagi totalnya (12.600), dihitung untuk penyajian.",
   "tebal": [],
   "panel": []
  },
  "T4.3.b": {
   "judul": "Hasil segmentasi model Mask R-CNN–RF (Tujuan 3) dibandingkan dengan Mask R-CNN Tujuan 1 pada basis yang sama",
   "kepala": [
    [
     [
      "Komponen",
      1,
      1
     ],
     [
      "*Tile* 00000163",
      1,
      1
     ],
     [
      "*Tile* 00000169",
      1,
      1
     ],
     [
      "*Tile* 00000184",
      1,
      1
     ],
     [
      "*Tile* 00000195",
      1,
      1
     ],
     [
      "Gabungan (mikro)",
      1,
      1
     ]
    ]
   ],
   "rows": [
    [
     "n_GT",
     "113",
     "155",
     "243",
     "93",
     "604"
    ],
    [
     "§Tujuan 1 (Mask R-CNN, `DETECTIONS_PER_IMAGE` = 100, jalur JPG)",
     "",
     "",
     "",
     "",
     ""
    ],
    [
     "Jumlah prediksi",
     "89",
     "100",
     "103",
     "103",
     "395"
    ],
    [
     "TP",
     "66",
     "87",
     "96",
     "73",
     "322"
    ],
    [
     "FP",
     "23",
     "13",
     "7",
     "30",
     "73"
    ],
    [
     "FN",
     "47",
     "68",
     "147",
     "20",
     "282"
    ],
    [
     "*Precision*",
     "0,7416",
     "0,8700",
     "0,9320",
     "0,7087",
     "0,8152"
    ],
    [
     "*Recall*",
     "0,5841",
     "0,5613",
     "0,3951",
     "0,7849",
     "0,5331"
    ],
    [
     "F1",
     "0,6535",
     "0,6824",
     "0,5549",
     "0,7449",
     "0,6446"
    ],
    [
     "§Tujuan 3 (Mask R-CNN, `DETECTIONS_PER_IMAGE` = 500, tanpa jalur JPG)",
     "",
     "",
     "",
     "",
     ""
    ],
    [
     "Jumlah prediksi",
     "92",
     "130",
     "189",
     "115",
     "526"
    ],
    [
     "TP",
     "67",
     "106",
     "147",
     "79",
     "399"
    ],
    [
     "FP",
     "25",
     "24",
     "42",
     "36",
     "127"
    ],
    [
     "FN",
     "46",
     "49",
     "96",
     "14",
     "205"
    ],
    [
     "*Precision*",
     "0,7283",
     "0,8154",
     "0,7778",
     "0,6870",
     "0,7586"
    ],
    [
     "*Recall*",
     "0,5929",
     "0,6839",
     "0,6049",
     "0,8495",
     "0,6606"
    ],
    [
     "F1",
     "0,6537",
     "0,7439",
     "0,6806",
     "0,7596",
     "0,7062"
    ],
    [
     "§Perubahan Tujuan 1 → Tujuan 3",
     "",
     "",
     "",
     "",
     ""
    ],
    [
     "Tambahan prediksi",
     "3",
     "30",
     "86",
     "12",
     "131"
    ],
    [
     "Tambahan TP",
     "1",
     "19",
     "51",
     "6",
     "77"
    ],
    [
     "Selisih *recall*",
     "+0,0088",
     "+0,1226",
     "+0,2099",
     "+0,0645",
     "+0,1275"
    ]
   ],
   "keterangan": "Kolom gabungan (mikro) dihitung dari jumlah TP, FP, dan FN keempat *tile*; untuk Tujuan 3 nilainya merupakan hasil resmi `summary_tujuan3.json`, untuk Tujuan 1 merupakan angka turunan. Nilai per *tile* Tujuan 1 adalah metrik instans per *tile* (rerata makronya disajikan pada Tabel 4.1). Selisih *recall* dihitung dari TP/n_GT tanpa pembulatan antara.",
   "tebal": [
    10,
    11,
    12,
    13,
    14,
    15,
    16
   ],
   "panel": [
    1,
    9,
    17
   ]
  },
  "T4.3.c2": {
   "judul": "*Recall* segmentasi model Mask R-CNN–RF menurut kuartil luas segmen *ground truth*",
   "kepala": [
    [
     [
      "Kuartil luas",
      1,
      1
     ],
     [
      "Rentang luas (m²)",
      1,
      1
     ],
     [
      "n_GT",
      1,
      1
     ],
     [
      "Terdeteksi (TP)",
      1,
      1
     ],
     [
      "*Recall* segmentasi",
      1,
      1
     ]
    ]
   ],
   "rows": [
    [
     "Q1 (terkecil)",
     "44–348",
     "151",
     "66",
     "0,4371"
    ],
    [
     "Q2",
     "349–591",
     "151",
     "112",
     "0,7417"
    ],
    [
     "Q3",
     "591–974",
     "151",
     "111",
     "0,7351"
    ],
    [
     "Q4 (terbesar)",
     "983–4.587",
     "151",
     "110",
     "0,7285"
    ]
   ],
   "keterangan": "Angka turunan (`data_turunan/ringkasan_deteksi_per_ukuran.csv`); luas segmen GT dihitung dengan shapely pada EPSG:32751. Keempat kuartil masing-masing memuat 151 segmen dari 604 segmen GT data uji.",
   "tebal": [],
   "panel": []
  },
  "T4.3.d": {
   "judul": "F1 Mask R-CNN–RF dibandingkan dengan Random Forest Tujuan 2 pada data uji",
   "kepala": [
    [
     [
      "Kelas",
      1,
      2
     ],
     [
      "Tujuan 2, uji penuh (n = 604)",
      3,
      1
     ],
     [
      "Tujuan 3, model Mask R-CNN–RF (n = 399)",
      3,
      1
     ],
     [
      "Selisih F1",
      1,
      2
     ]
    ],
    [
     [
      "*Precision*",
      1,
      1
     ],
     [
      "*Recall*",
      1,
      1
     ],
     [
      "F1",
      1,
      1
     ],
     [
      "*Precision*",
      1,
      1
     ],
     [
      "*Recall*",
      1,
      1
     ],
     [
      "F1",
      1,
      1
     ]
    ]
   ],
   "rows": [
    [
     "Tidak Terdampak",
     "0,9026",
     "0,4542",
     "0,6043",
     "0,8846",
     "0,3812",
     "0,5328",
     "−0,0715"
    ],
    [
     "Terdampak Sedang",
     "0,0375",
     "0,1000",
     "0,0545",
     "0,0357",
     "0,1176",
     "0,0548",
     "+0,0002"
    ],
    [
     "Terdampak Berat",
     "0,7000",
     "0,9664",
     "0,8119",
     "0,7283",
     "0,9602",
     "0,8283",
     "+0,0164"
    ],
    [
     "F1-*macro*",
     "",
     "",
     "0,4903",
     "",
     "",
     "0,4720",
     "−0,0183"
    ]
   ],
   "keterangan": "*Precision* dan *recall* per kelas diturunkan dari *confusion matrix*; F1 per kelas identik dengan nilai resmi. Selisih = F1 Tujuan 3 − F1 Tujuan 2, dihitung dari nilai tak terbulat. Segmen *false positive* (127) tidak termasuk dalam evaluasi F1 Mask R-CNN–RF.",
   "tebal": [
    3
   ],
   "panel": []
  },
  "T4.3.f": {
   "judul": "Komponen Skor gabungan xView2 dan mIoU model Mask R-CNN–RF",
   "kepala": [
    [
     [
      "Komponen",
      1,
      1
     ],
     [
      "Nilai",
      1,
      1
     ]
    ]
   ],
   "rows": [
    [
     "§Skor gabungan xView2 (Persamaan 2.23–2.24)",
     ""
    ],
    [
     "F1_segmentasi",
     "0,7062"
    ],
    [
     "F1 Mask R-CNN–RF: Tidak Terdampak",
     "0,5328"
    ],
    [
     "F1 Mask R-CNN–RF: Terdampak Sedang",
     "0,0548"
    ],
    [
     "F1 Mask R-CNN–RF: Terdampak Berat",
     "0,8283"
    ],
    [
     "F1 kerusakan (rerata harmonik)",
     "0,1406"
    ],
    [
     "Pembanding: rerata aritmetik (F1-*macro*)",
     "0,4720"
    ],
    [
     "Skor gabungan xView2 = 0,3 × F1_segmentasi + 0,7 × F1 kerusakan",
     "0,3103"
    ],
    [
     "§mIoU tingkat piksel (Persamaan 2.25–2.26)",
     ""
    ],
    [
     "IoU latar belakang",
     "0,7918"
    ],
    [
     "IoU Tidak Terdampak",
     "0,2496"
    ],
    [
     "IoU Terdampak Sedang",
     "0,0188"
    ],
    [
     "IoU Terdampak Berat",
     "0,5419"
    ],
    [
     "mIoU (rerata empat kelas)",
     "0,4005"
    ]
   ],
   "keterangan": "Seluruh nilai merupakan agregasi global (mikro) empat *tile* uji dari `summary_tujuan3.json`. mIoU dihitung pada tingkat piksel dengan kelas latar belakang, sehingga memuat pengaruh *false negative*, *false positive*, dan TP kelas salah sekaligus.",
   "tebal": [
    7,
    13
   ],
   "panel": [
    0,
    8
   ]
  },
  "T4.3.g": {
   "judul": "Kinerja klasifikasi dan komposisi kelas model Mask R-CNN–RF per *tile* uji",
   "kepala": [
    [
     [
      "Komponen",
      1,
      1
     ],
     [
      "*Tile* 00000163",
      1,
      1
     ],
     [
      "*Tile* 00000169",
      1,
      1
     ],
     [
      "*Tile* 00000184",
      1,
      1
     ],
     [
      "*Tile* 00000195",
      1,
      1
     ],
     [
      "Gabungan",
      1,
      1
     ]
    ]
   ],
   "rows": [
    [
     "§Klasifikasi pasangan TP",
     "",
     "",
     "",
     "",
     ""
    ],
    [
     "Pasangan TP",
     "67",
     "106",
     "147",
     "79",
     "399"
    ],
    [
     "TP kelas benar",
     "36",
     "53",
     "107",
     "68",
     "264"
    ],
    [
     "TP kelas salah",
     "31",
     "53",
     "40",
     "11",
     "135"
    ],
    [
     "Akurasi model Mask R-CNN–RF",
     "0,5373",
     "0,5000",
     "0,7279",
     "0,8608",
     "0,6617"
    ],
    [
     "§Komposisi kelas GT seluruh segmen (Tabel 3.4)",
     "",
     "",
     "",
     "",
     ""
    ],
    [
     "Tidak Terdampak",
     "77 (68,1%)",
     "88 (56,8%)",
     "129 (53,1%)",
     "12 (12,9%)",
     "306 (50,7%)"
    ],
    [
     "Terdampak Sedang",
     "2 (1,8%)",
     "10 (6,5%)",
     "12 (4,9%)",
     "6 (6,5%)",
     "30 (5,0%)"
    ],
    [
     "Terdampak Berat",
     "34 (30,1%)",
     "57 (36,8%)",
     "102 (42,0%)",
     "75 (80,6%)",
     "268 (44,4%)"
    ],
    [
     "§Komposisi kelas GT pasangan TP",
     "",
     "",
     "",
     "",
     ""
    ],
    [
     "Tidak Terdampak",
     "42 (62,7%)",
     "63 (59,4%)",
     "67 (45,6%)",
     "9 (11,4%)",
     "181 (45,4%)"
    ],
    [
     "Terdampak Sedang",
     "1 (1,5%)",
     "6 (5,7%)",
     "5 (3,4%)",
     "5 (6,3%)",
     "17 (4,3%)"
    ],
    [
     "Terdampak Berat",
     "24 (35,8%)",
     "37 (34,9%)",
     "75 (51,0%)",
     "65 (82,3%)",
     "201 (50,4%)"
    ],
    [
     "§*Recall* klasifikasi per kelas GT pada pasangan TP",
     "",
     "",
     "",
     "",
     ""
    ],
    [
     "Tidak Terdampak",
     "0,2857",
     "0,3175",
     "0,4776",
     "0,5556",
     "0,3812"
    ],
    [
     "Terdampak Sedang",
     "0,0000",
     "0,1667",
     "0,2000",
     "0,0000",
     "0,1176"
    ],
    [
     "Terdampak Berat",
     "1,0000",
     "0,8649",
     "0,9867",
     "0,9692",
     "0,9602"
    ],
    [
     "§*Recall* segmentasi per kelas GT",
     "",
     "",
     "",
     "",
     ""
    ],
    [
     "Tidak Terdampak",
     "0,5455",
     "0,7159",
     "0,5194",
     "0,7500",
     "0,5915"
    ],
    [
     "Terdampak Sedang",
     "0,5000",
     "0,6000",
     "0,4167",
     "0,8333",
     "0,5667"
    ],
    [
     "Terdampak Berat",
     "0,7059",
     "0,6491",
     "0,7353",
     "0,8667",
     "0,7500"
    ]
   ],
   "keterangan": "Hasil segmentasi per *tile* disajikan pada Tabel 4.10. Akurasi model Mask R-CNN–RF per *tile* dari `test_results_per_tile.csv`; jumlah TP kelas benar/salah, komposisi pasangan TP, dan *recall* per kelas diturunkan dari `match_all_4tile.csv`. *Recall* klasifikasi = pasangan yang kelasnya benar dibagi pasangan TP pada kelas GT yang sama; *recall* segmentasi = pasangan TP dibagi segmen GT pada kelas yang sama. Tanda – = tidak terdefinisi (penyebut nol).",
   "tebal": [],
   "panel": [
    0,
    5,
    9,
    13,
    17
   ]
  },
  "T4.3.i": {
   "judul": "Dekomposisi perubahan F1 per kelas dari Tujuan 2 ke model pembanding dan model Mask R-CNN–RF",
   "kepala": [
    [
     [
      "Kelas",
      1,
      2
     ],
     [
      "F1",
      3,
      1
     ],
     [
      "Selisih",
      3,
      1
     ]
    ],
    [
     [
      "Tujuan 2 uji penuh (n = 604)",
      1,
      1
     ],
     [
      "Model pembanding (n = 399, geometri GT)",
      1,
      1
     ],
     [
      "Model Mask R-CNN–RF (n = 399, geometri Mask R-CNN)",
      1,
      1
     ],
     [
      "Δ subset (model pembanding − Tujuan 2)",
      1,
      1
     ],
     [
      "Δ geometri (model Mask R-CNN–RF − model pembanding)",
      1,
      1
     ],
     [
      "Δ total (model Mask R-CNN–RF − Tujuan 2)",
      1,
      1
     ]
    ]
   ],
   "rows": [
    [
     "Tidak Terdampak",
     "0,6043",
     "0,5693",
     "0,5328",
     "−0,0351",
     "−0,0365",
     "−0,0715"
    ],
    [
     "Terdampak Sedang",
     "0,0545",
     "0,0588",
     "0,0548",
     "+0,0043",
     "−0,0040",
     "+0,0002"
    ],
    [
     "Terdampak Berat",
     "0,8119",
     "0,8423",
     "0,8283",
     "+0,0304",
     "−0,0140",
     "+0,0164"
    ],
    [
     "F1-*macro*",
     "0,4903",
     "0,4901",
     "0,4720",
     "−0,0001",
     "−0,0182",
     "−0,0183"
    ]
   ],
   "keterangan": "Seluruh selisih merupakan angka turunan yang dihitung dari *confusion matrix* tanpa pembulatan antara, sehingga dapat berbeda satu satuan digit terakhir dari selisih dua nilai yang sudah dibulatkan. Δ subset mengukur pengaruh penyempitan himpunan segmen (604 → 399) dengan geometri tetap GT; Δ geometri mengukur pengaruh penggantian geometri GT dengan geometri hasil deteksi.",
   "tebal": [
    3
   ],
   "panel": []
  },
  "T4.3.j": {
   "judul": "Estimasi jumlah dan luas lahan per kelas: *ground truth* dan model Mask R-CNN–RF",
   "kepala": [
    [
     [
      "Kelas",
      1,
      2
     ],
     [
      "*Ground truth*",
      2,
      1
     ],
     [
      "Prediksi model Mask R-CNN–RF",
      2,
      1
     ],
     [
      "Porsi dari *false positive*",
      2,
      1
     ],
     [
      "Selisih luas (ha)",
      1,
      2
     ]
    ],
    [
     [
      "Segmen",
      1,
      1
     ],
     [
      "Luas (ha)",
      1,
      1
     ],
     [
      "Segmen",
      1,
      1
     ],
     [
      "Luas (ha)",
      1,
      1
     ],
     [
      "Segmen",
      1,
      1
     ],
     [
      "Luas (ha)",
      1,
      1
     ]
    ]
   ],
   "rows": [
    [
     "Tidak Terdampak",
     "306",
     "21,81",
     "106",
     "7,13",
     "28",
     "1,31",
     "−14,68"
    ],
    [
     "Terdampak Sedang",
     "30",
     "2,89",
     "73",
     "4,26",
     "17",
     "0,74",
     "+1,37"
    ],
    [
     "Terdampak Berat",
     "268",
     "21,00",
     "347",
     "27,60",
     "82",
     "6,37",
     "+6,60"
    ],
    [
     "Jumlah",
     "604",
     "45,70",
     "526",
     "38,98",
     "127",
     "8,42",
     "−6,71"
    ]
   ],
   "keterangan": "Angka turunan (`data_turunan/ringkasan_luas_per_kelas.csv`), gabungan empat *tile* uji; luas dihitung dengan shapely pada EPSG:32751. Kelas prediksi model Mask R-CNN–RF meliputi seluruh 526 segmen (termasuk *false positive*). Luas prediksi dijumlahkan per segmen sehingga tumpang tindih antarprediksi terhitung ganda. Selisih = luas prediksi − luas GT. Luas ini tidak sebanding langsung dengan luas keluaran artefak web yang dihitung dari jumlah piksel × resolusi².",
   "tebal": [
    3
   ],
   "panel": []
  },
  "T4.3.k": {
   "judul": "Tipologi segmen *false positive model Mask R-CNN–RF*",
   "kepala": [
    [
     [
      "Tipologi",
      1,
      2
     ],
     [
      "n",
      1,
      2
     ],
     [
      "% dari FP",
      1,
      2
     ],
     [
      "Luas total (ha)",
      1,
      2
     ],
     [
      "Luas median (m²)",
      1,
      2
     ],
     [
      "Kelas prediksi",
      3,
      1
     ]
    ],
    [
     [
      "TT",
      1,
      1
     ],
     [
      "TS",
      1,
      1
     ],
     [
      "TB",
      1,
      1
     ]
    ]
   ],
   "rows": [
    [
     "Duplikat deteksi (IoU ≥ 0,5 dengan GT yang sudah berpasangan)",
     "2",
     "1,6%",
     "0,23",
     "1.169",
     "0",
     "0",
     "2"
    ],
    [
     "Di atas lahan GT (cakupan ≥ 50%, IoU < 0,5)",
     "97",
     "76,4%",
     "5,73",
     "513",
     "24",
     "12",
     "61"
    ],
    [
     "Sebagian di atas lahan GT (cakupan 10–50%)",
     "5",
     "3,9%",
     "0,45",
     "528",
     "2",
     "1",
     "2"
    ],
    [
     "Di luar lahan GT (cakupan < 10%)",
     "23",
     "18,1%",
     "2,00",
     "653",
     "2",
     "4",
     "17"
    ],
    [
     "Jumlah",
     "127",
     "100%",
     "8,42",
     "",
     "28",
     "17",
     "82"
    ]
   ],
   "keterangan": "Angka turunan (`data_turunan/ringkasan_tipologi_fp.csv`); cakupan = persentase luas segmen prediksi yang jatuh di atas segmen GT mana pun, dihitung dengan shapely pada EPSG:32751. Kolom kelas prediksi baris jumlah dari `match_all_4tile.csv`. TT = Tidak Terdampak; TS = Terdampak Sedang; TB = Terdampak Berat. \"Di luar lahan GT\" tidak otomatis berarti bukan lahan pertanian.",
   "tebal": [
    4
   ],
   "panel": []
  },
  "T4.4.a": {
   "judul": "Keluaran artefak web untuk *tile* 00000195 (jalur GeoTIFF)",
   "kepala": [
    [
     [
      "Kelas kerusakan",
      1,
      1
     ],
     [
      "Jumlah segmen",
      1,
      1
     ],
     [
      "Luas (ha)",
      1,
      1
     ]
    ]
   ],
   "rows": [
    [
     "Tidak Terdampak",
     "10",
     "0,7824"
    ],
    [
     "Terdampak Sedang",
     "7",
     "0,3673"
    ],
    [
     "Terdampak Berat",
     "98",
     "8,8604"
    ],
    [
     "Total",
     "115",
     "10,0101"
    ]
   ],
   "keterangan": "Dijalankan di Hugging Face Spaces (ZeroGPU, TF32 dimatikan). Luas dihitung dari jumlah piksel × resolusi² (0,4984 m/piksel dari metadata GeoTIFF).",
   "tebal": [
    3
   ],
   "panel": []
  },
  "T4.4.b": {
   "judul": "Waktu proses artefak web per tahap untuk *tile* 00000195 di ZeroGPU",
   "kepala": [
    [
     [
      "Tahap",
      1,
      1
     ],
     [
      "Waktu (detik)",
      1,
      1
     ]
    ]
   ],
   "rows": [
    [
     "1. Deteksi lahan pertanian (Mask R-CNN)",
     "2,6"
    ],
    [
     "2. Ekstraksi enam *layer* fitur",
     "18,8"
    ],
    [
     "3. Klasifikasi tingkat kerusakan (Random Forest)",
     "0,0"
    ],
    [
     "4. Perhitungan luas per kelas",
     "0,0"
    ],
    [
     "5. Visualisasi *overlay*",
     "0,2"
    ],
    [
     "Total (tercatat log)",
     "21,7"
    ]
   ],
   "keterangan": "Nilai per tahap dibulatkan satu desimal pada log aplikasi; jumlah kelima komponen (21,6 detik) berselisih 0,1 detik dari total tercatat akibat pembulatan per tahap. Tahap ekstraksi fitur didominasi SAM/AnyChange (*layer* 6).",
   "tebal": [
    5
   ],
   "panel": []
  },
  "T4.4.c": {
   "judul": "Validasi regresi artefak web terhadap hasil resmi Tujuan 3 (jalur GeoTIFF)",
   "kepala": [
    [
     [
      "*Tile*",
      1,
      1
     ],
     [
      "Segmen aplikasi/resmi",
      1,
      1
     ],
     [
      "Geometri identik",
      1,
      1
     ],
     [
      "`damage_pred` sama",
      1,
      1
     ]
    ]
   ],
   "rows": [
    [
     "00000163",
     "92/92",
     "92",
     "100,00%"
    ],
    [
     "00000169",
     "130/130",
     "130",
     "100,00%"
    ],
    [
     "00000184",
     "189/189",
     "189",
     "100,00%"
    ],
    [
     "00000195",
     "115/115",
     "115",
     "100,00%"
    ],
    [
     "Total",
     "526/526",
     "526",
     "100,00%"
    ]
   ],
   "keterangan": "Dijalankan di Kaggle GPU T4 (FP32) memakai modul aplikasi. Selisih maksimum keenam fitur `f_*_cont` = 0,00 poin persen (pembulatan dua desimal).",
   "tebal": [
    4
   ],
   "panel": []
  },
  "T4.4.d": {
   "judul": "Pengaruh cara penyiapan citra masukan terhadap keluaran artefak web (4 *tile*, 526 segmen resmi)",
   "kepala": [
    [
     [
      "Cara penyiapan citra",
      1,
      1
     ],
     [
      "Segmen ditemukan",
      1,
      1
     ],
     [
      "Kelas sama dengan hasil resmi",
      1,
      1
     ]
    ]
   ],
   "rows": [
    [
     "GeoTIFF 32-bit (tanpa konversi)",
     "526 (100%)",
     "526 (100%)"
    ],
    [
     "8-bit, normalisasi *min-max* gabungan tiga kanal",
     "509 (96,8%)",
     "469 (89,2%)"
    ],
    [
     "8-bit, peregangan persentil 2–98 per kanal",
     "212 (40,3%)",
     "199 (37,8%)"
    ]
   ],
   "keterangan": "Dijalankan di Kaggle GPU. Persentase terhadap 526 segmen hasil resmi Tujuan 3.",
   "tebal": [],
   "panel": []
  },
  "T4.4.e": {
   "judul": "Pengaruh pengaturan presisi aritmetik (TF32) terhadap keluaran *tile* 00000195",
   "kepala": [
    [
     [
      "Lingkungan",
      1,
      1
     ],
     [
      "Jumlah segmen",
      1,
      1
     ],
     [
      "Distribusi kelas (TT/TS/TB)",
      1,
      1
     ],
     [
      "Luas total (ha)",
      1,
      1
     ]
    ]
   ],
   "rows": [
    [
     "Kaggle GPU T4 (FP32)",
     "115",
     "10/7/98",
     "10,0105"
    ],
    [
     "ZeroGPU, TF32 aktif",
     "113",
     "10/5/98",
     "9,8783"
    ],
    [
     "ZeroGPU, TF32 dimatikan",
     "115",
     "10/7/98",
     "10,0101"
    ]
   ],
   "keterangan": "Jalur GeoTIFF. TT = Tidak Terdampak; TS = Terdampak Sedang; TB = Terdampak Berat. GPU ZeroGPU berarsitektur Blackwell; T4 tidak mendukung TF32 sehingga selalu FP32.",
   "tebal": [],
   "panel": []
  },
  "T4.5.b": {
   "judul": "Keterbatasan penelitian, pengaruhnya terhadap hasil, dan penanganannya",
   "kepala": [
    [
     [
      "Aspek",
      1,
      1
     ],
     [
      "Keterbatasan",
      1,
      1
     ],
     [
      "Pengaruh terhadap hasil",
      1,
      1
     ],
     [
      "Penanganan dalam penelitian ini",
      1,
      1
     ]
    ]
   ],
   "rows": [
    [
     "Data dan label",
     "18 *tile* dari satu kejadian; pelabelan oleh penilai tunggal tanpa validasi lapangan",
     "Generalisasi ke kejadian dan sensor lain belum teruji; label dapat memuat bias penilai",
     "Protokol pelabelan tertulis dan lima kendali atribusi kausal (Subbab 3.2.3 poin e–f)"
    ],
    [
     "Selang prabencana",
     "7,2–20,1 bulan sebelum kejadian",
     "Perubahan akibat siklus budi daya dapat terbaca sebagai perubahan",
     "Kehilangan tanaman tidak dipakai sebagai kriteria pelabelan (Subbab 3.2.3 poin e)"
    ],
    [
     "Pembagian data",
     "*Label shift* dan pergeseran kovariat pada peubah ukuran objek antara data latih dan data uji",
     "Kegagalan kelas Terdampak Sedang (F1 0,0545)",
     "Keutuhan *tile* dipertahankan demi kesahihan spasial; kedua pergeseran dikuantifikasi (Tabel 3.16, Tabel 3.17, Subbab 4.2.2)"
    ],
    [
     "Konfigurasi Tujuan 1",
     "YOLOv8-seg varian nano dengan `imgsz=640`; batas 100 deteksi per citra pada evaluasi Tujuan 1",
     "Perbandingan berlaku untuk konfigurasi tersebut; *recall* Tujuan 1 terbatasi konfigurasi",
     "Batas dinaikkan menjadi 500 pada Tujuan 3 dan pengaruhnya diukur (Subbab 4.3.1)"
    ],
    [
     "Deteksi objek kecil",
     "*Recall* segmentasi kuartil luas terkecil hanya 0,4371",
     "33,9% segmen uji tidak terdeteksi dan tidak dapat dinilai kerusakannya",
     "Dikuantifikasi melalui tipologi *false negative* dan kuartil luas (Tabel 4.11 dan Tabel 4.12)"
    ],
    [
     "Cakupan evaluasi",
     "Evaluasi model Mask R-CNN–RF tidak memuat 127 *false positive*",
     "Skor gabungan xView2 tidak mencerminkan risiko prediksi palsu",
     "Tipologi *false positive* dilaporkan terpisah (Subbab 4.3.6)"
    ],
    [
     "Parameter fitur",
     "Rentang HSV dan parameter *layer* tidak disetel ulang pada skala 18 *tile*",
     "Keteralihan ke citra dengan karakteristik radiometrik berbeda belum teruji",
     "Nilai bawaan dan nilai empiris dicatat eksplisit (Tabel 3.11)"
    ],
    [
     "Artefak web",
     "Kesetaraan hasil bergantung pada GeoTIFF 32-bit, presisi FP32, dan ketersediaan GPU",
     "Konversi persentil per kanal hanya 37,8% kelas sama; TF32 menggeser 2 dari 115 segmen",
     "Presisi dikunci ke FP32 dan panduan penyiapan citra disusun (Subbab 4.4.1 poin c–d)"
    ]
   ],
   "keterangan": "Angka dalam tabel merujuk pada hasil yang telah disajikan pada Subbab 4.1–4.4.",
   "tebal": [],
   "panel": []
  },
  "T4.5.c": {
   "judul": "Potensi pemanfaatan keluaran penelitian oleh instansi pemerintah",
   "kepala": [
    [
     [
      "Instansi",
      1,
      1
     ],
     [
      "Kebutuhan informasi",
      1,
      1
     ],
     [
      "Keluaran yang dapat dimanfaatkan",
      1,
      1
     ],
     [
      "Catatan penerapan",
      1,
      1
     ]
    ]
   ],
   "rows": [
    [
     "Kementerian Pertanian dan dinas pertanian daerah",
     "Sebaran dan tingkat keparahan kerusakan lahan pertanian sebagai dasar perencanaan bantuan dan pemulihan",
     "Segmen lahan berlabel kelas kerusakan beserta luas per kelas",
     "Kelas Terdampak Berat paling andal; kelas Terdampak Sedang memerlukan verifikasi lapangan"
    ],
    [
     "Badan Pusat Statistik",
     "Statistik lahan pertanian menurut kategori lahan sawah dan bukan sawah",
     "Jumlah dan luas lahan terdeteksi per kelas kerusakan sebagai data pendukung",
     "Definisi operasional penelitian berbeda dari kategori statistik; luas perlu dikoreksi untuk lahan yang tidak terdeteksi"
    ],
    [
     "Lembaga penanggulangan bencana pusat dan daerah",
     "Gambaran cepat dampak pascabencana pada wilayah yang luas",
     "Peta awal (*screening*) area pertanian terdampak dalam hitungan detik per *tile*",
     "Keluaran bersifat indikatif dan perlu diikuti verifikasi lapangan terarah"
    ],
    [
     "Pemerintah daerah (perencanaan wilayah)",
     "Perlindungan lahan pertanian pangan berkelanjutan dan identifikasi lahan rusak",
     "Indikasi lahan Terdampak Berat sebagai calon prioritas rehabilitasi",
     "Kelas model mengukur keluasan indikasi kerusakan fisik, bukan hilangnya fungsi produksi lahan"
    ]
   ],
   "keterangan": "Pemetaan disusun penelitian ini berdasarkan kebutuhan pemangku kepentingan pada Subbab 3.2.1 poin b dan rujukan kebijakan pada Subbab 2.1.2; belum divalidasi melalui konsultasi dengan instansi terkait.",
   "tebal": [],
   "panel": []
  }
 },
 "t1": {
  "label": [
   "Precision instans",
   "Recall instans",
   "F1 instans",
   "IoU instans",
   "Precision piksel",
   "Recall piksel",
   "F1 piksel",
   "IoU piksel"
  ],
  "yolo": [
   0.6092,
   0.5943,
   0.5973,
   0.7492,
   0.7643,
   0.6748,
   0.6963,
   0.5399
  ],
  "mrcnn": [
   0.8131,
   0.5813,
   0.6589,
   0.8421,
   0.8737,
   0.6467,
   0.7178,
   0.5702
  ]
 },
 "t2": {
  "label": [
   "Akurasi",
   "F1-macro",
   "Precision-macro",
   "Recall-macro",
   "Kappa kuadratik"
  ],
  "rf": [
   0.6639,
   0.4903,
   0.5467,
   0.5069,
   0.5556
  ],
  "lgbm": [
   0.6507,
   0.4849,
   0.5228,
   0.5063,
   0.4566
  ]
 },
 "fi": {
  "label": [
   "Batas lahan",
   "Material asing",
   "Kehilangan tanaman",
   "Perubahan radiometri",
   "Genangan baru",
   "Perubahan semantik (SAC)"
  ],
  "gini": [
   0.2193,
   0.1523,
   0.1005,
   0.1913,
   0.1617,
   0.1749
  ],
  "perm": [
   0.0474,
   0.0583,
   0.0253,
   0.0415,
   0.0581,
   0.037
  ],
  "perm_sd": [
   0.0201,
   0.0187,
   0.013,
   0.0108,
   0.0134,
   0.0192
  ]
 },
 "t3": {
  "deteksi": {
   "TP": 399,
   "FP": 127,
   "FN": 205,
   "precision": 0.7586,
   "recall": 0.6606,
   "f1_lokalisasi": 0.7062
  },
  "f1_kelas": {
   "Tidak Terdampak": 0.5328,
   "Terdampak Sedang": 0.0548,
   "Terdampak Berat": 0.8283
  },
  "macro_f1": 0.472,
  "hm": 0.1406,
  "xview2": 0.3103,
  "miou": {
   "per_kelas": {
    "background": 0.7918,
    "Tidak Terdampak": 0.2496,
    "Terdampak Sedang": 0.0188,
    "Terdampak Berat": 0.5419
   },
   "rata_rata": 0.4005
  },
  "oracle_selisih": 0.0182,
  "per_tile": [
   {
    "tile_id": "00000163",
    "n_pred": "92",
    "n_gt": "113",
    "TP": "67",
    "FP": "25",
    "FN": "46",
    "precision_lokalisasi": "0.7283",
    "recall_lokalisasi": "0.5929",
    "f1_lokalisasi": "0.6537",
    "akurasi_klasifikasi_matched": "0.5373"
   },
   {
    "tile_id": "00000169",
    "n_pred": "130",
    "n_gt": "155",
    "TP": "106",
    "FP": "24",
    "FN": "49",
    "precision_lokalisasi": "0.8154",
    "recall_lokalisasi": "0.6839",
    "f1_lokalisasi": "0.7439",
    "akurasi_klasifikasi_matched": "0.5"
   },
   {
    "tile_id": "00000184",
    "n_pred": "189",
    "n_gt": "243",
    "TP": "147",
    "FP": "42",
    "FN": "96",
    "precision_lokalisasi": "0.7778",
    "recall_lokalisasi": "0.6049",
    "f1_lokalisasi": "0.6806",
    "akurasi_klasifikasi_matched": "0.7279"
   },
   {
    "tile_id": "00000195",
    "n_pred": "115",
    "n_gt": "93",
    "TP": "79",
    "FP": "36",
    "FN": "14",
    "precision_lokalisasi": "0.687",
    "recall_lokalisasi": "0.8495",
    "f1_lokalisasi": "0.7596",
    "akurasi_klasifikasi_matched": "0.8608"
   }
  ]
 },
 "distribusi": {
  "Tidak Terdampak": "787",
  "Terdampak Sedang": "292",
  "Terdampak Berat": "2.192"
 },
 "galeri": [
  {
   "tile": "00000163",
   "ukuran_pre": [
    1024,
    1018
   ],
   "luas": [
    {
     "Kelas Kerusakan": "Tidak Terdampak",
     "Jumlah Poligon": "17",
     "Total Luas (ha)": "0.7223"
    },
    {
     "Kelas Kerusakan": "Terdampak Sedang",
     "Jumlah Poligon": "18",
     "Total Luas (ha)": "0.7808"
    },
    {
     "Kelas Kerusakan": "Terdampak Berat",
     "Jumlah Poligon": "57",
     "Total Luas (ha)": "3.4093"
    },
    {
     "Kelas Kerusakan": "Total",
     "Jumlah Poligon": "92",
     "Total Luas (ha)": "4.9124"
    }
   ],
   "resmi": {
    "tile_id": "00000163",
    "n_pred": "92",
    "n_gt": "113",
    "TP": "67",
    "FP": "25",
    "FN": "46",
    "precision_lokalisasi": "0.7283",
    "recall_lokalisasi": "0.5929",
    "f1_lokalisasi": "0.6537",
    "akurasi_klasifikasi_matched": "0.5373"
   }
  },
  {
   "tile": "00000169",
   "ukuran_pre": [
    1024,
    1018
   ],
   "luas": [
    {
     "Kelas Kerusakan": "Tidak Terdampak",
     "Jumlah Poligon": "34",
     "Total Luas (ha)": "1.9466"
    },
    {
     "Kelas Kerusakan": "Terdampak Sedang",
     "Jumlah Poligon": "19",
     "Total Luas (ha)": "1.1904"
    },
    {
     "Kelas Kerusakan": "Terdampak Berat",
     "Jumlah Poligon": "77",
     "Total Luas (ha)": "5.2011"
    },
    {
     "Kelas Kerusakan": "Total",
     "Jumlah Poligon": "130",
     "Total Luas (ha)": "8.3381"
    }
   ],
   "resmi": {
    "tile_id": "00000169",
    "n_pred": "130",
    "n_gt": "155",
    "TP": "106",
    "FP": "24",
    "FN": "49",
    "precision_lokalisasi": "0.8154",
    "recall_lokalisasi": "0.6839",
    "f1_lokalisasi": "0.7439",
    "akurasi_klasifikasi_matched": "0.5"
   }
  },
  {
   "tile": "00000184",
   "ukuran_pre": [
    1024,
    1018
   ],
   "luas": [
    {
     "Kelas Kerusakan": "Tidak Terdampak",
     "Jumlah Poligon": "45",
     "Total Luas (ha)": "3.6763"
    },
    {
     "Kelas Kerusakan": "Terdampak Sedang",
     "Jumlah Poligon": "29",
     "Total Luas (ha)": "1.9222"
    },
    {
     "Kelas Kerusakan": "Terdampak Berat",
     "Jumlah Poligon": "115",
     "Total Luas (ha)": "10.1253"
    },
    {
     "Kelas Kerusakan": "Total",
     "Jumlah Poligon": "189",
     "Total Luas (ha)": "15.7239"
    }
   ],
   "resmi": {
    "tile_id": "00000184",
    "n_pred": "189",
    "n_gt": "243",
    "TP": "147",
    "FP": "42",
    "FN": "96",
    "precision_lokalisasi": "0.7778",
    "recall_lokalisasi": "0.6049",
    "f1_lokalisasi": "0.6806",
    "akurasi_klasifikasi_matched": "0.7279"
   }
  },
  {
   "tile": "00000195",
   "ukuran_pre": [
    1024,
    1018
   ],
   "luas": [
    {
     "Kelas Kerusakan": "Tidak Terdampak",
     "Jumlah Poligon": "10",
     "Total Luas (ha)": "0.7824"
    },
    {
     "Kelas Kerusakan": "Terdampak Sedang",
     "Jumlah Poligon": "7",
     "Total Luas (ha)": "0.3673"
    },
    {
     "Kelas Kerusakan": "Terdampak Berat",
     "Jumlah Poligon": "98",
     "Total Luas (ha)": "8.8608"
    },
    {
     "Kelas Kerusakan": "Total",
     "Jumlah Poligon": "115",
     "Total Luas (ha)": "10.0105"
    }
   ],
   "resmi": {
    "tile_id": "00000195",
    "n_pred": "115",
    "n_gt": "93",
    "TP": "79",
    "FP": "36",
    "FN": "14",
    "precision_lokalisasi": "0.687",
    "recall_lokalisasi": "0.8495",
    "f1_lokalisasi": "0.7596",
    "akurasi_klasifikasi_matched": "0.8608"
   }
  }
 ]
};
