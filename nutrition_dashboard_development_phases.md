# Nutrition Dashboard Development Phases

This document outlines the next development phases for the Nutrition Status Dashboard after the initial Streamlit setup.

---

# Current Status

The dashboard currently has the basic Phase 1 foundation:

- Streamlit project structure
- Local development environment in VS Code
- GitHub repository workflow
- Basic dashboard app
- Nutrition status data loaded
- Initial filter structure
- Local Streamlit execution

---

# Phase 1 — Exploratory Nutrition Dashboard

## Objective

Build a stable exploratory dashboard for child nutrition status at the district/city level in Indonesia.

## Main Features

### 1. Sidebar Filters

Required filters:

- Nutrition indicator
  - Stunting
  - Underweight
  - Wasting
  - Severe wasting
  - Overweight
- Year filter
  - Only for stunting: 2013, 2018, 2024
- Island filter
- Province filter
- Reset filter button

### 2. KPI Cards

Display summary statistics based on selected filters:

- Mean
- Median
- Minimum
- Maximum
- Number of districts/cities

### 3. Interactive Map

Display district/city-level choropleth map.

Map requirements:

- Darker color = higher prevalence
- Tooltip showing district/city name
- Province
- Selected indicator
- Year
- Value
- National rank

### 4. Ranking Chart

Add ranking visualisation:

- Top 15 districts/cities
- Bottom 15 districts/cities
- Sort by selected nutrition indicator

### 5. Distribution Chart

Show distribution of selected indicator:

- Histogram
- Mean line
- Median line

### 6. Data Table

Add filtered data table:

- District/city name
- Province
- Island
- Selected indicator value
- Rank
- Download CSV button

## Phase 1 Output

A clean, stable, and interactive dashboard for basic exploratory analysis.

---

# Phase 2 — Comparative Analytics

## Objective

Add comparative analysis across districts, provinces, islands, and indicators.

## Main Features

### 1. Province Comparison

- Average indicator by province
- Top and bottom provinces
- Province-level ranking chart

### 2. Island Comparison

- Average indicator by island
- Island-level bar chart
- Comparison across Java, Sumatra, Kalimantan, Sulawesi, Bali-Nusa Tenggara, Maluku, Papua

### 3. Indicator Comparison

Add charts comparing:

- Stunting vs underweight
- Stunting vs wasting
- Underweight vs wasting
- Wasting vs overweight

### 4. Correlation Matrix

Add correlation matrix among nutrition indicators:

- Stunting
- Underweight
- Wasting
- Severe wasting
- Overweight

## Phase 2 Output

The dashboard can be used not only to inspect one indicator, but also to compare patterns across indicators and regions.

---

# Phase 3 — Stunting Trend Dashboard

## Objective

Use multi-year stunting data to analyze changes over time.

## Main Features

### 1. National Trend

Show average stunting prevalence for:

- 2013
- 2018
- 2024

### 2. Provincial Trend

Allow user to select province and view stunting trend.

### 3. District/City Trend

Allow user to select district/city and view stunting trend.

### 4. Change Analysis

Calculate:

- Change from 2013 to 2018
- Change from 2018 to 2024
- Change from 2013 to 2024

### 5. Improvement and Deterioration Ranking

Show:

- Districts/cities with largest decline in stunting
- Districts/cities with largest increase in stunting

## Phase 3 Output

The dashboard can identify where stunting improved, worsened, or remained persistent.

---

# Phase 4 — Spatial Analysis Dashboard

## Objective

Add exploratory spatial data analysis to detect geographic clustering.

## Main Features

### 1. Spatial Weight Matrix

Options:

- Queen contiguity
- Rook contiguity
- K-nearest neighbors
- Distance-based weights

### 2. Global Moran's I

Display:

- Moran's I statistic
- Expected value
- P-value
- Interpretation

### 3. LISA Cluster Map

Classify districts/cities into:

- High-High
- Low-Low
- High-Low
- Low-High
- Not significant

### 4. Hotspot Analysis

Identify spatial hotspots of high nutrition risk.

### 5. Neighbor Explorer

Allow user to select one district/city and inspect neighboring districts/cities.

