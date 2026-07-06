import streamlit as st


def render_data_table(df, value_column, indicator_label, selected_year):
    st.subheader("Data Table")

    if df.empty:
        st.warning("No data available for the selected filters.")
        return

    table_df = df[
        [
            "districtID",
            "district_en",
            "province_en",
            "island_en",
            value_column,
            "national_rank"
        ]
    ].rename(
        columns={
            "districtID": "District ID",
            "district_en": "District/City",
            "province_en": "Province",
            "island_en": "Island",
            value_column: f"{indicator_label} {selected_year} (%)",
            "national_rank": "National Rank"
        }
    )

    st.dataframe(
        table_df.sort_values(f"{indicator_label} {selected_year} (%)", ascending=False),
        use_container_width=True,
        hide_index=True
    )

#    csv = table_df.to_csv(index=False).encode("utf-8")

# Disable the download button for now, as it may not be necessary for the current use case
#    st.download_button(
#         label="Download filtered data as CSV",
#         data=csv,
#         file_name=f"{indicator_label.lower().replace(' ', '_')}_{selected_year}_filtered.csv",
#         mime="text/csv"
#     )
