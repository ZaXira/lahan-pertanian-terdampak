"""
Tahap 4 — Hitung luas per kelas kerusakan.

Poligon hidup di koordinat piksel, jadi luas asli dihitung dari resolusi
yang diinput pengguna (bukan dari CRS):
    luas_m2 = polygon.area (piksel^2) * resolusi^2
    luas_ha = luas_m2 / 10000
"""
import pandas as pd

from pipeline.classify import LABELS_ORD

DEFAULT_RESOLUSI_M = 0.5   # resolusi citra Palu (xBD) ~0,5 m/piksel

COL_KELAS = "Kelas Kerusakan"
COL_JUMLAH = "Jumlah Segmen"
COL_LUAS = "Total Luas (ha)"


def add_area_columns(gdf_pred, resolusi_m_per_px):
    """Tambahkan kolom luas_px, luas_m2, luas_ha per poligon."""
    if resolusi_m_per_px is None or resolusi_m_per_px <= 0:
        raise ValueError(f"Resolusi harus > 0 m/piksel (diberikan: {resolusi_m_per_px}).")
    gdf = gdf_pred.copy()
    gdf["luas_px"] = gdf.geometry.area
    gdf["luas_m2"] = gdf["luas_px"] * (resolusi_m_per_px ** 2)
    gdf["luas_ha"] = gdf["luas_m2"] / 10000
    return gdf


def area_table(gdf_pred, resolusi_m_per_px):
    """Tabel ringkasan: kelas | jumlah poligon | total luas (ha).
    Ketiga kelas selalu tampil (0 kalau tidak ada), ditutup baris Total."""
    gdf = add_area_columns(gdf_pred, resolusi_m_per_px)
    agg = gdf.groupby("damage_pred").agg(n=("luas_ha", "size"), ha=("luas_ha", "sum"))
    agg = agg.reindex(LABELS_ORD, fill_value=0)

    tabel = pd.DataFrame({
        COL_KELAS: LABELS_ORD,
        COL_JUMLAH: agg["n"].astype(int).to_numpy(),
        COL_LUAS: agg["ha"].astype(float).round(4).to_numpy(),
    })
    total = pd.DataFrame({COL_KELAS: ["Total"], COL_JUMLAH: [int(tabel[COL_JUMLAH].sum())],
                          COL_LUAS: [round(float(agg["ha"].sum()), 4)]})
    return pd.concat([tabel, total], ignore_index=True)
