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

NUTRITION_DEFINITIONS = {
    "Stunting": (
        "Stunting reflects chronic malnutrition, measured as height-for-age "
        "below -2 SD from the WHO Child Growth Standards median. It signals "
        "long-term inadequate nutrition, repeated infection, or poor "
        "psychosocial stimulation during early childhood."
    ),
    "Underweight": (
        "Underweight is measured as weight-for-age below -2 SD from the WHO "
        "median. It captures a mix of both chronic (stunting-like) and acute "
        "(wasting-like) undernutrition."
    ),
    "Wasting": (
        "Wasting reflects acute malnutrition, measured as weight-for-height "
        "below -2 SD from the WHO median. It often signals recent and severe "
        "weight loss due to illness or inadequate food intake."
    ),
    "Severe Wasting": (
        "Severe Wasting is weight-for-height below -3 SD from the WHO "
        "median, indicating a life-threatening form of acute malnutrition "
        "that requires urgent treatment."
    ),
    "Overweight": (
        "Overweight is measured as weight-for-height above +2 SD from the "
        "WHO median, reflecting excess weight relative to height among "
        "children under five."
    )
}

BASE_COLUMNS = [
    "districtID",
    "district_en",
    "province_en",
    "island_en"
]
