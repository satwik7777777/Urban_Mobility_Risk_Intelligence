import base64
from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Overview | Urban Mobility Risk Intelligence",
    page_icon="📊",
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

master_df = pd.read_csv(master_file)
station_df = pd.read_csv(station_file)
yearly_df = pd.read_csv(yearly_file)
priority_df = pd.read_csv(priority_file)


# ============================================================
# CALCULATIONS
# ============================================================

total_crashes = yearly_df["total_crashes"].sum()

fatal_crashes = yearly_df["fatal_crashes"].sum()

high_risk = (
    station_df["risk_category"]
    .eq("High")
    .sum()
)

critical = (
    priority_df["priority_category"]
    .eq("Critical Priority")
    .sum()
)

first_year = int(yearly_df.iloc[0]["year"])
last_year = int(yearly_df.iloc[-1]["year"])

first_year_crashes = yearly_df.iloc[0]["total_crashes"]
last_year_crashes = yearly_df.iloc[-1]["total_crashes"]

overall_change = (
    (last_year_crashes - first_year_crashes)
    / first_year_crashes
) * 100


# ============================================================
# BACKGROUND ARTWORK
# ============================================================
# Same detection approach as Home.py: look for the shared
# "bengaluru_ai_visual" artwork (svg/png/jpg) in the usual asset
# locations, plus the project's own dashboard/ folder tree, so
# every page can reuse the exact same background file without
# duplicating it per page. Falls back cleanly to the existing
# dot-grid-only look if nothing is found — nothing breaks either
# way.

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


# ============================================================
# BACKGROUND CSS
# ============================================================
# Layered, back to front: radial glow accents (top) -> dot grid ->
# a dark overlay that dims the artwork -> the artwork itself ->
# solid base color (bottom, always-present fallback). When no
# artwork file is found, the overlay + image layers are simply
# left out and the page renders exactly as before.

if BACKGROUND_IMAGE_URL:
    background_css = f"""
    .stApp {{
        background-image:
            radial-gradient(circle at 15% 10%, rgba(56,189,248,0.12), transparent 45%),
            radial-gradient(circle at 85% 85%, rgba(168,85,247,0.10), transparent 50%),
            radial-gradient(rgba(148,163,184,0.16) 1px, transparent 1px),
            linear-gradient(rgba(6,11,20,0.90), rgba(6,11,20,0.90)),
            url("{BACKGROUND_IMAGE_URL}");

        background-size: cover, cover, 26px 26px, cover, cover;
        background-position: center, center, 0 0, center, center;
        background-attachment: fixed, fixed, fixed, fixed, fixed;
        background-repeat: no-repeat, no-repeat, repeat, no-repeat, no-repeat;
        background-color: #060b14;
    }}
    """
else:
    background_css = """
    .stApp {
        background:
            radial-gradient(circle at 15% 10%, rgba(56,189,248,0.12), transparent 45%),
            radial-gradient(circle at 85% 85%, rgba(168,85,247,0.10), transparent 50%),
            radial-gradient(rgba(148,163,184,0.16) 1px, transparent 1px),
            #060b14;

        background-size: cover, cover, 26px 26px, cover;
        background-position: center, center, 0 0, center;
        background-attachment: fixed, fixed, fixed, fixed;
    }
    """


# ============================================================
# PAGE STYLING
# ============================================================

