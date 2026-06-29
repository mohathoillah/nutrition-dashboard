import streamlit as st

from config import NUTRITION_OPTIONS


def render_sidebar(df):
    st.sidebar.title("Filters")

    selected_indicator = st.sidebar.selectbox(
        "Nutrition status",
        options=list(NUTRITION_OPTIONS.keys())
    )

    indicator_config = NUTRITION_OPTIONS[selected_indicator]

    if indicator_config["type"] == "multi_year":
        selected_year = st.sidebar.selectbox(
            "Year",
            options=list(indicator_config["columns"].keys()),
            index=2
        )
    else:
        selected_year = indicator_config["year"]
        st.sidebar.info(f"{selected_indicator} is available only for {selected_year}.")

    island_options = ["All Islands"] + sorted(df["island_en"].dropna().unique().tolist())
    selected_island = st.sidebar.selectbox(
        "Island",
        options=island_options
    )

    if selected_island == "All Islands":
        province_df = df
    else:
        province_df = df[df["island_en"] == selected_island]

    province_options = ["All Provinces"] + sorted(
        province_df["province_en"].dropna().unique().tolist()
    )

    selected_province = st.sidebar.selectbox(
        "Province",
        options=province_options
    )

    st.sidebar.divider()

    color_scale = st.sidebar.selectbox(
        "Map color scale",
        options=["YlOrRd", "Reds", "Oranges", "Viridis", "Blues"],
        index=0
    )

    show_raw_data = st.sidebar.checkbox(
        "Show data table",
        value=True
    )

    return {
        "indicator": selected_indicator,
        "year": selected_year,
        "island": selected_island,
        "province": selected_province,
        "color_scale": color_scale,
        "show_raw_data": show_raw_data
    }
