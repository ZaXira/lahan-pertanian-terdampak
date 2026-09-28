# -*- coding: utf-8 -*-
"""Buat/perbarui Space baru (ZeroGPU) dari artefak_fix/space. Space lama tidak disentuh.
  python -X utf8 artefak_fix/tools/deploy_space.py"""
from pathlib import Path

from huggingface_hub import HfApi

ROOT = Path(__file__).resolve().parents[2]
SPACE = "ZaXira/lahan-pertanian-terdampak"
MODEL_REPO = "ZaXira/artefak-kerusakan-lahan"
SITUS = "https://lahan-terdampak-palu.vercel.app"

api = HfApi()
api.create_repo(SPACE, repo_type="space", space_sdk="gradio", space_hardware="zero-a10g", exist_ok=True)
api.add_space_variable(SPACE, "HF_MODEL_REPO", MODEL_REPO)
api.add_space_variable(SPACE, "SITUS_URL", SITUS)
info = api.upload_folder(repo_id=SPACE, repo_type="space", folder_path=str(ROOT / "artefak_fix" / "space"),
                         ignore_patterns=["__pycache__/*", "**/__pycache__/*", "*.pyc", "models/*", "*.pth", "*.joblib"],
                         commit_message="Tampilan baru (artefak_fix): tema lahan pertanian, tab panduan, API /proses")
print("diunggah:", info)
rt = api.get_space_runtime(SPACE)
print("hardware:", rt.hardware, "| diminta:", rt.requested_hardware, "| stage:", rt.stage)
