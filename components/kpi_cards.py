import streamlit as st


def render_kpi_cards(filtered_df, value_column, indicator_label, selected_year):
    col1, col2, col3, col4 = st.columns(4)

    if filtered_df.empty:
        col1.metric(f"Average {indicator_label}", "N/A")
        col2.metric("Highest Value", "N/A")
        col3.metric("Lowest Value", "N/A")
        col4.metric("Districts/Cities", "0")
        return

    avg_value = filtered_df[value_column].mean()
    max_value = filtered_df[value_column].max()
    min_value = filtered_df[value_column].min()
    total_districts = filtered_df["districtID"].nunique()

    col1.metric(
        f"Average {indicator_label} ({selected_year})",
        f"{avg_value:.2f}%"
    )

    col2.metric(
        "Highest Value",
        f"{max_value:.2f}%"
    )

    col3.metric(
        "Lowest Value",
        f"{min_value:.2f}%"
    )

    col4.metric(
        "Districts/Cities",
        f"{total_districts:,}"
    )