st.html(f"""
<style>

{background_css}


/* ============================================================
   MAIN CONTAINER
   ============================================================ */

.block-container {{
    max-width: 1450px;
    padding-top: 1.7rem;
    padding-bottom: 3rem;
}}


/* ============================================================
   GENERAL TEXT
   ============================================================ */

h1, h2, h3 {{
    color: #f8fafc !important;
}}

p {{
    color: #b9c6d6;
}}

hr {{
    border-color: rgba(148,163,184,0.10) !important;
}}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {{
    /* Transparent so the page's own .stApp background (gradients +
       artwork) shows through instead of a separate solid panel —
       keeps the sidebar visually merged with the rest of the page. */
    background: transparent;

    border-right:
        1px solid rgba(56,189,248,0.10);
}}


/* ============================================================
   HOVER LIFT (applies to all card types)
   ============================================================ */

.kpi, .analysis, .finding, .dataset-card, .coverage {{
    transition: transform 0.25s ease, box-shadow 0.25s ease,
        border-color 0.25s ease;
}}

.kpi:hover, .analysis:hover, .finding:hover, .coverage:hover {{
    transform: translateY(-4px);
    box-shadow: 0 20px 45px rgba(0,0,0,0.42);
}}

.dataset-card:hover {{
    transform: translateY(-3px);
    border-color: rgba(56,189,248,0.35);
    box-shadow: 0 18px 40px rgba(0,0,0,0.35);
}}


/* ============================================================
   HERO
   ============================================================ */

.hero {{
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

    min-height: 205px;

    box-shadow:
        0 18px 50px rgba(0,0,0,0.32);
}}


.hero::after {{
    content: "";

    position: absolute;

    right: -80px;
    top: -120px;

    width: 430px;
    height: 430px;

    background:
        radial-gradient(
            circle,
            rgba(56,189,248,0.35) 0 2px,
            transparent 3px
        );

    background-size: 25px 25px;

    transform: rotate(12deg);

    opacity: 0.9;

    z-index: 1;
}}


.hero::before {{
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

    z-index: 1;
}}


.hero-kicker {{
    position: relative;
    z-index: 2;

    color: #38bdf8;

    font-size: 0.72rem;

    font-weight: 850;

    letter-spacing: 2.4px;

    margin-bottom: 10px;
}}


.hero-title {{
    position: relative;
    z-index: 2;

    color: #f8fafc;

    font-size: 2.35rem;

    font-weight: 850;

    line-height: 1.1;

    max-width: 850px;

    margin-bottom: 12px;
}}


.hero-description {{
    position: relative;
    z-index: 2;

    color: #aebdce;

    font-size: 0.95rem;

    line-height: 1.65;

    max-width: 800px;
}}


.hero-badge {{
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
}}


/* ============================================================
   SECTION LABELS
   ============================================================ */

.section-label {{
    color: #64748b;

    font-size: 0.67rem;

    font-weight: 850;

    letter-spacing: 2px;

    margin-top: 28px;

    margin-bottom: 5px;
}}


.section-title {{
    color: #f8fafc;

    font-size: 1.42rem;

    font-weight: 800;

    margin-bottom: 14px;
}}


/* ============================================================
   KPI GRID
   ============================================================ */

.kpi-grid {{
    display: grid;

    grid-template-columns:
        repeat(4, minmax(0, 1fr));

    gap: 14px;

    margin-top: 17px;
}}


.kpi {{
    position: relative;

    overflow: hidden;

    min-height: 118px;

    padding: 18px 19px;

    border-radius: 13px;

    box-shadow:
        0 12px 30px rgba(0,0,0,0.28);
}}


.kpi::before {{
    content: "";

    position: absolute;

    left: 0;
    top: 0;
    bottom: 0;

    width: 5px;
}}


/* faint diagonal trend-line accent in the bottom-right of each
   KPI card — pure CSS (no embedded SVG), so it can't break the
   rest of the stylesheet the way a data-URI can */
.kpi::after {{
    content: "";

    position: absolute;

    right: 16px;
    bottom: 18px;

    width: 56px;
    height: 22px;

    opacity: 0.45;

    background: linear-gradient(
        100deg,
        transparent 46%,
        currentColor 47%,
        currentColor 53%,
        transparent 54%
    );
}}


.kpi-top {{
    display: flex;

    align-items: center;

    justify-content: space-between;
}}


.kpi-label {{
    color: #c3cedb;

    font-size: 0.70rem;

    font-weight: 850;

    letter-spacing: 0.8px;
}}


.kpi-icon {{
    width: 36px;
    height: 36px;

    display: flex;

    align-items: center;
    justify-content: center;

    border-radius: 50%;

    font-size: 1.15rem;
}}


.kpi-value {{
    color: #f8fafc;

    font-size: 2.05rem;

    font-weight: 900;

    line-height: 1;

    margin-top: 15px;
}}


/* ============================================================
   KPI BLUE
   ============================================================ */

.kpi-blue {{
    background:
        linear-gradient(
            145deg,
            rgba(7,39,65,0.98),
            rgba(5,21,36,0.98)
        );

    border:
        1px solid rgba(56,189,248,0.23);
}}

.kpi-blue::before {{
    background: #38bdf8;

    box-shadow:
        0 0 18px rgba(56,189,248,0.65);
}}

.kpi-blue .kpi-icon {{
    background: rgba(56,189,248,0.12);
    color: #38bdf8;
}}

.kpi-blue::after {{
    color: #38bdf8;
}}


/* ============================================================
   KPI RED
   ============================================================ */

.kpi-red {{
    background:
        linear-gradient(
            145deg,
            rgba(63,19,28,0.98),
            rgba(29,10,17,0.98)
        );

    border:
        1px solid rgba(239,68,68,0.24);
}}

.kpi-red::before {{
    background: #ef4444;

    box-shadow:
        0 0 18px rgba(239,68,68,0.65);
}}

.kpi-red .kpi-icon {{
    background: rgba(239,68,68,0.12);
    color: #f87171;
}}

.kpi-red::after {{
    color: #f87171;
}}


/* ============================================================
   KPI ORANGE
   ============================================================ */

.kpi-orange {{
    background:
        linear-gradient(
            145deg,
            rgba(61,39,8,0.98),
            rgba(29,19,6,0.98)
        );

    border:
        1px solid rgba(245,158,11,0.25);
}}

.kpi-orange::before {{
    background: #f59e0b;

    box-shadow:
        0 0 18px rgba(245,158,11,0.65);
}}

.kpi-orange .kpi-icon {{
    background: rgba(245,158,11,0.12);
    color: #fbbf24;
}}

.kpi-orange::after {{
    color: #fbbf24;
}}


/* ============================================================
   KPI PURPLE
   ============================================================ */

.kpi-purple {{
    background:
        linear-gradient(
            145deg,
            rgba(50,22,66,0.98),
            rgba(25,12,35,0.98)
        );

    border:
        1px solid rgba(168,85,247,0.26);
}}

.kpi-purple::before {{
    background: #a855f7;

    box-shadow:
        0 0 18px rgba(168,85,247,0.65);
}}

.kpi-purple .kpi-icon {{
    background: rgba(168,85,247,0.13);
    color: #c084fc;
}}

.kpi-purple::after {{
    color: #c084fc;
}}


/* ============================================================
   DATASET CARD
   ============================================================ */

.dataset-card {{
    display: grid;

    grid-template-columns:
        58px 1fr 145px;

    align-items: center;

    gap: 20px;

    background:
        linear-gradient(
            145deg,
            rgba(12,31,50,0.95),
            rgba(6,16,28,0.95)
        );

    border:
        1px solid rgba(56,189,248,0.14);

    border-radius: 15px;

    padding: 20px 23px;

    box-shadow:
        0 12px 30px rgba(0,0,0,0.22);
}}


.dataset-icon {{
    width: 55px;
    height: 55px;

    display: flex;

    align-items: center;
    justify-content: center;

    border-radius: 50%;

    background:
        rgba(56,189,248,0.10);

    border:
        1px solid rgba(56,189,248,0.18);

    font-size: 1.55rem;
}}


.dataset-main {{
    color: #b7c5d5;

    font-size: 0.87rem;

    line-height: 1.65;
}}


.dataset-main strong {{
    color: #f1f5f9;
}}


.dataset-period {{
    text-align: center;

    border-left:
        1px solid rgba(148,163,184,0.13);

    padding-left: 15px;
}}


.dataset-period-value {{
    color: #38bdf8;

    font-size: 1.30rem;

    font-weight: 850;
}}


.dataset-period-label {{
    color: #64748b;

    font-size: 0.61rem;

    font-weight: 800;

    letter-spacing: 0.8px;

    margin-top: 4px;
}}


/* ============================================================
   COVERAGE
   ============================================================ */

.coverage-grid {{
    display: grid;

    grid-template-columns:
        repeat(3, minmax(0, 1fr));

    gap: 13px;
}}


.coverage {{
    min-height: 100px;

    padding: 18px 20px;

    border-radius: 14px;
}}


.coverage-label {{
    color: #b6c3d2;

    font-size: 0.65rem;

    font-weight: 850;

    letter-spacing: 0.8px;
}}


.coverage-value {{
    color: #f8fafc;

    font-size: 1.60rem;

    font-weight: 900;

    margin-top: 8px;
}}


.coverage-note {{
    font-size: 0.67rem;

    margin-top: 3px;
}}


.coverage-green {{
    background:
        linear-gradient(
            145deg,
            rgba(7,51,38,0.96),
            rgba(6,25,22,0.96)
        );

    border:
        1px solid rgba(34,197,94,0.20);
}}

.coverage-green .coverage-note {{
    color: #4ade80;
}}


.coverage-blue {{
    background:
        linear-gradient(
            145deg,
            rgba(7,39,62,0.96),
            rgba(6,20,34,0.96)
        );

    border:
        1px solid rgba(56,189,248,0.20);
}}

.coverage-blue .coverage-note {{
    color: #38bdf8;
}}


.coverage-purple {{
    background:
        linear-gradient(
            145deg,
            rgba(46,21,62,0.96),
            rgba(23,12,33,0.96)
        );

    border:
        1px solid rgba(168,85,247,0.20);
}}

.coverage-purple .coverage-note {{
    color: #c084fc;
}}


/* ============================================================
   ANALYSIS CARDS
   ============================================================ */

.analysis-grid {{
    display: grid;

    grid-template-columns:
        repeat(2, minmax(0, 1fr));

    gap: 13px;
}}


.analysis {{
    min-height: 165px;

    padding: 21px 23px;

    border-radius: 15px;

    background:
        linear-gradient(
            145deg,
            rgba(8,34,55,0.96),
            rgba(6,18,30,0.96)
        );

    border:
        1px solid rgba(56,189,248,0.18);
}}


.analysis-orange {{
    background:
        linear-gradient(
            145deg,
            rgba(53,33,8,0.96),
            rgba(25,17,6,0.96)
        );

    border:
        1px solid rgba(245,158,11,0.19);
}}


.analysis-header {{
    display: flex;

    align-items: center;

    gap: 10px;

    margin-bottom: 12px;
}}


.analysis-icon {{
    font-size: 1.25rem;
}}


.analysis-title {{
    color: #f1f5f9;

    font-size: 0.80rem;

    font-weight: 850;

    letter-spacing: 0.6px;
}}


.analysis-item {{
    color: #a5b4c5;

    font-size: 0.79rem;

    line-height: 1.75;
}}


/* ============================================================
   FINDINGS
   ============================================================ */

.finding-grid {{
    display: grid;

    grid-template-columns:
        repeat(3, minmax(0, 1fr));

    gap: 13px;
}}


.finding {{
    min-height: 172px;

    padding: 20px 21px;

    border-radius: 15px;
}}


.finding-blue {{
    background:
        linear-gradient(
            145deg,
            rgba(7,38,63,0.97),
            rgba(6,20,34,0.97)
        );

    border:
        1px solid rgba(56,189,248,0.20);
}}


.finding-red {{
    background:
        linear-gradient(
            145deg,
            rgba(58,18,27,0.97),
            rgba(28,10,17,0.97)
        );

    border:
        1px solid rgba(239,68,68,0.20);
}}


.finding-green {{
    background:
        linear-gradient(
            145deg,
            rgba(7,49,37,0.97),
            rgba(6,25,22,0.97)
        );

    border:
        1px solid rgba(34,197,94,0.20);
}}


.finding-title {{
    font-size: 0.67rem;

    font-weight: 850;

    letter-spacing: 0.9px;

    margin-bottom: 12px;
}}


.finding-number {{
    color: #f8fafc;

    font-size: 1.95rem;

    font-weight: 900;

    line-height: 1;

    margin-bottom: 10px;
}}


.finding-description {{
    color: #aebccc;

    font-size: 0.77rem;

    line-height: 1.55;
}}


.finding-status {{
    color: #64748b;

    font-size: 0.64rem;

    margin-top: 12px;
}}


/* ============================================================
   DATA NOTE
   ============================================================ */

.data-note {{
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
}}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {{
    text-align: center;

    color: #405069;

    font-size: 0.62rem;

    letter-spacing: 1px;

    margin-top: 28px;
}}


/* ============================================================
   RESPONSIVE
   ============================================================ */

@media (max-width: 900px) {{

    .kpi-grid {{
        grid-template-columns: repeat(2, 1fr);
    }}

    .coverage-grid {{
        grid-template-columns: 1fr;
    }}

    .analysis-grid {{
        grid-template-columns: 1fr;
    }}

    .finding-grid {{
        grid-template-columns: 1fr;
    }}

    .dataset-card {{
        grid-template-columns: 1fr;
    }}

    .dataset-period {{
        border-left: none;
        border-top: 1px solid rgba(148,163,184,0.13);
        padding-left: 0;
        padding-top: 12px;
    }}

}}

</style>
""")


