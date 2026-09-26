import base64
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Predictive Risk | Urban Mobility Risk Intelligence",
    page_icon="🔮",
    layout="wide"
)


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_PATH = PROJECT_ROOT / "processed"

predictive_file = PROCESSED_PATH / "predictive_risk_2026.csv"


# ============================================================
# LOAD DATA
# ============================================================

predictive_df = pd.read_csv(predictive_file)


# ============================================================
# COLUMN NAMES FROM ACTUAL CSV
# ============================================================

STATION = "station"
ACTUAL_2025 = "actual_2025_crashes"
FORECAST_2026 = "predicted_2026_crashes"
TREND = "recent_trend_per_year"

RISK_SCORE = "risk_score"
RISK_CATEGORY = "risk_category"

OUTLOOK_INDEX = "predictive_outlook_index"
OUTLOOK_CATEGORY = "predictive_outlook"


# ============================================================
# BASIC CALCULATIONS
# ============================================================

total_stations = predictive_df[STATION].nunique()

critical_count = (
    predictive_df[OUTLOOK_CATEGORY]
    .astype(str)
    .str.contains("Critical", case=False, na=False)
    .sum()
)

high_count = (
    predictive_df[OUTLOOK_CATEGORY]
    .astype(str)
    .str.fullmatch("High", case=False, na=False)
    .sum()
)

moderate_count = (
    predictive_df[OUTLOOK_CATEGORY]
    .astype(str)
    .str.fullmatch("Moderate", case=False, na=False)
    .sum()
)

lower_count = (
    predictive_df[OUTLOOK_CATEGORY]
    .astype(str)
    .str.contains("Lower", case=False, na=False)
    .sum()
)

increasing_count = (
    predictive_df[TREND] > 0
).sum()

average_forecast = predictive_df[
    FORECAST_2026
].mean()


# ============================================================
# SORTED DATA
# ============================================================

top_predictive = (
    predictive_df
    .sort_values(
        OUTLOOK_INDEX,
        ascending=False
    )
    .reset_index(drop=True)
)


# ============================================================
# BACKGROUND ARTWORK
# ============================================================

SCRIPT_DIR = Path(__file__).resolve().parent
DASHBOARD_ROOT = PROJECT_ROOT / "dashboard"
IMAGE_STEM = "bengaluru_ai_visual"
IMAGE_EXTENSIONS = [".svg", ".png", ".jpg", ".jpeg"]

CANDIDATE_DIRS = [
    DASHBOARD_ROOT / "assets",
    PROJECT_ROOT / "assets",
    SCRIPT_DIR / "assets",
    SCRIPT_DIR,
    PROJECT_ROOT,
]

CANDIDATE_PATHS = [
    d / f"{IMAGE_STEM}{ext}"
    for d in CANDIDATE_DIRS
    for ext in IMAGE_EXTENSIONS
]

BACKGROUND_IMAGE_PATH = next((p for p in CANDIDATE_PATHS if p.exists()), None)

if BACKGROUND_IMAGE_PATH is None:
    for ext in IMAGE_EXTENSIONS:
        matches = list(PROJECT_ROOT.rglob(f"{IMAGE_STEM}{ext}"))
        if matches:
            BACKGROUND_IMAGE_PATH = matches[0]
            break

if BACKGROUND_IMAGE_PATH is not None:
    with open(BACKGROUND_IMAGE_PATH, "rb") as f:
        _encoded_bg = base64.b64encode(f.read()).decode()
    _mime = "image/svg+xml" if BACKGROUND_IMAGE_PATH.suffix == ".svg" else "image/png"
    BACKGROUND_IMAGE_URL = f"data:{_mime};base64,{_encoded_bg}"
else:
    BACKGROUND_IMAGE_URL = None


