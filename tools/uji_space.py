# -*- coding: utf-8 -*-
"""Uji regresi Space baru pada tile 00000195 (GeoTIFF) vs hasil resmi Space di Bab IV (Tabel 4.25):
115 poligon, 10/7/98, luas 10,0101 ha.
  python -X utf8 artefak_fix/tools/uji_space.py"""
import time
from pathlib import Path

from gradio_client import Client, handle_file

ROOT = Path(__file__).resolve().parents[2]
TIF = ROOT / "artefak_fix" / "dataset" / "tif"
c = Client("ZaXira/lahan-pertanian-terdampak", verbose=False, httpx_kwargs={"timeout": 300})
api = c.view_api(return_format="dict", print_info=False)
print("endpoint publik:", list(api["named_endpoints"]))
t0 = time.time()
overlay, tabel, log = c.predict(handle_file(str(TIF / "palu-tsunami_00000195_pre_disaster.tif")),
                                handle_file(str(TIF / "palu-tsunami_00000195_post_disaster.tif")),
                                0.4984, api_name="/proses")
print(f"waktu: {time.time() - t0:.1f} s | overlay: {overlay}")
print("tabel:", tabel)
print(log)
