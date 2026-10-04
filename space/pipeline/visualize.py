"""
Tahap 5 — Overlay poligon berwarna (per kelas kerusakan) di atas citra POST.

Diadaptasi dari reference/Tujuan 3 code.txt (CELL F, panel "Model"):
fill alpha 0.7 + outline tegas, skema warna Bab IV, latar citra POST-disaster.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.collections import PatchCollection  # noqa: E402
from matplotlib.patches import Polygon as MplPolygon  # noqa: E402

from pipeline.classify import LABELS_ORD  # noqa: E402

FILL_ALPHA = 0.7

LABEL_COLORS = {
    "Tidak Terdampak" : "#27ae60",
    "Terdampak Sedang": "#f39c12",
    "Terdampak Berat" : "#c0392b",
}


def display_image(img_rgb):
    """Logika _load_display_image Tujuan 3 (stretch percentile 2-98 gabungan
    3 band) untuk array HxWx3."""
    arr = np.asarray(img_rgb)[:, :, :3].astype(np.float32)
    lo, hi = np.percentile(arr, 2), np.percentile(arr, 98)
    return np.clip((arr - lo) / max(hi - lo, 1e-6), 0, 1)


def _geom_to_patches(geoms):
    patches = []
    for geom in geoms:
        if geom is None or geom.is_empty:
            continue
        polys = [geom] if geom.geom_type == "Polygon" else list(geom.geoms)
        for poly in polys:
            xs, ys = poly.exterior.coords.xy
            patches.append(MplPolygon(list(zip(xs, ys)), closed=True))
    return patches


def render_overlay(img_post_rgb, gdf_pred, alpha=FILL_ALPHA, linewidth=1.2):
    """Gambar overlay + legenda, dikembalikan sebagai array RGB uint8.

    gdf_pred: koordinat piksel, wajib punya kolom damage_pred.
    """
    img = display_image(img_post_rgb)
    h, w = img.shape[:2]

    dpi = 100
    fig_w = max(w / dpi, 6)
    img_h = fig_w * h / w
    fig, ax = plt.subplots(figsize=(fig_w, img_h + 0.9), dpi=dpi)
    # extent = tepi piksel, supaya koordinat poligon (tepi piksel) pas
    ax.imshow(img, extent=(0, w, h, 0))

    counts = gdf_pred["damage_pred"].value_counts() if len(gdf_pred) else {}
    for kelas in LABELS_ORD:
        subset = gdf_pred[gdf_pred["damage_pred"] == kelas] if len(gdf_pred) else gdf_pred
        if len(subset) == 0:
            continue
        color = LABEL_COLORS[kelas]
        patches = _geom_to_patches(subset.geometry)
        ax.add_collection(PatchCollection(patches, facecolor=color, edgecolor=color,
                                          alpha=alpha, linewidth=linewidth))
        # outline tegas di atas fill (biar batas poligon tetap jelas walau alpha tinggi)
        ax.add_collection(PatchCollection(patches, facecolor="none", edgecolor=color,
                                          linewidth=linewidth))
    ax.set_xlim(0, w)
    ax.set_ylim(h, 0)
    ax.axis("off")

    handles = [plt.Line2D([0], [0], marker="s", color=c, markerfacecolor=c, markersize=12,
                          lw=0, label=f"{k} ({int(counts.get(k, 0))})")
               for k, c in LABEL_COLORS.items()]

    # Lebar figure mengikuti lebar citra (bisa sempit), sedangkan label kelas panjang.
    # Legenda diletakkan di luar axes, dan gambar diambil dari canvas (bukan savefig,
    # jadi bbox_inches="tight" tidak berlaku) -> legenda yang lebih lebar dari figure
    # akan terpotong kiri-kanan. Karena itu: ukur lebar legenda, lalu rapatkan
    # (kurangi kolom / perkecil font) sampai muat.
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    batas_px = fig_w * dpi * 0.96          # sisakan margin 2% di tiap sisi
    legend, bbox = None, None
    for ncol, fontsize in ((3, 11), (3, 10), (3, 9), (2, 10), (2, 9), (1, 9), (1, 8)):
        if legend is not None:
            legend.remove()
        legend = fig.legend(handles=handles, loc="lower center", ncol=ncol, fontsize=fontsize,
                            title="Kelas kerusakan (jumlah segmen)", title_fontsize=fontsize,
                            frameon=False)
        bbox = legend.get_window_extent(renderer)
        if bbox.width <= batas_px:
            break

    # Tinggi figure menyesuaikan tinggi legenda yang terpakai (bisa >1 baris)
    legend_h = bbox.height / dpi + 0.25
    fig.set_size_inches(fig_w, img_h + legend_h)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=legend_h / (img_h + legend_h))

    fig.canvas.draw()
    out = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].copy()
    plt.close(fig)
    return out