# This page's original base color/opacities (#070b13, slightly
# lower gradient opacity than the other pages) are preserved —
# only the image layer + overlay + fallback pattern are added.
if BACKGROUND_IMAGE_URL:
    background_css = f"""
    .stApp {{
        background-image:
            radial-gradient(circle at 15% 10%, rgba(56,189,248,0.10), transparent 42%),
            radial-gradient(circle at 85% 85%, rgba(168,85,247,0.08), transparent 48%),
            radial-gradient(rgba(148,163,184,0.14) 1px, transparent 1px),
            linear-gradient(rgba(7,11,19,0.90), rgba(7,11,19,0.90)),
            url("{BACKGROUND_IMAGE_URL}");

        background-size: cover, cover, 26px 26px, cover, cover;
        background-position: center, center, 0 0, center, center;
        background-attachment: fixed, fixed, fixed, fixed, fixed;
        background-repeat: no-repeat, no-repeat, repeat, no-repeat, no-repeat;
        background-color: #070b13;
    }}
    """
else:
    background_css = """
    .stApp {
        background:
            radial-gradient(circle at 15% 10%, rgba(56,189,248,0.10), transparent 42%),
            radial-gradient(circle at 85% 85%, rgba(168,85,247,0.08), transparent 48%),
            radial-gradient(rgba(148,163,184,0.14) 1px, transparent 1px),
            #070b13;

        background-size: cover, cover, 26px 26px, cover;
        background-position: center, center, 0 0, center;
        background-attachment: fixed;
    }
    """


# ============================================================
# GLOBAL STYLE
# ============================================================

