import streamlit as st

from components.sidebar import render_sidebar
from components.kpi_cards import render_kpi_cards
from components.charts import render_distribution_chart, render_ranking_chart
from components.tables import render_data_table
from components.map import render_choropleth_map
from utils.loader import load_data, load_geojson
from utils.filters import apply_filters, get_selected_column


st.set_page_config(
    page_title="Nutrition Status Dashboard",
    page_icon="📊",
    layout="wide"
)


def main():
    st.title("Nutrition Status Dashboard in Indonesia")
    st.caption(
        "Phase 1: exploratory dashboard for child nutrition status "
        "at district/city level."
    )

    df = load_data()
    geojson = load_geojson()

    selections = render_sidebar(df)
    value_column, indicator_label, selected_year = get_selected_column(selections)
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
        geojson=geojson,
        value_column=value_column,
        indicator_label=indicator_label,
        selected_year=selected_year
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 15 Districts/Cities")
        render_ranking_chart(
            df=filtered_df,
            value_column=value_column,
            indicator_label=indicator_label
        )

    with col2:
        st.subheader("Distribution")
        render_distribution_chart(
            df=filtered_df,
            value_column=value_column,
            indicator_label=indicator_label
        )

    st.divider()

    render_data_table(
        df=filtered_df,
        value_column=value_column,
        indicator_label=indicator_label,
        selected_year=selected_year
    )


if __name__ == "__main__":
    main()
