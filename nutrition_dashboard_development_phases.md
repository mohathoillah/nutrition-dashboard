# Nutrition Dashboard Development Phases

This document outlines the next development phases for the Nutrition Status Dashboard after the initial Streamlit setup.

---

# Current Status

_Last reviewed: 2026-07-07 (Spatial Analysis moved to its own page)._

Phase 1 is functionally complete and deployed locally (v1.1), with some
deliberate deviations from the original spec (see notes inline below). Parts
of Phase 2, Phase 3, and now Phase 4 have also been pulled forward since they
were cheap to build on top of the existing data, or — for Phase 4 — because
Stunting is the only indicator with multi-year data worth analyzing
spatially, and the user chose to jump ahead to it directly (skipping the
remaining Phase 2/3 gaps for now):

- Streamlit project structure, local dev environment, GitHub workflow
- Full Phase 1 feature set (filters, KPI cards, map, ranking, distribution) —
  see Phase 1 notes for deviations
- From Phase 2: Island Comparison (2.2) is done
- From Phase 3: Change Analysis (3.4) and Improvement/Deterioration Ranking
  (3.5) are done, combined into one "Stunting Change Ranking" section;
  National Trend (3.1) and Provincial Trend (3.2) were built but are
  currently disabled by request (see Phase 3 notes)
- From Phase 4: all five sub-features (Spatial Weight Matrix, Global Moran's
  I, LISA Cluster Map, Hotspot Analysis, Neighbor Explorer) are done, scoped
  to Stunting only, on its own page (`pages/1_Spatial_Analysis.py`) — see
  Phase 4 notes
- Still open: Province Comparison (2.1), Indicator Comparison (2.3),
  Correlation Matrix (2.4), District/City Trend (3.3)

---

# Phase 1 — Exploratory Nutrition Dashboard

**Status: ✅ Done (with deviations noted below)**

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

> **Deviation:** Island and Province are multi-select (not single-select), and
> all filters sit inside an "Apply Filters" form so nothing recomputes until
> the user submits — this wasn't in the original spec but was requested to
> avoid re-rendering on every widget tweak.

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

> **Note:** Was temporarily disabled to speed up page load, then re-enabled.
> National rank is computed from the full national dataset (not the filtered
> subset), so it stays accurate regardless of active island/province filters.

### 4. Ranking Chart

Add ranking visualisation:

- Top 15 districts/cities
- Bottom 15 districts/cities
- Sort by selected nutrition indicator

> **Enhancement:** Bars are colored by province (validated 8-color categorical
> palette, overflow folds into a gray "Other" bucket), with a caption showing
> the per-province district count breakdown.

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

> **Deviation:** Intentionally disabled per user decision (2026-07-06). The
> component (`components/tables.py`) is fully built and spec-complete
> (including the rank column) but not wired into `app.py`. Re-enable only if
> asked again — it was toggled on/off several times in git history before
> settling on "off."

## Phase 1 Output

A clean, stable, and interactive dashboard for basic exploratory analysis.

---

# Phase 2 — Comparative Analytics

**Status: 🟡 Partially done — Island Comparison shipped, rest not started**

## Objective

Add comparative analysis across districts, provinces, islands, and indicators.

## Main Features

### 1. Province Comparison

**Status: Not started.**

- Average indicator by province
- Top and bottom provinces
- Province-level ranking chart

Note: the existing district-level ranking chart (Phase 1.4) already colors
bars by province, which covers part of the visual grouping need, but there is
no dedicated province-aggregated bar/ranking chart yet — this is the next
logical quick win, reusing the same groupby pattern as Island Comparison.

### 2. Island Comparison

**Status: ✅ Done** (`components/comparisons.py`)

- Average indicator by island
- Island-level bar chart
- Comparison across Java, Sumatera, Kalimantan, Sulawesi, Bali-Nusa Tenggara, Maluku, Papua

Works for whichever nutrition indicator is currently selected in the sidebar
(not stunting-only), and respects the active island/province filters.