st.html("""
<style>
""" + background_css + """

/* ============================================================
   CONTAINER
   ============================================================ */

.block-container {
    max-width: 1450px;
    padding-top: 1.7rem;
    padding-bottom: 3rem;
}


/* ============================================================
   TEXT
   ============================================================ */

h1, h2, h3 {
    color: #f8fafc !important;
}

p {
    color: #b9c6d6;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
    background: transparent;
    border-right: 1px solid rgba(56,189,248,0.10);
}


/* ============================================================
   HERO
   ============================================================ */

.hero {
    position: relative;
    overflow: hidden;

    background:
        linear-gradient(
            115deg,
            rgba(5,27,47,0.98),
            rgba(5,16,29,0.95)
        );

    border:
        1px solid rgba(56,189,248,0.20);

    border-radius: 20px;

    padding: 32px 38px;

    min-height: 190px;

    box-shadow:
        0 18px 50px rgba(0,0,0,0.32);
}


.hero::after {
    content: "";

    position: absolute;

    right: -80px;
    top: -120px;

    width: 430px;
    height: 430px;

    background:
        radial-gradient(
            circle,
            rgba(56,189,248,0.32) 0 2px,
            transparent 3px
        );

    background-size: 25px 25px;

    transform: rotate(12deg);

    opacity: 0.9;
}


.hero::before {
    content: "";

    position: absolute;

    left: -60px;
    bottom: -100px;

    width: 300px;
    height: 300px;

    background:
        radial-gradient(
            circle,
            rgba(56,189,248,0.18),
            transparent 70%
        );

    filter: blur(20px);
}


.hero-content {
    position: relative;
    z-index: 2;
}


.hero-kicker {
    color: #38bdf8;

    font-size: 0.72rem;

    font-weight: 850;

    letter-spacing: 2.4px;

    margin-bottom: 10px;
}


.hero-title {
    color: #f8fafc;

    font-size: 2.35rem;

    font-weight: 850;

    line-height: 1.1;

    margin-bottom: 12px;
}


.hero-description {
    color: #aebdce;

    font-size: 0.95rem;

    line-height: 1.65;

    max-width: 850px;
}


.hero-badge {
    position: absolute;

    z-index: 3;

    right: 25px;
    top: 23px;

    padding: 8px 12px;

    border-radius: 9px;

    background:
        rgba(5,15,28,0.82);

    border:
        1px solid rgba(56,189,248,0.17);

    color: #7dd3fc;

    font-size: 0.66rem;

    font-weight: 750;
}


/* ============================================================
   SECTION LABEL
   ============================================================ */

.section-label {
    color: #64748b;

    font-size: 0.67rem;

    font-weight: 850;

    letter-spacing: 2px;

    margin-top: 28px;

    margin-bottom: 5px;
}


.section-title {
    color: #f8fafc;

    font-size: 1.42rem;

    font-weight: 800;

    margin-bottom: 14px;
}


/* ============================================================
   GENERAL CARD
   ============================================================ */

.card {
    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease;
}


.card:hover {
    transform: translateY(-4px);

    box-shadow:
        0 20px 45px rgba(0,0,0,0.42);
}


/* ============================================================
   KPI CARDS
   ============================================================ */

.kpi-grid {
    display: grid;

    grid-template-columns:
        repeat(4, minmax(0, 1fr));

    gap: 14px;

    margin-top: 17px;
}


.kpi {
    position: relative;

    overflow: hidden;

    min-height: 118px;

    padding: 18px 19px;

    border-radius: 13px;

    box-shadow:
        0 12px 30px rgba(0,0,0,0.28);
}


.kpi::before {
    content: "";

    position: absolute;

    left: 0;
    top: 0;
    bottom: 0;

    width: 5px;
}


.kpi-top {
    display: flex;

    align-items: center;

    justify-content: space-between;
}


.kpi-label {
    color: #c3cedb;

    font-size: 0.70rem;

    font-weight: 850;

    letter-spacing: 0.8px;
}


.kpi-icon {
    width: 36px;
    height: 36px;

    display: flex;

    align-items: center;
    justify-content: center;

    border-radius: 50%;

    font-size: 1.15rem;
}


.kpi-value {
    color: #f8fafc;

    font-size: 2.05rem;

    font-weight: 900;

    line-height: 1;

    margin-top: 15px;
}


/* BLUE */

.kpi-blue {
    background:
        linear-gradient(
            145deg,
            rgba(7,39,65,0.98),
            rgba(5,21,36,0.98)
        );

    border:
        1px solid rgba(56,189,248,0.23);
}

.kpi-blue::before {
    background: #38bdf8;

    box-shadow:
        0 0 18px rgba(56,189,248,0.65);
}

.kpi-blue .kpi-icon {
    background: rgba(56,189,248,0.12);
}


/* RED */

.kpi-red {
    background:
        linear-gradient(
            145deg,
            rgba(63,19,28,0.98),
            rgba(29,10,17,0.98)
        );

    border:
        1px solid rgba(239,68,68,0.24);
}

.kpi-red::before {
    background: #ef4444;

    box-shadow:
        0 0 18px rgba(239,68,68,0.65);
}

.kpi-red .kpi-icon {
    background: rgba(239,68,68,0.12);
}


/* ORANGE */

.kpi-orange {
    background:
        linear-gradient(
            145deg,
            rgba(61,39,8,0.98),
            rgba(29,19,6,0.98)
        );

    border:
        1px solid rgba(245,158,11,0.25);
}

.kpi-orange::before {
    background: #f59e0b;

    box-shadow:
        0 0 18px rgba(245,158,11,0.65);
}

.kpi-orange .kpi-icon {
    background: rgba(245,158,11,0.12);
}


/* GREEN */

.kpi-green {
    background:
        linear-gradient(
            145deg,
            rgba(7,49,37,0.98),
            rgba(6,25,22,0.98)
        );

    border:
        1px solid rgba(34,197,94,0.23);
}

.kpi-green::before {
    background: #22c55e;

    box-shadow:
        0 0 18px rgba(34,197,94,0.65);
}

.kpi-green .kpi-icon {
    background: rgba(34,197,94,0.12);
}


/* ============================================================
   METHODOLOGY CARDS
   ============================================================ */

.info-grid {
    display: grid;

    grid-template-columns:
        repeat(2, minmax(0, 1fr));

    gap: 14px;
}


.info-card {
    min-height: 145px;

    padding: 20px 22px;

    border-radius: 15px;

    background:
        linear-gradient(
            145deg,
            rgba(8,34,55,0.96),
            rgba(6,18,30,0.96)
        );

    border:
        1px solid rgba(56,189,248,0.16);
}


.info-title {
    color: #f1f5f9;

    font-size: 0.82rem;

    font-weight: 850;

    margin-bottom: 9px;
}


.info-text {
    color: #aebccc;

    font-size: 0.77rem;

    line-height: 1.65;
}


/* ============================================================
   CHART PANEL
   ============================================================ */

.chart-panel {
    background:
        linear-gradient(
            145deg,
            rgba(8,26,43,0.96),
            rgba(5,15,27,0.96)
        );

    border:
        1px solid rgba(56,189,248,0.15);

    border-radius: 15px;

    padding: 16px 18px 8px;

    box-shadow:
        0 12px 30px rgba(0,0,0,0.22);
}


.chart-title {
    color: #f1f5f9;

    font-size: 0.80rem;

    font-weight: 850;

    letter-spacing: 0.7px;
}


.chart-subtitle {
    color: #64748b;

    font-size: 0.68rem;

    margin-top: 3px;
}


/* ============================================================
   OUTLOOK CARDS
   ============================================================ */

.outlook-grid {
    display: grid;

    grid-template-columns:
        repeat(4, minmax(0, 1fr));

    gap: 13px;
}


.outlook {
    min-height: 145px;

    padding: 19px 20px;

    border-radius: 15px;

    position: relative;

    overflow: hidden;
}


.outlook::before {
    content: "";

    position: absolute;

    left: 0;
    top: 0;
    bottom: 0;

    width: 5px;
}


.outlook-label {
    font-size: 0.67rem;

    font-weight: 850;

    letter-spacing: 0.9px;

    margin-bottom: 10px;
}


.outlook-number {
    color: #f8fafc;

    font-size: 1.90rem;

    font-weight: 900;

    line-height: 1;

    margin-bottom: 8px;
}


.outlook-description {
    color: #aebccc;

    font-size: 0.74rem;

    line-height: 1.45;
}


/* CRITICAL */

.outlook-critical {
    background:
        linear-gradient(
            145deg,
            rgba(63,19,28,0.98),
            rgba(29,10,17,0.98)
        );

    border:
        1px solid rgba(239,68,68,0.22);
}

.outlook-critical::before {
    background: #ef4444;
}


/* HIGH */

.outlook-high {
    background:
        linear-gradient(
            145deg,
            rgba(61,39,8,0.98),
            rgba(29,19,6,0.98)
        );

    border:
        1px solid rgba(245,158,11,0.22);
}

.outlook-high::before {
    background: #f59e0b;
}


/* MODERATE */

.outlook-moderate {
    background:
        linear-gradient(
            145deg,
            rgba(61,49,8,0.98),
            rgba(29,24,6,0.98)
        );

    border:
        1px solid rgba(234,179,8,0.22);
}

.outlook-moderate::before {
    background: #eab308;
}


/* LOWER */

.outlook-lower {
    background:
        linear-gradient(
            145deg,
            rgba(7,49,37,0.98),
            rgba(6,25,22,0.98)
        );

    border:
        1px solid rgba(34,197,94,0.22);
}

.outlook-lower::before {
    background: #22c55e;
}


/* ============================================================
   TABLE CONTAINER
   ============================================================ */

.table-card {
    background:
        linear-gradient(
            145deg,
            rgba(8,26,43,0.96),
            rgba(5,15,27,0.96)
        );

    border:
        1px solid rgba(56,189,248,0.14);

    border-radius: 15px;

    padding: 10px;
}


/* ============================================================
   DATA NOTE
   ============================================================ */

.data-note {
    margin-top: 27px;

    padding: 13px 17px;

    background:
        rgba(9,17,29,0.75);

    border:
        1px solid rgba(148,163,184,0.10);

    border-radius: 11px;

    color: #718198;

    font-size: 0.68rem;

    line-height: 1.55;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    text-align: center;

    color: #405069;

    font-size: 0.62rem;

    letter-spacing: 1px;

    margin-top: 28px;
}


/* ============================================================
   RESPONSIVE
   ============================================================ */

@media (max-width: 1000px) {

    .kpi-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .outlook-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .info-grid {
        grid-template-columns: 1fr;
    }
}

</style>
""")


