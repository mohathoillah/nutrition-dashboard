import warnings

import numpy as np
import pandas as pd
import geopandas as gpd
import streamlit as st

from libpysal.weights import Queen, Rook, KNN, DistanceBand
from esda.moran import Moran, Moran_Local
from esda.getisord import G_Local

from utils.loader import load_data, load_geojson

WEIGHT_METHODS = [
    "Queen contiguity",
    "Rook contiguity",
    "K-nearest neighbors",
    "Distance-band",
]

LISA_LABELS = {1: "High-High", 2: "Low-High", 3: "Low-Low", 4: "High-Low"}

SEED = 12345
ALPHA = 0.05


def _build_gdf(value_column):
    df = load_data()
    geojson = load_geojson()

    gdf = gpd.GeoDataFrame.from_features(geojson["features"], crs="EPSG:4326")
    gdf = gdf.merge(df, on="district_en", how="inner")
    gdf = gdf.dropna(subset=[value_column]).reset_index(drop=True)
    return gdf


def _build_weights(gdf, method, k=8, threshold_km=200):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        if method == "Queen contiguity":
            w = Queen.from_dataframe(gdf, use_index=False, silence_warnings=True)
        elif method == "Rook contiguity":
            w = Rook.from_dataframe(gdf, use_index=False, silence_warnings=True)
        elif method == "K-nearest neighbors":
            w = KNN.from_dataframe(gdf, k=k, silence_warnings=True)
        elif method == "Distance-band":
            points = gdf.geometry.representative_point()
            coords = list(zip(points.x, points.y))
            w = DistanceBand(
                coords,
                threshold=threshold_km,
                binary=True,
                distance_metric="arc",
                radius=6371,
                silence_warnings=True,
            )
        else:
            raise ValueError(f"Unknown weight method: {method}")

    w.transform = "r"
    return w


def _classify_lisa(q, p_sim):
    if pd.isna(q) or pd.isna(p_sim):
        return "No Neighbors"
    if p_sim >= ALPHA:
        return "Not Significant"
    return LISA_LABELS.get(int(q), "Not Significant")


def _classify_hotspot(z, p_sim):
    if pd.isna(z) or pd.isna(p_sim):
        return "No Neighbors"
    if p_sim <= 0.01:
        tier = "99%"
    elif p_sim <= 0.05:
        tier = "95%"
    elif p_sim <= 0.10:
        tier = "90%"
    else:
        return "Not Significant"
    return f"{'Hot Spot' if z > 0 else 'Cold Spot'} ({tier})"


@st.cache_resource(
    show_spinner="Building spatial weights and running spatial statistics...",
    max_entries=8,
)
def get_spatial_analysis(value_column, method, k=8, threshold_km=200, permutations=999):
    gdf = _build_gdf(value_column)
    w = _build_weights(gdf, method, k=k, threshold_km=threshold_km)
    y = gdf[value_column].to_numpy(dtype=float)

    np.random.seed(SEED)
    moran_global = Moran(y, w, permutations=permutations)

    lisa = Moran_Local(y, w, permutations=permutations, seed=SEED)
    hotspot = G_Local(y, w, transform="R", permutations=permutations, star=True, seed=SEED)

    gdf = gdf.copy()
    gdf["lisa_cluster"] = [_classify_lisa(q, p) for q, p in zip(lisa.q, lisa.p_sim)]
    gdf["hotspot_class"] = [
        _classify_hotspot(z, p) for z, p in zip(hotspot.z_sim, hotspot.p_sim)
    ]

    cardinalities = np.array(list(w.cardinalities.values()))
    summary = {
        "n_units": w.n,
        "n_isolates": len(w.islands),
        "avg_neighbors": float(cardinalities.mean()),
        "min_neighbors": int(cardinalities.min()),
        "max_neighbors": int(cardinalities.max()),
    }

    map_gdf = gpd.GeoDataFrame({"district_en": gdf["district_en"]}, geometry=gdf.geometry, crs=gdf.crs)

    return {
        "gdf": gdf,
        "geo_interface": map_gdf.__geo_interface__,
        "w": w,
        "moran_global": moran_global,
        "summary": summary,
    }


def get_neighbor_names(gdf, w, district_en):
    matches = gdf.index[gdf["district_en"] == district_en]
    if len(matches) == 0:
        return []

    idx = matches[0]
    neighbor_idxs = w.neighbors.get(idx, [])
    return gdf.loc[neighbor_idxs, "district_en"].tolist()