### 3. Indicator Comparison

**Status: Not started.**

Add charts comparing:

- Stunting vs underweight
- Stunting vs wasting
- Underweight vs wasting
- Wasting vs overweight

Quick win: all five indicators already share a common 2024 snapshot in the
loaded data, so this needs no new data — just scatter plots between column
pairs.

### 4. Correlation Matrix

**Status: Not started.**

Add correlation matrix among nutrition indicators:

- Stunting
- Underweight
- Wasting
- Severe wasting
- Overweight

Quick win, same reason as above — one `df.corr()` call plus a heatmap.

## Phase 2 Output

The dashboard can be used not only to inspect one indicator, but also to compare patterns across indicators and regions.

---

# Phase 3 — Stunting Trend Dashboard

**Status: 🟡 Partially done — 3.1/3.2 built but disabled, 3.4/3.5 shipped, 3.3 not started**

## Objective

Use multi-year stunting data to analyze changes over time.

## Main Features

### 1. National Trend

**Status: Built, currently disabled.**

Show average stunting prevalence for:

- 2013
- 2018
- 2024

A one-line text summary of this (e.g. "2013: 41.2% → 2018: 33.1% → 2024:
27.8%") was added under the indicator description, then removed per user
request (2026-07-06) — the user wants the top-of-page description area kept
free of stunting-specific content.

### 2. Provincial Trend

**Status: Built, currently disabled.**

Allow user to select province and view stunting trend.

Implemented as `render_stunting_trend()` in `components/trends.py` — a line
chart of average stunting per province across 2013/2018/2024, highlighting
the top 8 highest-2024-stunting provinces in color and graying out the rest.
Disabled in `app.py` (commented out) per user request in favor of the
descriptive-text approach above, which was then also removed. The function is
intact and ready to re-enable if wanted again.

### 3. District/City Trend

**Status: Not started.**

Allow user to select district/city and view stunting trend.

Needs a new selectbox (district picker) — otherwise the same line-chart
pattern as Provincial Trend, just at finer granularity.

### 4. Change Analysis

**Status: ✅ Done**, combined with 3.5 below.

Calculate:

- Change from 2013 to 2018
- Change from 2018 to 2024
- Change from 2013 to 2024

### 5. Improvement and Deterioration Ranking

**Status: ✅ Done** — `render_stunting_change_ranking()` in `components/trends.py`.

Show:

- Districts/cities with largest decline in stunting
- Districts/cities with largest increase in stunting

Implemented as one "Stunting Change Ranking" section: a radio button picks
the comparison period (2013→2018, 2018→2024, 2013→2024), then two tabs show
Top-15 "Most Improved" and "Most Deteriorated" district rankings, plus a
caption with the average change. Only shown when the sidebar's Nutrition
status is set to Stunting (hidden for other indicators, since they have no
multi-year data).

## Phase 3 Output

The dashboard can identify where stunting improved, worsened, or remained persistent.

---

# Phase 4 — Spatial Analysis Dashboard

**Status: ✅ Done, scoped to Stunting only** — `utils/spatial.py` +
`components/spatial.py`. Originally wired into `app.py` directly below
Stunting Change Ranking; moved on 2026-07-07 to its own page,
`pages/1_Spatial_Analysis.py`, via Streamlit's native multi-page app
support (the `pages/` directory convention). Reason for the move: since
this section ignores the sidebar's island/province filters anyway (it
always operates on the full national dataset), it didn't need to live on
the same page as the filtered main dashboard — and keeping it there meant
its heavy map figures got rebuilt/reserialized on every rerun triggered by
unrelated sidebar interactions. As a separate page, it only loads/computes
when the user actually navigates to it.

