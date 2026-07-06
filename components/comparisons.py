import plotly.express as px
import streamlit as st

from utils.colors import build_categorical_color_groups


def render_island_comparison(filtered_df, value_column, indicator_label):
    st.subheader("Island Comparison")

    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
        return

    island_avg = (
        filtered_df.groupby("island_en")[value_column]
        .mean()
        .reset_index()
        .sort_values(value_column, ascending=False)
    )

    _, color_map, category_order = build_categorical_color_groups(
        island_avg["island_en"]
    )

    fig = px.bar(
        island_avg,
        x="island_en",
        y=value_column,
        color="island_en",
        color_discrete_map=color_map,
        category_orders={"island_en": category_order},
        labels={
            value_column: f"{indicator_label} (%)",
            "island_en": "Island"
        }
    )

    fig.update_layout(
        height=450,
        margin=dict(l=10, r=10, t=20, b=10),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        f"Average {indicator_label} value per island, aggregated across its "
        "districts/cities, sorted from highest to lowest."
    )
    st.caption(
        f"{filtered_df['districtID'].nunique()} districts/cities across "
        f"{island_avg['island_en'].nunique()} islands."
    )
