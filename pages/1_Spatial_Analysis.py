import streamlit as st

from components.spatial import render_spatial_analysis

st.title("Spatial Analysis")
st.caption(
    "Spatial autocorrelation and clustering analysis for stunting prevalence "
    "across Indonesia's 514 districts/cities."
)

render_spatial_analysis()
