import base64
from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Summary & Results | Urban Mobility Risk Intelligence",
    page_icon="📋",
    layout="wide"
)


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_PATH = PROJECT_ROOT / "processed"


# ============================================================
# LOAD DATA
# ============================================================

master_file = PROCESSED_PATH / "bengaluru_crashes_station_master.csv"
station_file = PROCESSED_PATH / "dashboard_station_master.csv"
yearly_file = PROCESSED_PATH / "dashboard_yearly_trends.csv"
priority_file = PROCESSED_PATH / "final_intervention_priority_ranking.csv"
predictive_file = PROCESSED_PATH / "predictive_risk_2026.csv"


master_df = pd.read_csv(master_file)
station_df = pd.read_csv(station_file)
yearly_df = pd.read_csv(yearly_file)
priority_df = pd.read_csv(priority_file)
predictive_df = pd.read_csv(predictive_file)


# ============================================================
# CALCULATIONS
# ============================================================

first_year = int(yearly_df["year"].min())
last_year = int(yearly_df["year"].max())

first_year_crashes = yearly_df.iloc[0]["total_crashes"]
last_year_crashes = yearly_df.iloc[-1]["total_crashes"]

overall_change = (
    (last_year_crashes - first_year_crashes)
    / first_year_crashes
) * 100


total_crashes = yearly_df["total_crashes"].sum()

fatal_crashes = yearly_df["fatal_crashes"].sum()

station_count = station_df["station"].nunique()

high_risk_count = (
    station_df["risk_category"]
    .eq("High")
    .sum()
)

critical_count = (
    priority_df["priority_category"]
    .eq("Critical Priority")
    .sum()
)

predictive_critical = (
    predictive_df["predictive_outlook"]
    .astype(str)
    .str.contains("Critical", case=False, na=False)
    .sum()
)


# ============================================================
# TOP PRIORITY STATIONS
# ============================================================

top_priority = (
    priority_df
    .sort_values(
        "priority_index",
        ascending=False
    )
    .head(10)
    .copy()
)


# ============================================================
# TOP RISK STATIONS
# ============================================================

top_risk = (
    station_df
    .sort_values(
        "risk_score",
        ascending=False
    )
    .head(5)
    .copy()
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


# This page's original base color/opacities (#070b13) are
# preserved — only the image layer + overlay + fallback pattern
# are added, matching Predictive Risk's treatment.
if BACKGROUND_IMAGE_URL:
    background_css = f"""
    .stApp {{
        background-image:
            radial-gradient(circle at 15% 10%, rgba(56,189,248,0.10), transparent 42%),
            radial-gradient(circle at 85% 85%, rgba(168,85,247,0.09), transparent 48%),
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
            radial-gradient(circle at 85% 85%, rgba(168,85,247,0.09), transparent 48%),
            radial-gradient(rgba(148,163,184,0.14) 1px, transparent 1px),
            #070b13;

        background-size: cover, cover, 26px 26px, cover;
        background-position: center, center, 0 0, center;
        background-attachment: fixed;
    }
    """


# ============================================================
# BACKGROUND + GLOBAL STYLE
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

    border-right:
        1px solid rgba(56,189,248,0.10);
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
            rgba(5,16,29,0.96)
        );

    border:
        1px solid rgba(56,189,248,0.20);

    border-radius: 20px;

    padding: 32px 38px;

    min-height: 200px;

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

    left: -70px;

    bottom: -120px;

    width: 330px;

    height: 330px;

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

    max-width: 900px;
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

    margin-top: 30px;

    margin-bottom: 5px;
}


.section-title {

    color: #f8fafc;

    font-size: 1.42rem;

    font-weight: 800;

    margin-bottom: 14px;
}


/* ============================================================
   KPI GRID
   ============================================================ */

.kpi-grid {

    display: grid;

    grid-template-columns:
        repeat(4, minmax(0,1fr));

    gap: 14px;

    margin-top: 18px;
}


.kpi {

    position: relative;

    overflow: hidden;

    min-height: 120px;

    padding: 18px 19px;

    border-radius: 13px;

    box-shadow:
        0 12px 30px rgba(0,0,0,0.28);

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease;
}