# ============================================================
# HERO
# ============================================================

st.html("""
<div class="hero">

    <div class="hero-badge">
        2026 OUTLOOK • 37 STATIONS
    </div>

    <div class="hero-content">

        <div class="hero-kicker">
            PREDICTIVE RISK INTELLIGENCE
        </div>

        <div class="hero-title">
            2026 Predictive Risk Outlook
        </div>

        <div class="hero-description">
            A historical forecasting baseline combined with
            station-level risk and recent crash trends to provide
            a relative predictive outlook for continuously
            observed Bengaluru stations.
        </div>

    </div>

</div>
""")


# ============================================================
# KEY FIGURES
# ============================================================

st.html("""
<div class="section-label">
    PREDICTIVE OVERVIEW
</div>
""")


st.html(f"""
<div class="kpi-grid">

    <div class="kpi kpi-blue card">

        <div class="kpi-top">
            <div class="kpi-label">
                STATIONS FORECAST
            </div>

            <div class="kpi-icon">
                🔮
            </div>
        </div>

        <div class="kpi-value">
            {total_stations}
        </div>

    </div>


    <div class="kpi kpi-red card">

        <div class="kpi-top">
            <div class="kpi-label">
                CRITICAL OUTLOOK
            </div>

            <div class="kpi-icon">
                🚨
            </div>
        </div>

        <div class="kpi-value">
            {critical_count}
        </div>

    </div>


    <div class="kpi kpi-orange card">

        <div class="kpi-top">
            <div class="kpi-label">
                HIGH OUTLOOK
            </div>

            <div class="kpi-icon">
                ⚠️
            </div>
        </div>

        <div class="kpi-value">
            {high_count}
        </div>

    </div>


    <div class="kpi kpi-green card">

        <div class="kpi-top">
            <div class="kpi-label">
                INCREASING TRENDS
            </div>

            <div class="kpi-icon">
                📈
            </div>
        </div>

        <div class="kpi-value">
            {increasing_count}
        </div>

    </div>

</div>
""")