# ============================================================
# HERO TITLE CARD
# ============================================================

st.html("""
<div class="hero">

    <div class="hero-badge">
        PROJECT OVERVIEW • 2018–2025
    </div>

    <div class="hero-content">

        <div class="hero-kicker">
            PROJECT OVERVIEW
        </div>

        <div class="hero-title">
            Bengaluru Road Crash Risk Intelligence
        </div>

        <div class="hero-description">
            An analytical overview of Bengaluru's road-crash
            patterns, station-level risk, data coverage,
            and intervention priorities across 2018–2025.
        </div>

    </div>

</div>
""")

# ============================================================
# KEY FIGURES
# ============================================================

st.html("""
<div class="section-label">
    KEY FIGURES
</div>
""")


st.html(f"""
<div class="kpi-grid">

    <div class="kpi kpi-blue">

        <div class="kpi-top">

            <div class="kpi-label">
                TOTAL CRASHES
            </div>

            <div class="kpi-icon">
                📊
            </div>

        </div>

        <div class="kpi-value">
            {total_crashes:,.0f}
        </div>

    </div>


    <div class="kpi kpi-red">

        <div class="kpi-top">

            <div class="kpi-label">
                FATAL CRASHES
            </div>

            <div class="kpi-icon">
                🚨
            </div>

        </div>

        <div class="kpi-value">
            {fatal_crashes:,.0f}
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
            {high_risk}
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
            {critical}
        </div>

    </div>

</div>
""")