Built ahead of the remaining Phase 2/3 gaps per user request (2026-07-07):
Stunting is the only indicator with multi-year data (2013/2018/2024), so it's
the only one worth analyzing spatially over time right now. All spatial
statistics (weights, Moran's I, LISA, Getis-Ord Gi*) are computed on the full
national 514-district dataset, independent of the main dashboard's
island/province filters — mirroring the existing `national_rank` pattern —
so contiguity relationships aren't cut off at a filter boundary. The page
has its own controls: a year radio (2013/2018/2024) and a weight-matrix
method selectbox, decoupled from the main page's own year selector.

New dependencies: `geopandas`, `libpysal`, `esda`.

## Objective

Add exploratory spatial data analysis to detect geographic clustering.

## Main Features

### 1. Spatial Weight Matrix

**Status: ✅ Done.** All four options implemented via `libpysal`, selectable
in the UI:

- Queen contiguity
- Rook contiguity
- K-nearest neighbors (k slider, 4–10, default 8)
- Distance-based weights (threshold slider, 50–500km, default 200km, using
  great-circle/arc distance between district representative points)

Indonesia's archipelago geography means Queen/Rook contiguity leaves ~33
districts as isolates (small/remote islands with no shared land border) —
surfaced to the user as a warning with a suggestion to switch to
KNN/Distance-band if every unit needs at least one neighbor.

### 2. Global Moran's I

**Status: ✅ Done.** Displays Moran's I, Expected I, z-score, and p-value
(999 permutations), plus an auto-generated interpretation sentence. Observed
values on 2024 stunting are strongly significant (I ≈ 0.43–0.52 depending on
weight method, p = 0.001), consistent with known regional clustering of
stunting in eastern Indonesia.

### 3. LISA Cluster Map

**Status: ✅ Done.** Classifies each district into High-High, Low-High,
Low-Low, High-Low, Not Significant (p ≥ 0.05), or No Neighbors (isolates
under contiguity weights) — shown as a categorical choropleth map.

### 4. Hotspot Analysis

**Status: ✅ Done.** Getis-Ord Gi* (with the location itself included, i.e.
Gi*, not Gi), classified into Hot Spot / Cold Spot at 90/95/99% confidence,
Not Significant, or No Neighbors — shown as a categorical choropleth map.

### 5. Neighbor Explorer

**Status: ✅ Done.** District/city selectbox, a table of its neighbors under
the current weight matrix, and a map highlighting the selected district and
its neighbors against the rest of the country.

> **Performance note:** the district boundary GeoJSON is a full-resolution
> coastline file (~54MB parsed). Rendering it directly for 3 additional
> categorical maps (LISA, hotspot, neighbor explorer) on top of the existing
> national map made every full-page rerun extremely slow (a single
> uncached choropleth figure serialized to ~225MB). Fixed by simplifying
> geometry (Douglas-Peucker, tolerance ≈ 0.01°/~1.1km, `preserve_topology`)
> for the three new **display** maps only — weight construction
> (Queen/Rook/KNN/Distance-band) still uses full-precision geometry so
> adjacency results are unaffected. This cut the map payload to ~3.7MB.
> Each unique (year, weight method, k/threshold) combination is cached via
> `st.cache_resource`, so the ~10–30s cost (permutation-based Moran/LISA/Gi*
> on 514 units, plus first-time geometry simplification) is only paid once
> per combination per session, not on every rerun.

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

_Updated 2026-07-07 to reflect actual progress — see Phase 1–4 status notes above._

## Short-Term Priority

1. ✅ Finish Phase 1
2. ⬜ Deploy Phase 1 to Streamlit Community Cloud — not done yet
3. 🟡 Improve UI and stability — ongoing (header color, section descriptions added)
4. 🟡 Add province and island comparison — island done, province not started
5. 🟡 Add stunting trend analysis — change/ranking done, trend charts built but disabled

## Medium-Term Priority

1. ⬜ Add correlation analysis — not started (quick win, no new data needed)
2. ✅ Add spatial analysis — done, scoped to Stunting only (see Phase 4)
3. ⬜ Add risk factor integration

## Long-Term Priority

1. ⬜ Add composite index
2. ⬜ Add CIAF module
3. ⬜ Add reporting and export tools

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