# ============================================================
# METHODOLOGY
# ============================================================

st.html("""
<div class="section-label">
    FORECAST METHODOLOGY
</div>

<div class="section-title">
    How the 2026 Outlook Was Built
</div>
""")


st.html("""
<div class="info-grid">

    <div class="info-card card">

        <div class="info-title">
            🧪 VALIDATED FORECAST BASELINE
        </div>

        <div class="info-text">
            Three historical forecasting approaches were tested:
            Last-Year baseline, 3-Year Moving Average, and Linear
            Trend. The Last-Year baseline produced the lowest
            validation error among the tested approaches.
        </div>

    </div>


    <div class="info-card card">

        <div class="info-title">
            📊 VALIDATION PERFORMANCE
        </div>

        <div class="info-text">
            The selected Last-Year baseline achieved a validation
            MAE of approximately
            <strong style="color:#38bdf8;">21.41</strong>
            and RMSE of approximately
            <strong style="color:#38bdf8;">31.66</strong>.
        </div>

    </div>

</div>
""")


# ============================================================
# TOP PREDICTIVE OUTLOOK
# ============================================================

st.html("""
<div class="section-label">
    2026 OUTLOOK
</div>

<div class="section-title">
    Highest Predictive Risk Outlook
</div>
""")


top_chart = (
    top_predictive
    .head(15)
    .sort_values(
        OUTLOOK_INDEX,
        ascending=True
    )
)


bar_colors = []

for category in top_chart[
    OUTLOOK_CATEGORY
].astype(str):

    category_lower = category.lower()

    if "critical" in category_lower:
        bar_colors.append("#ef4444")

    elif "high" in category_lower:
        bar_colors.append("#f59e0b")

    elif "moderate" in category_lower:
        bar_colors.append("#eab308")

    else:
        bar_colors.append("#22c55e")


fig_outlook = go.Figure()


fig_outlook.add_trace(
    go.Bar(
        x=top_chart[OUTLOOK_INDEX],
        y=top_chart[STATION],
        orientation="h",
        marker_color=bar_colors,
        hovertemplate=
            "<b>%{y}</b><br>"
            "Predictive Outlook Index: %{x:.2f}"
            "<extra></extra>"
    )
)


fig_outlook.update_layout(

    height=560,

    margin=dict(
        l=20,
        r=30,
        t=15,
        b=20
    ),

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    font=dict(
        color="#aebccc",
        family="Arial"
    ),

    xaxis=dict(
        title="Predictive Outlook Index",
        gridcolor="rgba(148,163,184,0.10)",
        zeroline=False
    ),

    yaxis=dict(
        title=None
    ),

    showlegend=False,

    hoverlabel=dict(
        bgcolor="#0b1725",
        font_color="#f8fafc"
    )
)