# ============================================================
# DATA FOUNDATION
# ============================================================

st.html("""
<div class="section-label">
    DATA FOUNDATION
</div>

<div class="section-title">
    Understanding the Dataset
</div>
""")


st.html("""
<div class="dataset-card">

    <div class="dataset-icon">
        🗄️
    </div>

    <div class="dataset-main">

        This project analyzes
        <strong>Bengaluru road crash data</strong>
        to identify accident patterns, high-risk traffic police
        stations, crash severity, changing trends, and areas that
        may require targeted intervention.

        <br>

        Station-level records are combined with risk scoring,
        trend analysis, geographic information, and intervention
        prioritization.

    </div>

    <div class="dataset-period">

        <div class="dataset-period-value">
            2018–2025
        </div>

        <div class="dataset-period-label">
            ANALYSIS PERIOD
        </div>

    </div>

</div>
""")


# ============================================================
# DATA COVERAGE
# ============================================================

st.html("""
<div class="section-label">
    DATASET SCALE
</div>

<div class="section-title">
    Data Coverage
</div>
""")


st.html(f"""
<div class="coverage-grid">

    <div class="coverage coverage-green">

        <div class="coverage-label">
            ANALYSIS PERIOD
        </div>

        <div class="coverage-value">
            {first_year}–{last_year}
        </div>

        <div class="coverage-note">
            ● 8 years of data
        </div>

    </div>


    <div class="coverage coverage-blue">

        <div class="coverage-label">
            STATIONS ANALYZED
        </div>

        <div class="coverage-value">
            {station_df["station"].nunique()}
        </div>

        <div class="coverage-note">
            ● Traffic police stations
        </div>

    </div>


    <div class="coverage coverage-purple">

        <div class="coverage-label">
            STATION-YEAR RECORDS
        </div>

        <div class="coverage-value">
            {len(master_df):,}
        </div>

        <div class="coverage-note">
            ● Total analytical records
        </div>

    </div>

</div>
""")


