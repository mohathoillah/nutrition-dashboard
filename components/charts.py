import plotly.express as px
import streamlit as st

from utils.colors import build_categorical_color_groups


def render_ranking_chart(df, value_column, indicator_label, top=True, axis_label=None):
    if df.empty:
        st.warning("No data available for the selected filters.")
        return

    chart_df = (
        df[["district_en", "province_en", value_column]]
        .dropna(subset=[value_column])
        .sort_values(value_column, ascending=not top)
        .head(15)
        .sort_values(value_column, ascending=True)
    )

    named_provinces, color_map, category_order = build_categorical_color_groups(
        chart_df["province_en"]
    )
    chart_df = chart_df.assign(
        province_group=chart_df["province_en"].where(
            chart_df["province_en"].isin(named_provinces), "Other"
        )
    )

    fig = px.bar(
        chart_df,
        x=value_column,
        y="district_en",
        orientation="h",
        color="province_group",
        color_discrete_map=color_map,
        category_orders={"province_group": category_order},
        hover_data=["province_en"],
        labels={
            value_column: axis_label or f"{indicator_label} (%)",
            "district_en": "District/City",
            "province_group": "Province"
        }
    )

    fig.update_layout(
        height=500,
        margin=dict(l=10, r=10, t=20, b=10),
        yaxis_title=None,
        legend_title_text="Province"
    )

    st.plotly_chart(fig, use_container_width=True)

    rank_word = "highest" if top else "lowest"
    st.caption(
        f"The 15 districts/cities with the {rank_word} {indicator_label} values "
        "among the current filters, colored by province."
    )

    province_counts = chart_df["province_en"].value_counts()
    breakdown = ", ".join(
        f"{province} ({count})" for province, count in province_counts.items()
    )
    st.caption(f"{len(chart_df)} districts/cities shown — {breakdown}")


def render_distribution_chart(df, value_column, indicator_label):
    if df.empty:
        st.warning("No data available for the selected filters.")
        return

    mean_value = df[value_column].mean()
    median_value = df[value_column].median()

    fig = px.histogram(
        df,
        x=value_column,
        nbins=30,
        labels={
            value_column: f"{indicator_label} (%)"
        }
    )

    fig.add_vline(
        x=mean_value,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Mean: {mean_value:.2f}",
        annotation_position="top"
    )

    fig.add_vline(
        x=median_value,
        line_dash="dot",
        line_color="blue",
        annotation_text=f"Median: {median_value:.2f}",
        annotation_position="bottom"
    )

    fig.update_layout(
        height=500,
        margin=dict(l=10, r=10, t=20, b=10),
        yaxis_title="Number of districts/cities"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        f"Distribution of {indicator_label} values across all filtered "
        "districts/cities. Dashed red line marks the mean; dotted blue line "
        "marks the median."
    )
