import plotly.express as px
import streamlit as st

from config import NUTRITION_OPTIONS
from utils.spatial import WEIGHT_METHODS, get_neighbor_names, get_spatial_analysis

STUNTING_YEAR_COLUMNS = NUTRITION_OPTIONS["Stunting"]["columns"]

LISA_COLORS = {
    "High-High": "#e34948",
    "Low-High": "#a6d3f2",
    "Low-Low": "#2a78d6",
    "High-Low": "#eb6834",
    "Not Significant": "#d9d9d9",
    "No Neighbors": "#6b6b6b",
}
LISA_ORDER = list(LISA_COLORS.keys())

HOTSPOT_COLORS = {
    "Hot Spot (99%)": "#b2182b",
    "Hot Spot (95%)": "#ef8a62",
    "Hot Spot (90%)": "#fddbc7",
    "Not Significant": "#d9d9d9",
    "Cold Spot (90%)": "#d1e5f0",
    "Cold Spot (95%)": "#67a9cf",
    "Cold Spot (99%)": "#2166ac",
    "No Neighbors": "#6b6b6b",
}
HOTSPOT_ORDER = list(HOTSPOT_COLORS.keys())

MAP_CENTER = {"lat": -2.5, "lon": 118}
MAP_ZOOM = 3.5