# ============================================================
# ANALYTICAL FRAMEWORK
# ============================================================

st.html("""
<div class="section-label">
    ANALYTICAL FRAMEWORK
</div>

<div class="section-title">
    What the Analysis Covers
</div>
""")


st.html("""
<div class="analysis-grid">

    <div class="analysis">

        <div class="analysis-header">

            <div class="analysis-icon">
                📈
            </div>

            <div class="analysis-title">
                CRASH PATTERNS
            </div>

        </div>

        <div class="analysis-item">
            • Annual crash volumes
        </div>

        <div class="analysis-item">
            • Fatal and non-fatal crashes
        </div>

        <div class="analysis-item">
            • Year-over-year changes
        </div>

        <div class="analysis-item">
            • Station-level crash trends
        </div>

    </div>


    <div class="analysis analysis-orange">

        <div class="analysis-header">

            <div class="analysis-icon">
                🎯
            </div>

            <div class="analysis-title">
                RISK & INTERVENTION
            </div>

        </div>

        <div class="analysis-item">
            • Station risk scores
        </div>

        <div class="analysis-item">
            • Crash severity
        </div>

        <div class="analysis-item">
            • Risk categories
        </div>

        <div class="analysis-item">
            • Intervention priority ranking
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
    Key Findings
</div>
""")


