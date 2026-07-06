import streamlit as st

from components.sidebar import render_sidebar
from components.kpi_cards import render_kpi_cards
from components.charts import render_distribution_chart, render_ranking_chart
from components.trends import render_stunting_trend, render_stunting_change_ranking
from components.comparisons import render_island_comparison
from components.tables import render_data_table
from components.map import render_choropleth_map
from utils.loader import load_data, load_geojson
from utils.filters import apply_filters, get_selected_column
from config import NUTRITION_DEFINITIONS


st.set_page_config(
    page_title="Nutrition Status Dashboard",
    page_icon="📊",
    layout="wide"
)

st.markdown(
    """
    <style>
    h1, h2, h3,
    [data-testid="stHeading"] h1,
    [data-testid="stHeading"] h2,
    [data-testid="stHeading"] h3 {
        color: #2563eb !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def main():
    st.title("Nutrition Status Dashboard in Indonesia")
    st.caption(
        "Phase 1: exploratory dashboard for child nutrition status "
        "at district/city level."
    )

    df = load_data()

    selections = render_sidebar(df)
    value_column, indicator_label, selected_year = get_selected_column(selections)

    st.markdown(f"**{indicator_label}** — {NUTRITION_DEFINITIONS[indicator_label]}")

    filtered_df = apply_filters(df, selections, value_column)

    render_kpi_cards(
        filtered_df=filtered_df,
        value_column=value_column,
        indicator_label=indicator_label,
        selected_year=selected_year
    )

    st.divider()

    st.subheader("Spatial Distribution")
    render_choropleth_map(
        df=filtered_df,
        geojson=load_geojson(),
        value_column=value_column,
        indicator_label=indicator_label,
        selected_year=selected_year
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Ranking")
        tab_top, tab_bottom = st.tabs(["Top 15", "Bottom 15"])

        with tab_top:
            render_ranking_chart(
                df=filtered_df,
                value_column=value_column,
                indicator_label=indicator_label,
                top=True
            )

        with tab_bottom:
            render_ranking_chart(
                df=filtered_df,
                value_column=value_column,
                indicator_label=indicator_label,
                top=False
            )

    with col2:
        st.subheader("Distribution")
        render_distribution_chart(
            df=filtered_df,
            value_column=value_column,
            indicator_label=indicator_label
        )

    st.divider()

    render_island_comparison(
        filtered_df=filtered_df,
        value_column=value_column,
        indicator_label=indicator_label
    )

    if selections["indicator"] == "Stunting":
        st.divider()
        render_stunting_change_ranking(df=df, selections=selections)

# Disable the stunting trend chart; shown descriptively in the header instead
    # render_stunting_trend(df=df, selections=selections)

# Disable to import the data table
    # render_data_table(
    #     df=filtered_df,
    #     value_column=value_column,
    #     indicator_label=indicator_label,
    #     selected_year=selected_year
    # )

    # Adding a footer with a link to the GitHub repository
    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
### Data Sources

- **Child Nutrition Status (2024)**
  Ministry of Health, Republic of Indonesia

- **Administrative Boundary:**
  [Indonesia514 GeoJSON Repository](https://github.com/quarcs-lab/indonesia514)

- **Indonesia514 Project:**
  https://quarcs-lab.github.io/indonesia514/
---
""")

    with col2:
        st.markdown("""
### Version: 1.3

Developed by **Moh. Athoillah**
Graduate School of International Development, Nagoya University
""")


pg = st.navigation([
    st.Page(main, title="Main Dashboard", icon="📊", default=True),
    st.Page("pages/1_Spatial_Analysis.py", title="Spatial Analysis", icon="🗺️"),
])
pg.run()