st.html("""
<div class="chart-panel">

    <div class="chart-title">
        PREDICTIVE OUTLOOK BY STATION
    </div>

    <div class="chart-subtitle">
        Relative 2026 outlook combining risk score,
        forecast level, and recent trend
    </div>

</div>
""")


st.plotly_chart(
    fig_outlook,
    use_container_width=True,
    config={"displayModeBar": False}
)


# ============================================================
# RECENT CRASH TREND
# ============================================================

st.html("""
<div class="section-label">
    RECENT CRASH MOVEMENT
</div>

<div class="section-title">
    Recent Station Trend
</div>
""")


trend_chart = (
    predictive_df
    .sort_values(
        TREND,
        ascending=True
    )
    .copy()
)


# Show strongest declines and increases
trend_chart = pd.concat(
    [
        trend_chart.head(8),
        trend_chart.tail(8)
    ]
).drop_duplicates(
    subset=[STATION]
)


trend_chart = trend_chart.sort_values(
    TREND,
    ascending=True
)


trend_colors = [
    "#ef4444" if value > 0 else "#22c55e"
    for value in trend_chart[TREND]
]


fig_trend = go.Figure()


fig_trend.add_trace(
    go.Bar(
        x=trend_chart[TREND],
        y=trend_chart[STATION],
        orientation="h",
        marker_color=trend_colors,
        hovertemplate=
            "<b>%{y}</b><br>"
            "Trend: %{x:+.2f} crashes/year"
            "<extra></extra>"
    )
)


fig_trend.add_vline(
    x=0,
    line_width=1,
    line_color="rgba(148,163,184,0.35)"
)


fig_trend.update_layout(

    height=520,

    margin=dict(
        l=20,
        r=30,
        t=15,
        b=20
    ),

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    font=dict(
        color="#aebccc",
        family="Arial"
    ),

    xaxis=dict(
        title="Recent Trend (Crashes / Year)",
        gridcolor="rgba(148,163,184,0.10)",
        zeroline=False
    ),

    yaxis=dict(
        title=None
    ),

    showlegend=False,

    hoverlabel=dict(
        bgcolor="#0b1725",
        font_color="#f8fafc"
    )
)


st.plotly_chart(
    fig_trend,
    use_container_width=True,
    config={"displayModeBar": False}
)


# ============================================================
# FORECAST TABLE
# ============================================================

st.html("""
<div class="section-label">
    FORECAST DETAILS
</div>

<div class="section-title">
    2025 Baseline vs 2026 Forecast
</div>
""")


forecast_table = predictive_df[
    [
        STATION,
        ACTUAL_2025,
        FORECAST_2026,
        RISK_SCORE,
        OUTLOOK_INDEX,
        OUTLOOK_CATEGORY
    ]
].copy()


forecast_table = (
    forecast_table
    .sort_values(
        OUTLOOK_INDEX,
        ascending=False
    )
    .head(20)
)


forecast_table.columns = [
    "Station",
    "2025 Crashes",
    "2026 Forecast",
    "Risk Score",
    "Outlook Index",
    "Predictive Outlook"
]


forecast_table["2025 Crashes"] = (
    forecast_table["2025 Crashes"]
    .round(0)
    .astype(int)
)


forecast_table["2026 Forecast"] = (
    forecast_table["2026 Forecast"]
    .round(0)
    .astype(int)
)


forecast_table["Risk Score"] = (
    forecast_table["Risk Score"]
    .round(2)
)


forecast_table["Outlook Index"] = (
    forecast_table["Outlook Index"]
    .round(2)
)


st.html("""
<div class="table-card">
</div>
""")


