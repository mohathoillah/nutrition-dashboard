import plotly.express as px
import streamlit as st


def render_ranking_chart(df, value_column, indicator_label):
    if df.empty:
        st.warning("No data available for the selected filters.")
        return

    chart_df = (
        df[["district_en", "province_en", value_column]]
        .dropna(subset=[value_column])
        .sort_values(value_column, ascending=False)
        .head(15)
        .sort_values(value_column, ascending=True)
    )

    fig = px.bar(
        chart_df,
        x=value_column,
        y="district_en",
        orientation="h",
        hover_data=["province_en"],
        labels={
            value_column: f"{indicator_label} (%)",
            "district_en": "District/City"
        }
    )

    fig.update_layout(
        height=500,
        margin=dict(l=10, r=10, t=20, b=10),
        yaxis_title=None
    )

    st.plotly_chart(fig, use_container_width=True)


def render_distribution_chart(df, value_column, indicator_label):
    if df.empty:
        st.warning("No data available for the selected filters.")
        return

    fig = px.histogram(
        df,
        x=value_column,
        nbins=30,
        labels={
            value_column: f"{indicator_label} (%)"
        }
    )

    fig.update_layout(
        height=500,
        margin=dict(l=10, r=10, t=20, b=10),
        yaxis_title="Number of districts/cities"
    )

    st.plotly_chart(fig, use_container_width=True)
