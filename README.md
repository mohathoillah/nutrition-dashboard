# Nutrition Dashboard Phase 1

This is a modular Streamlit dashboard for exploratory analysis of child nutrition status in Indonesia.

## Phase 1 features

- Nutrition status filter:
  - Stunting
  - Underweight
  - Severe Wasting
  - Wasting
  - Overweight
- Year filter for stunting:
  - 2013
  - 2018
  - 2024
- Island filter
- Province filter
- KPI cards
- Interactive choropleth map
- Top 15 district/city ranking
- Distribution chart
- Data table
- CSV download

## Project structure

```text
nutrition-dashboard-phase1/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── data/
│   └── stunting_spatial.csv
├── components/
│   ├── sidebar.py
│   ├── kpi_cards.py
│   ├── map.py
│   ├── charts.py
│   └── tables.py
├── utils/
│   ├── loader.py
│   └── filters.py
└── .streamlit/
    └── config.toml
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Use GitHub Raw data source

By default, the dashboard reads:

```python
LOCAL_DATA_PATH = "data/stunting_spatial.csv"
```

To read the CSV from GitHub Raw URL, edit `config.py`:

```python
DATA_SOURCE = "github"
DATA_URL = "https://raw.githubusercontent.com/<USERNAME>/<REPO>/main/data/stunting_spatial.csv"
```

## Required columns

```text
districtID
district_en
province_en
island_en
underweight_2024
severe_wasting_2024
wasting_2024
overweight_2024
stunting_2013
stunting_2018
stunting_2024
```