st.dataframe(
    forecast_table,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# OUTLOOK CATEGORIES
# ============================================================

st.html("""
<div class="section-label">
    OUTLOOK CATEGORIES
</div>

<div class="section-title">
    Predictive Risk Classification
</div>
""")


st.html(f"""
<div class="outlook-grid">

    <div class="outlook outlook-critical card">

        <div class="outlook-label"
             style="color:#f87171;">
            CRITICAL
        </div>

        <div class="outlook-number">
            {critical_count}
        </div>

        <div class="outlook-description">
            Highest relative predictive outlook.
        </div>

    </div>


    <div class="outlook outlook-high card">

        <div class="outlook-label"
             style="color:#fbbf24;">
            HIGH
        </div>

        <div class="outlook-number">
            {high_count}
        </div>

        <div class="outlook-description">
            Elevated predictive risk outlook.
        </div>

    </div>


    <div class="outlook outlook-moderate card">

        <div class="outlook-label"
             style="color:#fde047;">
            MODERATE
        </div>

        <div class="outlook-number">
            {moderate_count}
        </div>

        <div class="outlook-description">
            Intermediate predictive outlook.
        </div>

    </div>


    <div class="outlook outlook-lower card">

        <div class="outlook-label"
             style="color:#4ade80;">
            LOWER
        </div>

        <div class="outlook-number">
            {lower_count}
        </div>

        <div class="outlook-description">
            Comparatively lower predictive outlook.
        </div>

    </div>

</div>
""")


# ============================================================
# INTERPRETATION
# ============================================================

top_station = top_predictive.iloc[0][STATION]

top_station_forecast = (
    top_predictive.iloc[0][FORECAST_2026]
)

top_station_outlook = (
    top_predictive.iloc[0][OUTLOOK_INDEX]
)


st.html("""
<div class="section-label">
    INTERPRETATION
</div>

<div class="section-title">
    What the Predictive Analysis Means
</div>
""")


st.html(f"""
<div class="info-grid">

    <div class="info-card card">

        <div class="info-title">
            🔮 HIGHEST PREDICTIVE OUTLOOK
        </div>

        <div class="info-text">

            <strong style="color:#f8fafc;">
                {top_station}
            </strong>
            has the highest predictive outlook index in
            the 2026 station-level assessment, with an
            outlook index of
            <strong style="color:#f87171;">
                {top_station_outlook:.2f}
            </strong>.

        </div>

    </div>


    <div class="info-card card">

        <div class="info-title">
            📊 2026 FORECAST
        </div>

        <div class="info-text">

            The selected baseline produces a 2026 forecast
            of approximately
            <strong style="color:#38bdf8;">
                {top_station_forecast:.0f}
            </strong>
            crashes for this station.

            This is a historical-pattern estimate rather
            than an exact prediction.

        </div>

    </div>

</div>
""")


# ============================================================
# LIMITATIONS
# ============================================================

st.html("""
<div class="section-label">
    MODEL LIMITATIONS
</div>

<div class="section-title">
    Important Interpretation Notes
</div>
""")


st.html("""
<div class="info-grid">

    <div class="info-card card">

        <div class="info-title">
            ⚠️ NOT AN EXACT ACCIDENT PREDICTION
        </div>

        <div class="info-text">
            The predictive component provides a relative
            decision-support outlook. It does not claim that
            a specific number of crashes will definitely occur
            at a particular station in 2026.
        </div>

    </div>


    <div class="info-card card">

        <div class="info-title">
            🧩 VARIABLES NOT INCLUDED
        </div>

        <div class="info-text">
            The current model does not incorporate traffic
            volume, weather, road condition, construction,
            vehicle mix, or future traffic-management changes.
            These factors could affect actual crash outcomes.
        </div>

    </div>

</div>
""")


# ============================================================
# DATA NOTE
# ============================================================

st.html("""
<div class="data-note">

    <strong style="color:#94a3b8;">
        DATA NOTE
    </strong>

    &nbsp;

    The predictive analysis covers 37 stations with continuous
    historical observations from 2018–2025. The selected
    Last-Year baseline uses the latest observed crash count
    as the 2026 forecast and was selected through historical
    validation against the other tested baseline methods.

</div>
""")


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="footer">

    URBAN MOBILITY RISK INTELLIGENCE
    &nbsp; • &nbsp;
    BENGALURU ROAD CRASH ANALYSIS
    &nbsp; • &nbsp;
    2026 PREDICTIVE RISK OUTLOOK

</div>
""")