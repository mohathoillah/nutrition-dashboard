# -----------------------------
# Data source
# -----------------------------
# Use "local" when the CSV is stored in the repository under data/.
# Use "github" when the CSV should be read from a GitHub Raw URL.

DATA_SOURCE = "local"

LOCAL_DATA_PATH = "data/stunting_spatial.csv"

DATA_URL = "https://raw.githubusercontent.com/<USERNAME>/<REPO>/main/data/stunting_spatial.csv"

GEOJSON_URL = "https://raw.githubusercontent.com/quarcs-lab/indonesia514/main/maps/mapIndonesia514_new.geojson"


# -----------------------------
# Dashboard options
# -----------------------------
NUTRITION_OPTIONS = {
    "Stunting": {
        "type": "multi_year",
        "columns": {
            "2013": "stunting_2013",
            "2018": "stunting_2018",
            "2024": "stunting_2024"
        }
    },
    "Underweight": {
        "type": "single_year",
        "year": "2024",
        "column": "underweight_2024"
    },
    "Severe Wasting": {
        "type": "single_year",
        "year": "2024",
        "column": "severe_wasting_2024"
    },
    "Wasting": {
        "type": "single_year",
        "year": "2024",
        "column": "wasting_2024"
    },
    "Overweight": {
        "type": "single_year",
        "year": "2024",
        "column": "overweight_2024"
    }
}

BASE_COLUMNS = [
    "districtID",
    "district_en",
    "province_en",
    "island_en"
]
