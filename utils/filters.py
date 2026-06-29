import streamlit as st

from config import NUTRITION_OPTIONS


def get_selected_column(selections):
    selected_indicator = selections["indicator"]
    selected_year = selections["year"]

    indicator_config = NUTRITION_OPTIONS[selected_indicator]

    if indicator_config["type"] == "multi_year":
        value_column = indicator_config["columns"][selected_year]
    else:
        value_column = indicator_config["column"]

    return value_column, selected_indicator, selected_year


def apply_filters(df, selections, value_column):
    filtered_df = df.copy()

    if selections["island"] != "All Islands":
        filtered_df = filtered_df[filtered_df["island_en"] == selections["island"]]

    if selections["province"] != "All Provinces":
        filtered_df = filtered_df[filtered_df["province_en"] == selections["province"]]

    if value_column not in filtered_df.columns:
        st.error(f"Column not found: {value_column}")
        st.stop()

    filtered_df = filtered_df.dropna(subset=[value_column])

    st.session_state["color_scale"] = selections["color_scale"]

    return filtered_df
