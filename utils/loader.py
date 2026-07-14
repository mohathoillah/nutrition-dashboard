import json

import pandas as pd
import streamlit as st

from config import DATA_SOURCE, DATA_URL, LOCAL_DATA_PATH, GEOJSON_PATH, BASE_COLUMNS


@st.cache_data
def load_data():
    if DATA_SOURCE == "github":
        df = pd.read_csv(DATA_URL)
    else:
        df = pd.read_csv(LOCAL_DATA_PATH)

    missing = [col for col in BASE_COLUMNS if col not in df.columns]
    if missing:
        st.error(f"Missing required columns: {missing}")
        st.stop()

    return df


@st.cache_data
def load_geojson():
    with open(GEOJSON_PATH) as f:
        return json.load(f)
