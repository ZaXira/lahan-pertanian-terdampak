"""
Tahap 3 — Klasifikasi tingkat kerusakan per poligon (Random Forest).

Diadaptasi dari reference/Tujuan 3 code.txt (CELL A load model, CELL D langkah 3).
"""
from functools import lru_cache

import joblib
import numpy as np

from pipeline.model_paths import LE_FILE, RF_FILE, resolve

# Urutan ordinal (ringan -> berat), BUKAN alfabetis
LABELS_ORD = ["Tidak Terdampak", "Terdampak Sedang", "Terdampak Berat"]

# Input model: HANYA 6 fitur kontinu, urutan WAJIB persis seperti ini
FEATURE_COLS_MODEL = [
    "f_batas_cont", "f_material_cont", "f_tanaman_cont",
    "f_radiometri_cont", "f_genangan_cont", "f_sac_cont",
]


@lru_cache(maxsize=1)
def load_classifier():
    """Load Random Forest + LabelEncoder sekali, dipakai ulang antar request."""
    model_rf = joblib.load(resolve(RF_FILE))
    le = joblib.load(resolve(LE_FILE))
    le.classes_ = np.array(LABELS_ORD)
    assert list(le.classes_) == LABELS_ORD, f"Urutan label encoder tidak sesuai: {list(le.classes_)}"
    return model_rf, le


def classify_polygons(df_feat):
    """Tambahkan kolom damage_pred ke tabel fitur (salinan, input tidak diubah)."""
    df_out = df_feat.copy()
    if len(df_out) == 0:
        df_out["damage_pred"] = []
        return df_out
    model_rf, le = load_classifier()
    X = df_out[FEATURE_COLS_MODEL].values.astype(np.float32)
    df_out["damage_pred"] = le.inverse_transform(model_rf.predict(X))
    return df_out
