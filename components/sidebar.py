import streamlit as st

from config import NUTRITION_OPTIONS

FILTER_KEYS = [
    "filter_indicator",
    "filter_year",
    "filter_island",
    "filter_province",
    "filter_color_scale",
    "filter_show_raw_data"
]


def render_sidebar(df):
    st.sidebar.title("Filters")

    if st.sidebar.button("Reset filters"):
        for key in FILTER_KEYS:
            st.session_state.pop(key, None)
        st.rerun()

    with st.sidebar.form("filter_form"):
        selected_indicator = st.selectbox(
            "Nutrition status",
            options=list(NUTRITION_OPTIONS.keys()),
            key="filter_indicator"
        )

        indicator_config = NUTRITION_OPTIONS[selected_indicator]

        if indicator_config["type"] == "multi_year":
            selected_year = st.selectbox(
                "Year",
                options=list(indicator_config["columns"].keys()),
                index=2,
                key="filter_year"
            )
        else:
            selected_year = indicator_config["year"]
            st.info(f"{selected_indicator} is available only for {selected_year}.")

        island_options = sorted(df["island_en"].dropna().unique().tolist())
        selected_islands = st.multiselect(
            "Island (leave empty for all)",
            options=island_options,
            key="filter_island"
        )

        province_options = sorted(df["province_en"].dropna().unique().tolist())
        selected_provinces = st.multiselect(
            "Province (leave empty for all)",
            options=province_options,
            key="filter_province"
        )

        st.divider()

        color_scale = st.selectbox(
            "Map color scale",
            options=["YlOrRd", "Reds", "Oranges", "Viridis", "Blues"],
            index=0,
            key="filter_color_scale"
        )

        show_raw_data = st.checkbox(
            "Show data table",
            value=True,
            key="filter_show_raw_data"
        )

        st.form_submit_button("Apply Filters")

    return {
        "indicator": selected_indicator,
        "year": selected_year,
        "islands": selected_islands,
        "provinces": selected_provinces,
        "color_scale": color_scale,
        "show_raw_data": show_raw_data
    }
