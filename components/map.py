import plotly.graph_objects as go
import streamlit as st


def render_choropleth_map(
    df,
    geojson,
    value_column,
    indicator_label,
    selected_year
):
    if df.empty:
        st.warning("No data available for the selected filters.")
        return

    hover_text = (
        df["district_en"].astype(str)
        + ", "
        + df["province_en"].astype(str)
        + "<br>"
        + indicator_label
        + " "
        + str(selected_year)
        + ": "
        + df[value_column].round(2).astype(str)
        + "%"
    )

    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=geojson,
            locations=df["district_en"],
            z=df[value_column],
            featureidkey="properties.district_en",
            colorscale=st.session_state.get("color_scale", "YlOrRd"),
            reversescale=False,
            marker_opacity=0.85,
            marker_line_width=0.2,
            text=hover_text,
            hoverinfo="text",
            colorbar_title=f"{indicator_label} (%)"
        )
    )

    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=3.5,
        mapbox_center={"lat": -2.5, "lon": 118},
        height=650,
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

    st.plotly_chart(fig, use_container_width=True)