## Phase 4 Output

The dashboard can detect spatial clustering and identify priority geographic areas.

---

# Phase 5 — Risk Factor Integration

## Objective

Integrate nutrition outcomes with possible risk factors.

## Candidate Risk Factors

- Poverty rate
- Food consumption inadequacy
- Food insecurity
- Socioeconomic vulnerability
- Population characteristics

## Main Features

### 1. Risk Factor Map

Map each risk factor independently.

### 2. Scatter Analysis

Examples:

- Stunting vs poverty
- Stunting vs food consumption inadequacy
- Underweight vs poverty
- Wasting vs food insecurity

### 3. Correlation Summary

Show pairwise correlations between nutrition indicators and risk factors.

### 4. Vulnerability Typology

Classify districts/cities into:

- High nutrition risk, high poverty
- High nutrition risk, low poverty
- Low nutrition risk, high poverty
- Low nutrition risk, low poverty

## Phase 5 Output

The dashboard can support preliminary policy-oriented diagnosis.

---

# Phase 6 — Composite Index and CIAF

## Objective

Develop composite measures of child nutrition failure and vulnerability.

## Main Features

### 1. CIAF Module

If microdata are available, construct:

- No failure
- Wasting only
- Underweight only
- Stunting only
- Wasting and underweight
- Stunting and underweight
- Stunting, wasting, and underweight

### 2. Composite Nutrition Risk Index

Possible indicators:

- Stunting
- Underweight
- Wasting
- Severe wasting
- Overweight

### 3. Normalization Options

- Min-max normalization
- Z-score normalization
- Rank-based scoring

### 4. Composite Map

Map the composite nutrition risk index by district/city.

## Phase 6 Output

The dashboard can summarize multidimensional nutrition risk, not only single indicators.

---

# Phase 7 — Export and Reporting

## Objective

Make the dashboard useful for research presentation and reporting.

## Main Features

### 1. Export Data

- Download filtered data as CSV
- Download province summary
- Download district ranking

### 2. Export Figures

- Export map
- Export charts
- Export ranking tables

### 3. Auto-generated Summary

Generate short text summaries such as:

- Highest-risk districts/cities
- Provinces with highest average prevalence
- Main spatial patterns
- Main trend findings

### 4. Documentation Page

Add an About or Metadata page explaining:

- Data source
- Variable definitions
- Year coverage
- Limitations
- Citation

## Phase 7 Output

The dashboard becomes usable for presentations, reports, and research communication.

---

# Recommended Implementation Order

## Short-Term Priority

1. Finish Phase 1
2. Deploy Phase 1 to Streamlit Community Cloud
3. Improve UI and stability
4. Add province and island comparison
5. Add stunting trend analysis

## Medium-Term Priority

1. Add correlation analysis
2. Add spatial analysis
3. Add risk factor integration

## Long-Term Priority

1. Add composite index
2. Add CIAF module
3. Add reporting and export tools

---

# Git Workflow for Each Phase

For each phase:

1. Create or edit code in VS Code
2. Test locally using:

```powershell
py -m streamlit run app.py
```

3. Commit changes in GitHub Desktop
4. Push to GitHub
5. Check Streamlit Cloud deployment
6. Fix errors if needed
7. Continue to the next sprint

---

# Suggested Commit Messages

## Phase 1

```text
Add sidebar filters
Add KPI cards
Add choropleth map
Add ranking chart
Add distribution chart
Add data table
Prepare Phase 1 deployment
```

## Phase 2

```text
Add province comparison
Add island comparison
Add nutrition indicator comparison
Add correlation matrix
```

## Phase 3

```text
Add stunting trend module
Add district trend view
Add stunting change ranking
```

## Phase 4

```text
Add spatial weights
Add Moran I analysis
Add LISA cluster map
Add hotspot analysis
```

## Phase 5

```text
Add poverty data integration
Add food insecurity data integration
Add nutrition risk typology
```

## Phase 6

```text
Add composite nutrition index
Add CIAF module
Add composite risk map
```

## Phase 7

```text
Add export tools
Add auto-generated summary
Add metadata page
```