.kpi:hover {

    transform: translateY(-4px);

    box-shadow:
        0 20px 45px rgba(0,0,0,0.42);
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
}

.kpi-orange .kpi-icon {

    background: rgba(245,158,11,0.12);
}


/* PURPLE */

.kpi-purple {

    background:
        linear-gradient(
            145deg,
            rgba(48,18,68,0.98),
            rgba(25,10,38,0.98)
        );

    border:
        1px solid rgba(168,85,247,0.25);
}

.kpi-purple::before {

    background: #a855f7;
}

.kpi-purple .kpi-icon {

    background: rgba(168,85,247,0.12);
}


/* ============================================================
   FINDING CARDS
   ============================================================ */

.finding-grid {

    display: grid;

    grid-template-columns:
        repeat(3, minmax(0,1fr));

    gap: 14px;
}


.finding {

    min-height: 175px;

    padding: 21px 22px;

    border-radius: 15px;

    position: relative;

    overflow: hidden;

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease;
}


.finding:hover {

    transform: translateY(-4px);

    box-shadow:
        0 20px 45px rgba(0,0,0,0.38);
}


.finding::before {

    content: "";

    position: absolute;

    left: 0;

    top: 0;

    bottom: 0;

    width: 5px;
}


.finding-blue {

    background:
        linear-gradient(
            145deg,
            rgba(7,39,65,0.98),
            rgba(5,21,36,0.98)
        );

    border:
        1px solid rgba(56,189,248,0.20);
}

.finding-blue::before {

    background: #38bdf8;
}


.finding-red {

    background:
        linear-gradient(
            145deg,
            rgba(63,19,28,0.98),
            rgba(29,10,17,0.98)
        );

    border:
        1px solid rgba(239,68,68,0.20);
}

.finding-red::before {

    background: #ef4444;
}


.finding-green {

    background:
        linear-gradient(
            145deg,
            rgba(7,49,37,0.98),
            rgba(6,25,22,0.98)
        );

    border:
        1px solid rgba(34,197,94,0.20);
}

.finding-green::before {

    background: #22c55e;
}


.finding-title {

    font-size: 0.68rem;

    font-weight: 850;

    letter-spacing: 1px;

    margin-bottom: 10px;
}


.finding-number {

    color: #f8fafc;

    font-size: 2rem;

    font-weight: 900;

    line-height: 1;

    margin-bottom: 10px;
}


.finding-description {

    color: #aebccc;

    font-size: 0.76rem;

    line-height: 1.55;
}


.finding-status {

    color: #64748b;

    font-size: 0.64rem;

    margin-top: 14px;
}


/* ============================================================
   PRIORITY TABLE CARD
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

    overflow: hidden;
}


/* ============================================================
   TWO-COLUMN INFORMATION
   ============================================================ */

.info-grid {

    display: grid;

    grid-template-columns:
        repeat(2, minmax(0,1fr));

    gap: 14px;
}


.info-card {

    min-height: 155px;

    padding: 21px 22px;

    border-radius: 15px;

    background:
        linear-gradient(
            145deg,
            rgba(8,34,55,0.96),
            rgba(6,18,30,0.96)
        );

    border:
        1px solid rgba(56,189,248,0.15);

    transition:
        transform 0.25s ease;
}


.info-card:hover {

    transform: translateY(-3px);
}


.info-title {

    color: #f1f5f9;

    font-size: 0.82rem;

    font-weight: 850;

    margin-bottom: 10px;
}


.info-text {

    color: #aebccc;

    font-size: 0.77rem;

    line-height: 1.65;
}


/* ============================================================
   FINAL TAKEAWAY
   ============================================================ */

.takeaway {

    position: relative;

    overflow: hidden;

    padding: 27px 30px;

    border-radius: 17px;

    background:
        linear-gradient(
            110deg,
            rgba(7,39,65,0.98),
            rgba(35,15,55,0.98)
        );

    border:
        1px solid rgba(56,189,248,0.22);

    box-shadow:
        0 15px 40px rgba(0,0,0,0.30);
}