st.html(f"""
<div class="finding-grid">

    <div class="finding finding-blue">

        <div class="finding-title" style="color:#38bdf8;">
            OVERALL CRASH CHANGE
        </div>

        <div class="finding-number">
            {overall_change:+.1f}%
        </div>

        <div class="finding-description">
            Total crashes changed by {overall_change:+.1f}%
            between {first_year} and {last_year}.
        </div>

        <div class="finding-status">
            ● Historical citywide comparison
        </div>

    </div>


    <div class="finding finding-red">

        <div class="finding-title" style="color:#f87171;">
            HIGH-RISK STATIONS
        </div>

        <div class="finding-number">
            {high_risk}
        </div>

        <div class="finding-description">
            Stations identified by the project's risk model
            as requiring the closest attention.
        </div>

        <div class="finding-status">
            ● Risk score based assessment
        </div>

    </div>


    <div class="finding finding-green">

        <div class="finding-title" style="color:#4ade80;">
            CRITICAL PRIORITIES
        </div>

        <div class="finding-number">
            {critical}
        </div>

        <div class="finding-description">
            Stations classified as critical intervention
            priorities using combined risk and trend analysis.
        </div>

        <div class="finding-status">
            ● Risk + severity + trend
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

    2024 and 2025 station datasets do not provide
    people-killed and people-injured fields. These values are
    retained as missing rather than treated as zero.

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
    2018–2025

</div>
""")