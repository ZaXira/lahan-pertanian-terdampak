"""
Tahap 1 — Deteksi poligon lahan pertanian dengan Mask R-CNN (detectron2).

Hanya memakai citra PRE-disaster (sama seperti Tujuan 1 & 3).

Diadaptasi dari reference/Tujuan 3 code.txt (CELL A, B, C):
  - safe_geometry, mask_to_polygons : disalin apa adanya
  - build_maskrcnn_cfg              : config inferensi Tujuan 3 (baris 889-896),
                                      dibungkus jadi fungsi
  - rgb_to_model_bgr                : _tif_pre_to_bgr_uint8, tapi menerima array
                                      (bukan path GeoTIFF)

Adaptasi ruang piksel: citra upload tidak punya georeferensi, jadi transform
= Affine.identity() dan crs = None -> poligon hidup di koordinat piksel.
"""
import os
import sys
from functools import lru_cache

import numpy as np
import geopandas as gpd
import torch
from affine import Affine
from rasterio.features import shapes as rio_shapes
from shapely.geometry import shape
from shapely.validation import make_valid

from pipeline.model_paths import MRCNN_FILE, PROJECT_ROOT, resolve

# detectron2 di Windows lokal tidak bisa di-build (tanpa MSVC) -> pakai source
# tanpa ekstensi C++ dari third_party/. Mask R-CNN R50-FPN hanya butuh op
# torchvision (roi_align, nms), bukan detectron2._C.
_D2_SRC = os.path.join(PROJECT_ROOT, "third_party", "detectron2")
try:
    import detectron2  # noqa: F401
except ImportError:
    sys.path.insert(0, _D2_SRC)

from detectron2.config import get_cfg  # noqa: E402
from detectron2.engine import DefaultPredictor  # noqa: E402

MRCNN_BASE_CONFIG = "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"
PIXEL_TRANSFORM = Affine.identity()

# Konsistensi numerik lintas perangkat keras: GPU modern (Ampere ke atas) memakai
# TF32 untuk konvolusi/matmul secara default, sehingga beberapa deteksi di ambang
# batas bergeser dibanding hasil penelitian (dilatih & dievaluasi di T4, FP32 penuh).
torch.backends.cudnn.allow_tf32 = False
torch.backends.cuda.matmul.allow_tf32 = False


# ================================================================
# Fungsi reuse Tujuan 1/3 (logika TIDAK diubah)
# ================================================================
def safe_geometry(geom):
    if geom is None or geom.is_empty:
        return None
    if not geom.is_valid:
        try:
            geom = make_valid(geom)
        except Exception:
            try:
                geom = geom.buffer(0)
            except Exception:
                return None
    if geom is None or geom.is_empty or geom.area <= 0:
        return None
    if geom.geom_type not in ("Polygon", "MultiPolygon"):
        polys = [g for g in getattr(geom, "geoms", []) if g.geom_type == "Polygon"]
        if not polys:
            return None
        geom = max(polys, key=lambda g: g.area)
    return geom


def mask_to_polygons(mask, transform, crs, min_area_px=10):
    polys = []
    mask = mask.astype(np.int32)
    for geom_json, value in rio_shapes(mask, mask=(mask > 0), transform=transform):
        if value == 0:
            continue
        geom = safe_geometry(shape(geom_json))
        if geom is None:
            continue
        polys.append(geom)
    if not polys:
        return gpd.GeoDataFrame(geometry=[], crs=crs)
    gdf = gpd.GeoDataFrame(geometry=polys, crs=crs)
    px_area = abs(transform.a * transform.e)
    gdf = gdf[gdf.geometry.area >= (min_area_px * px_area)].reset_index(drop=True)
    return gdf


# ================================================================
# Config & predictor
# ================================================================
def _base_config_file():
    """Path YAML config dasar. Diambil dari third_party/detectron2/configs lebih dulu:
    detectron2.model_zoo sengaja TIDAK diimpor karena memakai pkg_resources, yang
    tidak tersedia di Python 3.12 tanpa setuptools."""
    lokal = os.path.join(_D2_SRC, "configs", MRCNN_BASE_CONFIG)
    if os.path.exists(lokal):
        return lokal
    from detectron2 import model_zoo  # detectron2 hasil pip install
    return model_zoo.get_config_file(MRCNN_BASE_CONFIG)


def build_maskrcnn_cfg(weights_path=None, device=None):
    """Config inferensi final (rekonstruksi Tujuan 3 yang sudah tervalidasi)."""
    cfg = get_cfg()
    cfg.merge_from_file(_base_config_file())
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
    cfg.MODEL.WEIGHTS = weights_path or resolve(MRCNN_FILE, "MRCNN_WEIGHTS_PATH")
    cfg.TEST.DETECTIONS_PER_IMAGE = 500          # dinaikkan dari default 100
    cfg.MODEL.ROI_HEADS.NMS_THRESH_TEST = 0.5    # default, dipertahankan
    # MODEL_DEVICE bisa dipaksa lewat env (mis. "cuda" di ZeroGPU, yang memakai
    # emulasi CUDA di luar fungsi ber-dekorator @spaces.GPU).
    cfg.MODEL.DEVICE = (device or os.environ.get("MODEL_DEVICE")
                        or ("cuda" if torch.cuda.is_available() else "cpu"))
    return cfg


@lru_cache(maxsize=1)
def get_predictor():
    """Load Mask R-CNN sekali, dipakai ulang antar request."""
    return DefaultPredictor(build_maskrcnn_cfg())


# ================================================================
# Preprocessing & inferensi
# ================================================================
def rgb_to_model_bgr(img_rgb):
    """Replikasi _tif_pre_to_bgr_uint8 Tujuan 3 untuk array HxWx3 (RGB):
    min-max normalize GABUNGAN 3 band (bukan per-band) -> uint8, lalu RGB->BGR."""
    arr = np.asarray(img_rgb)[:, :, :3].astype(np.float32)
    arr = ((arr - arr.min()) / max(arr.max() - arr.min(), 1) * 255).astype(np.uint8)
    return np.ascontiguousarray(arr[:, :, ::-1])


def detect_polygons(img_pre_rgb, min_area_px=10):
    """Jalankan Mask R-CNN pada citra PRE-disaster (tile penuh, tanpa sliding-window).

    Args:
        img_pre_rgb: array HxWx3 (RGB), dtype apa saja (uint8 dari upload,
            int16 dari GeoTIFF uji).

    Returns:
        GeoDataFrame (koordinat piksel, crs=None) dengan kolom
        pred_id (0, 1, 2, ...), polygon_id (= pred_id, dibutuhkan
        extract_all_features), geometry.
    """
    img_bgr = rgb_to_model_bgr(img_pre_rgb)
    outputs = get_predictor()(img_bgr)
    instances = outputs["instances"].to("cpu")

    all_polys = []
    if instances.has("pred_masks"):
        for m in instances.pred_masks.numpy():
            gdf_tmp = mask_to_polygons(m.astype(np.uint8), PIXEL_TRANSFORM, None,
                                       min_area_px=min_area_px)
            all_polys.extend(list(gdf_tmp.geometry))

    all_polys = [safe_geometry(g) for g in all_polys]
    all_polys = [g for g in all_polys if g is not None]

    gdf_pred = gpd.GeoDataFrame(geometry=all_polys, crs=None)
    gdf_pred["pred_id"] = np.arange(len(gdf_pred))
    gdf_pred["polygon_id"] = gdf_pred["pred_id"]
    return gdf_pred[["pred_id", "polygon_id", "geometry"]]
