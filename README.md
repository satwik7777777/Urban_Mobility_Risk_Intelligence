# Urban Mobility Risk Intelligence

Bengaluru road crash analysis and risk intelligence dashboard using crash data from 2018–2025.
## Live Dashboard

[Open the live dashboard](https://urbanmobilityriskintelligence-257bsrotgsjpl9sqp6frl3.streamlit.app/)

## About the Project

This project analyzes road crash data across Bengaluru police stations to understand how crash activity changes over time and which locations show higher levels of risk.

The project combines data analysis, station-level risk scoring, trend analysis, geospatial visualization and a simple 2026 predictive outlook in a Streamlit dashboard.

## What the Project Covers

- City-wide crash trends from 2018 to 2025
- Station-level crash and fatal crash analysis
- Crash severity comparison
- Historical and recent crash activity
- Station-level risk scoring
- Interactive Bengaluru risk map
- 2026 crash outlook for stations with continuous historical data

## Dashboard

The dashboard contains six sections:

1. **Overview** – Overall project statistics and key findings
2. **Crash Trends** – Year-wise crash trends and changes
3. **Risk Intelligence** – Station-level risk and severity analysis
4. **Risk Map** – Interactive map of station risk
5. **Predictive Risk** – 2026 station-level crash outlook
6. **Summary & Results** – Main findings and limitations

## Risk Scoring

The station risk score combines:

- Historical crash frequency
- Historical fatal crash activity
- Crash severity
- Recent crash activity
- Recent fatal crash activity

Stations are classified into:

- **High Risk**
- **Medium Risk**
- **Low Risk**

The score is intended for relative comparison between stations and is not an accident probability.

## Predictive Analysis

The predictive analysis was tested using stations with continuous data from 2018–2025.

Three simple forecasting approaches were compared:

| Method | MAE | RMSE |
| --- | ---: | ---: |
| Last Year | 21.41 | 31.66 |
| 3-Year Moving Average | 23.68 | 34.56 |
| Linear Trend | 27.47 | 41.06 |

The Last Year baseline performed best on the validation data and was used for the 2026 outlook.

The predictive results should be treated as an analytical outlook rather than an exact prediction of future accidents.

## Data

The analysis covers Bengaluru station-level crash data for 2018–2025.

There are differences in station coverage across years. Because of this, raw totals are not directly compared between stations with very different numbers of available years.

For the predictive analysis, only stations with continuous 2018–2025 data were used.

## Tech Stack

- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- Folium
- Streamlit-Folium
- Scikit-learn
- Geopy
- OSMnx
- Jupyter Notebook

## Project Structure

```text
Urban_Mobility_Risk_Intelligence/
│
├── dashboard/
│   ├── app.py
│   └── pages/
│       ├── 1_📊_Overview.py
│       ├── 2_📈_Crash_Trends.py
│       ├── 3_⚠️_Risk_Intelligence.py
│       ├── 4_🗺️_Risk_Map.py
│       ├── 5_🔮_Predictive_Risk.py
│       └── 6_📋_Summary_Results.py
│
├── data/
├── DATA FILES/
├── notebooks/
├── processed/
├── requirements.txt
└── README.md
