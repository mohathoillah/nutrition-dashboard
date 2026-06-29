import streamlit as st


def render_data_table(df, value_column, indicator_label, selected_year):
    st.subheader(f"Top 15 Districts/Cities by {indicator_label}")

    if df.empty:
        st.warning("No data available for the selected filters.")
        return

    table_df = (
        df[
            [
                "district_en",
                "province_en",
                "island_en",
                value_column,
            ]
        ]
        .rename(
            columns={
                "district_en": "District/City",
                "province_en": "Province",
                "island_en": "Island",
                value_column: f"{indicator_label} {selected_year} (%)",
            }
        )
        .sort_values(
            by=f"{indicator_label} {selected_year} (%)",
            ascending=False,
        )
        .head(15)
        .reset_index(drop=True)
    )

    table_df.insert(0, "Rank", table_df.index + 1)

    st.dataframe(
        table_df,
        width="stretch",
        hide_index=True,
    )