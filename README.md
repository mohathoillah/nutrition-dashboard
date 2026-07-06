# Nutrition Dashboard

A modular Streamlit dashboard for exploratory analysis of child nutrition status in Indonesia. Development follows the phased plan in [nutrition_dashboard_development_phases.md](nutrition_dashboard_development_phases.md) — see that file for detailed status per phase.

## Current features (v1.1)

**Filters (sidebar, applied via an "Apply Filters" button):**

- Nutrition status: Stunting, Underweight, Wasting, Severe Wasting, Overweight
- Year filter for Stunting: 2013, 2018, 2024
- Island filter (multi-select)
- Province filter (multi-select)
- Map color scale picker
- Reset filters button

**Main view:**

- Per-indicator description (WHO-based definitions) shown under the title
- KPI cards: average, median, highest, lowest, number of districts/cities
- Interactive choropleth map, with district/province/value/national rank in the tooltip
- Ranking chart: Top 15 / Bottom 15 tabs, bars colored by province
- Distribution histogram with mean/median reference lines
- Island comparison: average indicator value per island

**Stunting-specific (shown only when Stunting is the selected indicator):**

- Stunting Change Ranking: pick a comparison period (2013→2018, 2018→2024, 2013→2024), see Top-15 "Most Improved" and "Most Deteriorated" districts/cities

**Currently disabled (built, not wired into the app):**

- Data table with CSV download (`components/tables.py`) — intentionally left off
- Provincial stunting trend line chart (`render_stunting_trend` in `components/trends.py`) — kept in code for future use

## Project structure

```text
nutrition-dashboard/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── nutrition_dashboard_development_phases.md
├── data/
│   └── stunting_spatial.csv
├── components/
│   ├── sidebar.py
│   ├── kpi_cards.py
│   ├── map.py
│   ├── charts.py
│   ├── comparisons.py
│   ├── trends.py
│   └── tables.py
├── utils/
│   ├── loader.py
│   ├── filters.py
│   └── colors.py
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

## Data Sources

- **Child Nutrition Status (2024)** — Ministry of Health, Republic of Indonesia
- **Administrative Boundary** — [Indonesia514 GeoJSON Repository](https://github.com/quarcs-lab/indonesia514)
- **Indonesia514 Project** — https://quarcs-lab.github.io/indonesia514/

Developed by **Moh. Athoillah**, Graduate School of International Development, Nagoya University.
