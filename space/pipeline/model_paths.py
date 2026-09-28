"""
Pencarian file model, dengan urutan prioritas:

  1. env var khusus (mis. SAM_CHECKPOINT_PATH) kalau file-nya ada
  2. file lokal di models/ (pengembangan di laptop)
  3. unduh dari Hugging Face Hub, kalau HF_MODEL_REPO di-set (dipakai di Spaces:
     file model besar tidak ikut repo Space, tapi disimpan di model repo terpisah)
"""
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.environ.get("MODEL_DIR", os.path.join(PROJECT_ROOT, "models"))

# Model repo HF berisi keempat file di bawah, mis. "namauser/artefak-kerusakan-lahan"
HF_MODEL_REPO = os.environ.get("HF_MODEL_REPO")

MRCNN_FILE = "model_final.pth"
RF_FILE = "model_random_forest.joblib"
LE_FILE = "label_encoder.joblib"
SAM_FILE = "sam_vit_b_01ec64.pth"


def resolve(filename, env_var=None):
    """Kembalikan path lokal file model (mengunduh dari HF Hub bila perlu)."""
    if env_var:
        p = os.environ.get(env_var)
        if p and os.path.exists(p):
            return p

    lokal = os.path.join(MODEL_DIR, filename)
    if os.path.exists(lokal):
        return lokal

    if HF_MODEL_REPO:
        from huggingface_hub import hf_hub_download
        return hf_hub_download(repo_id=HF_MODEL_REPO, filename=filename,
                               token=os.environ.get("HF_TOKEN"))

    raise FileNotFoundError(
        f"File model '{filename}' tidak ditemukan di {MODEL_DIR}"
        + (f" (env {env_var} juga tidak menunjuk file yang ada)" if env_var else "")
        + ". Taruh file di models/, set env var tersebut, atau set HF_MODEL_REPO "
          "ke model repo Hugging Face yang memuatnya.")
