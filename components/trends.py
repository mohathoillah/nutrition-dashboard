import plotly.express as px
import streamlit as st

from components.charts import render_ranking_chart
from utils.colors import build_categorical_color_groups

STUNTING_YEAR_COLUMNS = {
    "2013": "stunting_2013",
    "2018": "stunting_2018",
    "2024": "stunting_2024"
}

CHANGE_PERIODS = {
    "2013 → 2018": ("stunting_2013", "stunting_2018"),
    "2018 → 2024": ("stunting_2018", "stunting_2024"),
    "2013 → 2024": ("stunting_2013", "stunting_2024")
}


def get_stunting_trend_summary(df, selections):
    region_df = df.copy()

    if selections["islands"]:
        region_df = region_df[region_df["island_en"].isin(selections["islands"])]

    if selections["provinces"]:
        region_df = region_df[region_df["province_en"].isin(selections["provinces"])]

    year_columns = list(STUNTING_YEAR_COLUMNS.values())
    region_df = region_df.dropna(subset=year_columns, how="all")

    if region_df.empty:
        return None

    averages = region_df[year_columns].mean()
    trend_text = " → ".join(
        f"{year}: {averages[column]:.1f}%"
        for year, column in STUNTING_YEAR_COLUMNS.items()
    )

    return f"Stunting trend for the selected region — {trend_text}."


def render_stunting_trend(df, selections):
    st.subheader("Stunting Trend by Province (2013–2024)")

    region_df = df.copy()

    if selections["islands"]:
        region_df = region_df[region_df["island_en"].isin(selections["islands"])]

    if selections["provinces"]:
        region_df = region_df[region_df["province_en"].isin(selections["provinces"])]

    year_columns = list(STUNTING_YEAR_COLUMNS.values())
    region_df = region_df.dropna(subset=year_columns, how="all")

    if region_df.empty:
        st.warning("No data available for the selected filters.")
        return

    province_avg = (
        region_df.groupby("province_en")[year_columns]
        .mean()
        .reset_index()
    )

    trend_df = province_avg.melt(
        id_vars="province_en",
        value_vars=year_columns,
        var_name="year_column",
        value_name="stunting_avg"
    ).dropna(subset=["stunting_avg"])

    year_lookup = {column: year for year, column in STUNTING_YEAR_COLUMNS.items()}
    trend_df["year"] = trend_df["year_column"].map(year_lookup)

    priority_order = (
        province_avg.sort_values("stunting_2024", ascending=False)["province_en"]
        .tolist()
    )
    named_provinces, color_map, category_order = build_categorical_color_groups(
        trend_df["province_en"], priority_order=priority_order
    )
    trend_df = trend_df.assign(
        province_group=trend_df["province_en"].where(
            trend_df["province_en"].isin(named_provinces), "Other"
        )
    )

    fig = px.line(
        trend_df.sort_values("year"),
        x="year",
        y="stunting_avg",
        color="province_group",
        color_discrete_map=color_map,
        category_orders={
            "province_group": category_order,
            "year": list(STUNTING_YEAR_COLUMNS.keys())
        },
        markers=True,
        hover_data=["province_en"],
        labels={
            "year": "Year",
            "stunting_avg": "Average Stunting (%)",
            "province_group": "Province"
        }
    )

    fig.update_layout(
        height=500,
        margin=dict(l=10, r=10, t=20, b=10),
        legend_title_text="Province"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        f"{trend_df['province_en'].nunique()} provinces shown, "
        f"averaged from {region_df['districtID'].nunique()} districts/cities."
    )


def render_stunting_change_ranking(df, selections):
    st.subheader("Stunting Change Ranking")
    st.caption(
        "Compares stunting prevalence between two survey years to find which "
        "districts/cities improved the most (largest decline) and which "
        "worsened the most (largest increase)."
    )

    region_df = df.copy()

    if selections["islands"]:
        region_df = region_df[region_df["island_en"].isin(selections["islands"])]

    if selections["provinces"]:
        region_df = region_df[region_df["province_en"].isin(selections["provinces"])]

    period_label = st.radio(
        "Comparison period",
        options=list(CHANGE_PERIODS.keys()),
        index=2,
        horizontal=True
    )
    start_column, end_column = CHANGE_PERIODS[period_label]

    change_df = region_df.dropna(subset=[start_column, end_column]).copy()

    if change_df.empty:
        st.warning("No data available for the selected filters.")
        return

    change_df["change"] = change_df[end_column] - change_df[start_column]
    axis_label = f"Stunting Change {period_label} (pp)"

    tab_improved, tab_worsened = st.tabs(
        ["Most Improved (largest decline)", "Most Deteriorated (largest increase)"]
    )

    with tab_improved:
        render_ranking_chart(
            df=change_df,
            value_column="change",
            indicator_label="Stunting Change",
            axis_label=axis_label,
            top=False
        )

    with tab_worsened:
        render_ranking_chart(
            df=change_df,
            value_column="change",
            indicator_label="Stunting Change",
            axis_label=axis_label,
            top=True
        )

    st.caption(
        f"Average change {period_label}: {change_df['change'].mean():+.2f} pp "
        f"across {change_df['districtID'].nunique()} districts/cities "
        "(negative = improvement, positive = deterioration)."
    )