def _categorical_choropleth(gdf, geo_interface, value_column, color_column, color_map, category_order, legend_title):
    fig = px.choropleth_mapbox(
        gdf,
        geojson=geo_interface,
        locations="district_en",
        featureidkey="properties.district_en",
        color=color_column,
        color_discrete_map=color_map,
        category_orders={color_column: category_order},
        hover_name="district_en",
        hover_data=["province_en", value_column],
        mapbox_style="carto-positron",
        zoom=MAP_ZOOM,
        center=MAP_CENTER,
        opacity=0.85,
    )
    fig.update_layout(
        height=650,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        legend_title_text=legend_title,
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_controls():
    st.caption(
        "Computed on the full national dataset of 514 districts/cities, "
        "independent of the sidebar's island/province filters, so that "
        "spatial neighborhoods aren't cut off at a filter boundary."
    )

    col_year, col_method, col_param = st.columns([1, 1.4, 1.2])

    with col_year:
        year = st.radio(
            "Year",
            options=list(STUNTING_YEAR_COLUMNS.keys()),
            index=2,
            horizontal=True,
            key="spatial_year",
        )

    with col_method:
        method = st.selectbox(
            "Spatial weight matrix",
            options=WEIGHT_METHODS,
            index=0,
            key="spatial_method",
        )

    k = 8
    threshold_km = 200
    with col_param:
        if method == "K-nearest neighbors":
            k = st.slider("k (neighbors)", min_value=4, max_value=10, value=8, key="spatial_k")
        elif method == "Distance-band":
            threshold_km = st.slider(
                "Distance threshold (km)",
                min_value=50,
                max_value=500,
                value=200,
                step=10,
                key="spatial_threshold",
            )
        else:
            st.caption("No extra parameter needed for contiguity weights.")

    value_column = STUNTING_YEAR_COLUMNS[year]
    return value_column, year, method, k, threshold_km


def _render_weight_summary(summary, method):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Districts/cities analyzed", summary["n_units"])
    col2.metric("Avg. neighbors", f"{summary['avg_neighbors']:.1f}")
    col3.metric("Min / Max neighbors", f"{summary['min_neighbors']} / {summary['max_neighbors']}")
    col4.metric("Isolates (no neighbors)", summary["n_isolates"])

    st.caption(
        f"Weight matrix: {method}. Row-standardized before use in Moran's I, "
        "LISA, and Getis-Ord Gi*."
    )

    if summary["n_isolates"] > 0:
        st.warning(
            f"{summary['n_isolates']} districts/cities have no neighbors under "
            f"{method} (typically small or remote islands with no shared "
            "border, or outside the distance threshold). They're excluded "
            "from local statistics ('No Neighbors' class) but still counted "
            "in the global Moran's I. Try K-nearest neighbors or "
            "Distance-band if every unit needs at least one neighbor."
        )


def _render_global_moran(moran_global, year):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Moran's I", f"{moran_global.I:.4f}")
    col2.metric("Expected I", f"{moran_global.EI:.4f}")
    col3.metric("Z-score", f"{moran_global.z_sim:.2f}")
    col4.metric("P-value (999 perm.)", f"{moran_global.p_sim:.4f}")

    if moran_global.p_sim < 0.05:
        direction = "positive" if moran_global.I > moran_global.EI else "negative"
        interpretation = (
            "districts with similar stunting levels cluster together geographically"
            if direction == "positive"
            else "neighboring districts tend to have dissimilar stunting levels"
        )
        st.success(
            f"Statistically significant {direction} spatial autocorrelation in "
            f"stunting prevalence for {year} (p = {moran_global.p_sim:.3f}) — "
            f"{interpretation}."
        )
    else:
        st.info(
            f"No statistically significant spatial autocorrelation detected for "
            f"{year} (p = {moran_global.p_sim:.3f}) — stunting appears spatially "
            "random under this weight configuration."
        )


def _render_lisa_map(gdf, geo_interface, value_column, year):
    st.caption(
        "Compares each district/city's stunting value to its neighbors' "
        "average. High-High and Low-Low mark clusters of similarly extreme "
        "values; High-Low and Low-High mark spatial outliers. "
        "Significance at p < 0.05 (999 permutations)."
    )
    _categorical_choropleth(gdf, geo_interface, value_column, "lisa_cluster", LISA_COLORS, LISA_ORDER, "LISA Cluster")

    counts = gdf["lisa_cluster"].value_counts()
    breakdown = ", ".join(
        f"{label}: {counts.get(label, 0)}" for label in LISA_ORDER if counts.get(label, 0) > 0
    )
    st.caption(f"Stunting {year} — {breakdown}")


def _render_hotspot_map(gdf, geo_interface, value_column, year):
    st.caption(
        "Getis-Ord Gi* identifies districts/cities where high (hot spot) or "
        "low (cold spot) stunting values cluster with their neighbors, at "
        "90/95/99% confidence (999 permutations)."
    )
    _categorical_choropleth(
        gdf, geo_interface, value_column, "hotspot_class", HOTSPOT_COLORS, HOTSPOT_ORDER, "Hotspot Class"
    )

    counts = gdf["hotspot_class"].value_counts()
    breakdown = ", ".join(
        f"{label}: {counts.get(label, 0)}" for label in HOTSPOT_ORDER if counts.get(label, 0) > 0
    )
    st.caption(f"Stunting {year} — {breakdown}")


def _render_neighbor_explorer(gdf, geo_interface, w, value_column, year):
    st.caption(
        "Pick a district/city to see its neighbors under the current weight "
        "matrix, highlighted on the map."
    )
    district_options = sorted(gdf["district_en"].tolist())
    selected = st.selectbox("District/city", options=district_options, key="spatial_neighbor_district")

    neighbor_names = get_neighbor_names(gdf, w, selected)

    if not neighbor_names:
        st.warning(f"{selected} has no neighbors under the current weight matrix.")
    else:
        neighbor_df = (
            gdf[gdf["district_en"].isin(neighbor_names)][["district_en", "province_en", value_column]]
            .sort_values(value_column, ascending=False)
            .rename(columns={value_column: f"Stunting {year} (%)"})
        )
        st.dataframe(neighbor_df, hide_index=True, use_container_width=True)

    highlight_col = "_highlight"
    highlight_gdf = gdf.copy()
    highlight_gdf[highlight_col] = "Other"
    highlight_gdf.loc[highlight_gdf["district_en"].isin(neighbor_names), highlight_col] = "Neighbor"
    highlight_gdf.loc[highlight_gdf["district_en"] == selected, highlight_col] = "Selected"

    highlight_colors = {"Selected": "#e34948", "Neighbor": "#eda100", "Other": "#d9d9d9"}
    highlight_order = ["Selected", "Neighbor", "Other"]

    _categorical_choropleth(
        highlight_gdf, geo_interface, value_column, highlight_col, highlight_colors, highlight_order, "Role"
    )


def render_spatial_analysis():
    st.subheader("Spatial Analysis (Stunting)")

    value_column, year, method, k, threshold_km = _render_controls()

    result = get_spatial_analysis(value_column, method, k=k, threshold_km=threshold_km)
    gdf = result["gdf"]
    geo_interface = result["geo_interface"]
    w = result["w"]
    moran_global = result["moran_global"]
    summary = result["summary"]

    tab_weights, tab_moran, tab_lisa, tab_hotspot, tab_neighbors = st.tabs(
        ["Weight Matrix", "Global Moran's I", "LISA Cluster Map", "Hotspot Analysis", "Neighbor Explorer"]
    )

    with tab_weights:
        _render_weight_summary(summary, method)

    with tab_moran:
        _render_global_moran(moran_global, year)

    with tab_lisa:
        _render_lisa_map(gdf, geo_interface, value_column, year)

    with tab_hotspot:
        _render_hotspot_map(gdf, geo_interface, value_column, year)

    with tab_neighbors:
        _render_neighbor_explorer(gdf, geo_interface, w, value_column, year)