.takeaway::after {

    content: "";

    position: absolute;

    width: 250px;

    height: 250px;

    right: -80px;

    top: -100px;

    background:
        radial-gradient(
            circle,
            rgba(168,85,247,0.25),
            transparent 70%
        );
}


.takeaway-title {

    position: relative;

    z-index: 2;

    color: #38bdf8;

    font-size: 0.70rem;

    font-weight: 850;

    letter-spacing: 2px;

    margin-bottom: 9px;
}


.takeaway-main {

    position: relative;

    z-index: 2;

    color: #f8fafc;

    font-size: 1.25rem;

    font-weight: 800;

    line-height: 1.45;

    max-width: 1000px;
}


.takeaway-text {

    position: relative;

    z-index: 2;

    color: #aebccc;

    font-size: 0.78rem;

    line-height: 1.65;

    max-width: 1050px;

    margin-top: 9px;
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

    margin-top: 30px;
}


/* ============================================================
   RESPONSIVE
   ============================================================ */

@media (max-width: 1000px) {

    .kpi-grid {

        grid-template-columns:
            repeat(2,1fr);
    }

    .finding-grid {

        grid-template-columns:
            1fr;
    }

    .info-grid {

        grid-template-columns:
            1fr;
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
        PROJECT CONCLUSION • 2018–2025
    </div>

    <div class="hero-content">

        <div class="hero-kicker">
            EXECUTIVE SUMMARY
        </div>

        <div class="hero-title">
            Summary & Results
        </div>

        <div class="hero-description">
            Consolidated findings from Bengaluru's historical crash
            patterns, station-level risk assessment, geographic
            analysis, intervention prioritization, and 2026
            predictive outlook.
        </div>

    </div>

</div>
""")


# ============================================================
# PROJECT SNAPSHOT
# ============================================================

st.html("""
<div class="section-label">
    PROJECT SNAPSHOT
</div>
""")


st.html(f"""
<div class="kpi-grid">

    <div class="kpi kpi-blue">

        <div class="kpi-top">

            <div class="kpi-label">
                STATIONS ANALYZED
            </div>

            <div class="kpi-icon">
                📍
            </div>

        </div>

        <div class="kpi-value">
            {station_count}
        </div>

    </div>


    <div class="kpi kpi-red">

        <div class="kpi-top">

            <div class="kpi-label">
                TOTAL CRASHES
            </div>

            <div class="kpi-icon">
                🚨
            </div>

        </div>

        <div class="kpi-value">
            {total_crashes:,.0f}
        </div>

    </div>


    <div class="kpi kpi-orange">

        <div class="kpi-top">

            <div class="kpi-label">
                HIGH-RISK STATIONS
            </div>

            <div class="kpi-icon">
                ⚠️
            </div>

        </div>

        <div class="kpi-value">
            {high_risk_count}
        </div>

    </div>


    <div class="kpi kpi-purple">

        <div class="kpi-top">

            <div class="kpi-label">
                CRITICAL PRIORITIES
            </div>

            <div class="kpi-icon">
                🎯
            </div>

        </div>

        <div class="kpi-value">
            {critical_count}
        </div>

    </div>

</div>
""")


# ============================================================
# KEY FINDINGS
# ============================================================

st.html("""
<div class="section-label">
    EXECUTIVE INSIGHTS
</div>

<div class="section-title">
    What the Analysis Found
</div>
""")


st.html(f"""
<div class="finding-grid">

    <div class="finding finding-blue">

        <div class="finding-title"
             style="color:#38bdf8;">

            CITYWIDE CRASH CHANGE

        </div>

        <div class="finding-number">
            {overall_change:+.1f}%
        </div>

        <div class="finding-description">

            Total recorded crashes changed by
            {overall_change:+.1f}% between
            {first_year} and {last_year}.

        </div>

        <div class="finding-status">
            ● Historical citywide comparison
        </div>

    </div>


    <div class="finding finding-red">

        <div class="finding-title"
             style="color:#f87171;">

            HIGH-RISK LOCATIONS

        </div>

        <div class="finding-number">
            {high_risk_count}
        </div>

        <div class="finding-description">

            Three stations are classified as
            High Risk by the station-level risk
            scoring framework.

        </div>

        <div class="finding-status">
            ● Risk score assessment
        </div>

    </div>


    <div class="finding finding-green">

        <div class="finding-title"
             style="color:#4ade80;">

            CRITICAL PRIORITIES

        </div>

        <div class="finding-number">
            {critical_count}
        </div>

        <div class="finding-description">

            Stations classified as Critical Priority
            using the project's intervention-priority
            framework.

        </div>

        <div class="finding-status">
            ● Risk + severity + trend
        </div>

    </div>

</div>
""")


# ============================================================
# PRIORITY AREAS
# ============================================================

st.html("""
<div class="section-label">
    INTERVENTION PRIORITIES
</div>

<div class="section-title">
    Priority Stations
</div>
""")


priority_display = top_priority[
    [
        "priority_rank",
        "station",
        "priority_index",
        "priority_category",
        "risk_score",
        "trend_category"
    ]
].copy()


priority_display.columns = [
    "Priority Rank",
    "Station",
    "Priority Index",
    "Priority Category",
    "Risk Score",
    "Trend"
]


priority_display["Priority Index"] = (
    priority_display["Priority Index"]
    .round(2)
)


priority_display["Risk Score"] = (
    priority_display["Risk Score"]
    .round(2)
)


st.html("""
<div class="table-card">
</div>
""")


st.dataframe(
    priority_display,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# MAIN RISK FINDINGS
# ============================================================

st.html("""
<div class="section-label">
    MAIN RISK FINDINGS
</div>

<div class="section-title">
    Stations Requiring Attention
</div>
""")


risk_items = ""


for _, row in top_risk.head(5).iterrows():

    risk_items += f"""
    <div style="
        display:flex;
        align-items:center;
        justify-content:space-between;
        padding:10px 0;
        border-bottom:1px solid rgba(148,163,184,0.08);
    ">

        <div>

            <div style="
                color:#f8fafc;
                font-weight:800;
                font-size:0.78rem;
            ">
                {row["station"]}
            </div>

            <div style="
                color:#64748b;
                font-size:0.64rem;
                margin-top:3px;
            ">
                {row["data_coverage"]} coverage
                • {row["years_available"]} years
            </div>

        </div>


        <div style="
            text-align:right;
        ">

            <div style="
                color:#f87171;
                font-size:0.90rem;
                font-weight:850;
            ">
                {row["risk_score"]:.2f}
            </div>

            <div style="
                color:#64748b;
                font-size:0.60rem;
            ">
                RISK SCORE
            </div>

        </div>

    </div>
    """


st.html(f"""
<div class="info-grid">

    <div class="info-card">

        <div class="info-title">
            🔴 TOP RISK STATIONS
        </div>

        {risk_items}

    </div>


    <div class="info-card">

        <div class="info-title">
            📊 WHAT THE RISK MODEL USES
        </div>

        <div class="info-text">

            The station-level risk framework combines
            historical crash frequency, fatality,
            crash severity, and recent crash performance.

            <br><br>

            Coverage strength is also reported so that
            stations with shorter histories are not
            interpreted in the same way as stations with
            long continuous records.

        </div>

    </div>

</div>
""")


# ============================================================
# PREDICTIVE OUTLOOK
# ============================================================

st.html("""
<div class="section-label">
    LOOKING AHEAD
</div>

<div class="section-title">
    2026 Predictive Outlook
</div>
""")


st.html(f"""
<div class="info-grid">

    <div class="info-card">

        <div class="info-title">
            🔮 PREDICTIVE ANALYSIS
        </div>

        <div class="info-text">

            The predictive component evaluates
            <strong style="color:#38bdf8;">
                37 stations
            </strong>
            with continuous observations from
            2018–2025.

            The selected Last-Year forecasting baseline
            achieved a validation MAE of approximately
            <strong style="color:#38bdf8;">
                21.41
            </strong>
            and RMSE of approximately
            <strong style="color:#38bdf8;">
                31.66
            </strong>.

        </div>

    </div>


    <div class="info-card">

        <div class="info-title">
            ⚠️ INTERPRETATION
        </div>

        <div class="info-text">

            The 2026 predictive outlook is a relative
            decision-support indicator based on historical
            patterns, risk scores, forecast level, and
            recent trends.

            It should not be interpreted as an exact
            prediction of future accidents.

        </div>

    </div>

</div>
""")


# ============================================================
# PROJECT APPLICATIONS
# ============================================================

st.html("""
<div class="section-label">
    PRACTICAL APPLICATION
</div>

<div class="section-title">
    How the Dashboard Can Be Used
</div>
""")


st.html("""
<div class="info-grid">

    <div class="info-card">

        <div class="info-title">
            🚦 TARGETED ROAD SAFETY
        </div>

        <div class="info-text">

            Identify stations and surrounding areas that
            may warrant closer examination for road-safety
            interventions, enforcement activity, junction
            improvements, or engineering review.

        </div>

    </div>


    <div class="info-card">

        <div class="info-title">
            📊 DATA-DRIVEN MONITORING
        </div>

        <div class="info-text">

            Track how crash activity changes over time,
            compare recent performance with historical
            patterns, and identify locations where trends
            are changing.

        </div>

    </div>


    <div class="info-card">

        <div class="info-title">
            🗺️ GEOGRAPHIC PLANNING
        </div>

        <div class="info-text">

            Use the risk map to understand the spatial
            distribution of higher-risk stations and
            support geographically targeted analysis.

        </div>

    </div>


    <div class="info-card">

        <div class="info-title">
            🔮 FORWARD-LOOKING ANALYSIS
        </div>

        <div class="info-text">

            Use the predictive outlook as an additional
            analytical layer for identifying stations
            that may deserve continued monitoring.

        </div>

    </div>

</div>
""")


# ============================================================
# LIMITATIONS
# ============================================================

st.html("""
<div class="section-label">
    LIMITATIONS
</div>

<div class="section-title">
    Important Considerations
</div>
""")


st.html("""
<div class="info-grid">

    <div class="info-card">

        <div class="info-title">
            📁 DATA AVAILABILITY
        </div>

        <div class="info-text">

            Station coverage is not identical across all
            locations. Some stations have shorter historical
            records, so comparisons should consider the
            available observation period.

        </div>

    </div>


    <div class="info-card">

        <div class="info-title">
            🧩 UNOBSERVED FACTORS
        </div>

        <div class="info-text">

            The analysis does not currently incorporate
            traffic volume, weather, road condition,
            construction activity, vehicle mix, or future
            traffic-management changes.

        </div>

    </div>


    <div class="info-card">

        <div class="info-title">
            📍 GEOGRAPHIC PRECISION
        </div>

        <div class="info-text">

            Some station coordinates represent station or
            locality areas and may be approximate rather
            than exact police-station building locations.

        </div>

    </div>


    <div class="info-card">

        <div class="info-title">
            🔮 PREDICTION LIMITATION
        </div>

        <div class="info-text">

            The predictive component is a historical
            baseline and relative outlook. It is not a
            causal accident-prediction system or a guarantee
            of future crash counts.

        </div>

    </div>

</div>
""")


# ============================================================
# FINAL TAKEAWAY
# ============================================================

st.html("""
<div class="section-label">
    FINAL TAKEAWAY
</div>
""")


st.html(f"""
<div class="takeaway">

    <div class="takeaway-title">
        URBAN MOBILITY RISK INTELLIGENCE
    </div>

    <div class="takeaway-main">

        A station-level analytical framework for understanding
        where Bengaluru's road-crash burden, severity, trends,
        and predictive risk outlook intersect.

    </div>

    <div class="takeaway-text">

        The project brings together {first_year}–{last_year}
        crash records, station-level risk scoring, geographic
        visualization, intervention prioritization, and a
        validated historical forecasting baseline into a
        single decision-support dashboard.

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

    2024 and 2025 station datasets do not provide
    people-killed and people-injured fields. These values
    are retained as missing rather than treated as zero.

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
    FINAL RESULTS

</div>
""")