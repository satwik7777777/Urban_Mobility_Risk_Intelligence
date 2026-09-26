import base64
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Crash Trends | Urban Mobility Risk Intelligence",
    page_icon="📈",
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

yearly_file = PROCESSED_PATH / "dashboard_yearly_trends.csv"

yearly_df = pd.read_csv(yearly_file)

yearly_df = yearly_df.sort_values("year").reset_index(drop=True)


# ============================================================
# CALCULATIONS
# ============================================================

total_crashes = yearly_df["total_crashes"].sum()
fatal_crashes = yearly_df["fatal_crashes"].sum()
nonfatal_crashes = yearly_df["nonfatal_crashes"].sum()

first_year = int(yearly_df.iloc[0]["year"])
last_year = int(yearly_df.iloc[-1]["year"])

first_year_crashes = yearly_df.iloc[0]["total_crashes"]
last_year_crashes = yearly_df.iloc[-1]["total_crashes"]

overall_change = (
    (last_year_crashes - first_year_crashes)
    / first_year_crashes
) * 100


# YoY percentage change
yearly_df["yoy_change"] = (
    yearly_df["total_crashes"]
    .pct_change()
    * 100
)


# Peak and lowest years
peak_row = yearly_df.loc[
    yearly_df["total_crashes"].idxmax()
]

lowest_row = yearly_df.loc[
    yearly_df["total_crashes"].idxmin()
]


# Largest increase/decrease
yoy_valid = yearly_df.dropna(subset=["yoy_change"])

largest_increase = yoy_valid.loc[
    yoy_valid["yoy_change"].idxmax()
]

largest_decrease = yoy_valid.loc[
    yoy_valid["yoy_change"].idxmin()
]


# ============================================================
# BACKGROUND ARTWORK
# ============================================================
# Same shared-asset detection used on every page: looks for
# "bengaluru_ai_visual" (svg/png/jpg) in the usual asset
# locations so all pages reuse one file. Falls back cleanly to
# the plain dot-grid look if nothing is found.

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


# Small, isolated f-string just for the background rule so the
# large static stylesheet below doesn't need every brace escaped.
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
# GLOBAL STYLING
# ============================================================

st.html("""
<style>
""" + background_css + """

/* ============================================================
   MAIN CONTAINER
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

hr {
    border-color: rgba(148,163,184,0.10) !important;
}


/* ============================================================
   SIDEBAR
   ============================================================ */
/* Transparent so the .stApp background/artwork above shows
   through instead of a separate solid panel. */

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
            rgba(56,189,248,0.35) 0 2px,
            transparent 3px
        );

    background-size: 25px 25px;

    transform: rotate(12deg);

    opacity: 0.9;

    z-index: 1;
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

    z-index: 1;
}


.hero-kicker {
    position: relative;
    z-index: 2;

    color: #38bdf8;

    font-size: 0.72rem;

    font-weight: 850;

    letter-spacing: 2.4px;

    margin-bottom: 10px;
}


.hero-title {
    position: relative;
    z-index: 2;

    color: #f8fafc;

    font-size: 2.35rem;

    font-weight: 850;

    line-height: 1.1;

    max-width: 850px;

    margin-bottom: 12px;
}


.hero-description {
    position: relative;
    z-index: 2;

    color: #aebdce;

    font-size: 0.95rem;

    line-height: 1.65;

    max-width: 820px;
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
   SECTION LABELS
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
   HOVER
   ============================================================ */

.card {
    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease,
        border-color 0.25s ease;
}

.card:hover {
    transform: translateY(-4px);

    box-shadow:
        0 20px 45px rgba(0,0,0,0.42);
}


/* ============================================================
   KPI GRID
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
    color: #38bdf8;
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
    color: #f87171;
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
    color: #fbbf24;
}


/* PURPLE */

.kpi-purple {
    background:
        linear-gradient(
            145deg,
            rgba(50,22,66,0.98),
            rgba(25,12,35,0.98)
        );

    border:
        1px solid rgba(168,85,247,0.26);
}

.kpi-purple::before {
    background: #a855f7;

    box-shadow:
        0 0 18px rgba(168,85,247,0.65);
}

.kpi-purple .kpi-icon {
    background: rgba(168,85,247,0.13);
    color: #c084fc;
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

    padding: 16px 18px 8px 18px;

    box-shadow:
        0 12px 30px rgba(0,0,0,0.22);
}


.chart-panel-red {
    border:
        1px solid rgba(239,68,68,0.15);
}


.chart-panel-title {
    color: #f1f5f9;

    font-size: 0.80rem;

    font-weight: 850;

    letter-spacing: 0.7px;

    margin-bottom: 2px;
}


.chart-panel-subtitle {
    color: #64748b;

    font-size: 0.68rem;

    margin-bottom: 4px;
}


/* ============================================================
   HIGHLIGHT CARDS
   ============================================================ */

.highlight-grid {
    display: grid;

    grid-template-columns:
        repeat(4, minmax(0, 1fr));

    gap: 13px;
}


.highlight {
    min-height: 155px;

    padding: 19px 20px;

    border-radius: 15px;

    position: relative;

    overflow: hidden;
}


.highlight::before {
    content: "";

    position: absolute;

    left: 0;
    top: 0;
    bottom: 0;

    width: 5px;
}


.highlight-title {
    font-size: 0.67rem;

    font-weight: 850;

    letter-spacing: 0.9px;

    margin-bottom: 11px;
}


.highlight-number {
    color: #f8fafc;

    font-size: 1.85rem;

    font-weight: 900;

    line-height: 1;

    margin-bottom: 7px;
}


.highlight-year {
    color: #94a3b8;

    font-size: 0.68rem;

    margin-bottom: 9px;
}


.highlight-description {
    color: #aebccc;

    font-size: 0.74rem;

    line-height: 1.45;
}


/* RED */

.highlight-red {
    background:
        linear-gradient(
            145deg,
            rgba(58,18,27,0.97),
            rgba(28,10,17,0.97)
        );

    border:
        1px solid rgba(239,68,68,0.20);
}

.highlight-red::before {
    background: #ef4444;
}


/* GREEN */

.highlight-green {
    background:
        linear-gradient(
            145deg,
            rgba(7,49,37,0.97),
            rgba(6,25,22,0.97)
        );

    border:
        1px solid rgba(34,197,94,0.20);
}

.highlight-green::before {
    background: #22c55e;
}


/* ORANGE */

.highlight-orange {
    background:
        linear-gradient(
            145deg,
            rgba(61,39,8,0.97),
            rgba(29,19,6,0.97)
        );

    border:
        1px solid rgba(245,158,11,0.20);
}

.highlight-orange::before {
    background: #f59e0b;
}


/* ============================================================
   INSIGHT PANELS
   ============================================================ */

.insight-grid {
    display: grid;

    grid-template-columns:
        repeat(2, minmax(0, 1fr));

    gap: 13px;
}


.insight {
    min-height: 150px;

    padding: 20px 22px;

    border-radius: 15px;

    background:
        linear-gradient(
            145deg,
            rgba(8,34,55,0.96),
            rgba(6,18,30,0.96)
        );

    border:
        1px solid rgba(56,189,248,0.17);
}


.insight-title {
    color: #f1f5f9;

    font-size: 0.82rem;

    font-weight: 850;

    margin-bottom: 10px;
}


.insight-text {
    color: #aebccc;

    font-size: 0.78rem;

    line-height: 1.65;
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

    .highlight-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .insight-grid {
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
        2018–2025 &nbsp; • &nbsp; HISTORICAL TRENDS
    </div>

    <div class="hero-kicker">
        CRASH TRENDS
    </div>

    <div class="hero-title">
        Bengaluru Crash Trends
    </div>

    <div class="hero-description">
        Historical analysis of crash activity, fatality,
        year-over-year changes, and long-term crash patterns
        across Bengaluru from 2018 to 2025.
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

    <div class="kpi kpi-blue card">

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


    <div class="kpi kpi-red card">

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


    <div class="kpi kpi-orange card">

        <div class="kpi-top">

            <div class="kpi-label">
                NON-FATAL CRASHES
            </div>

            <div class="kpi-icon">
                🚗
            </div>

        </div>

        <div class="kpi-value">
            {nonfatal_crashes:,.0f}
        </div>

    </div>


    <div class="kpi kpi-purple card">

        <div class="kpi-top">

            <div class="kpi-label">
                {first_year} → {last_year} CHANGE
            </div>

            <div class="kpi-icon">
                📈
            </div>

        </div>

        <div class="kpi-value">
            {overall_change:+.1f}%
        </div>

    </div>

</div>
""")


# ============================================================
# OVERALL TREND
# ============================================================

st.html("""
<div class="section-label">
    CITYWIDE CRASH ACTIVITY
</div>

<div class="section-title">
    Overall Crash Trend
</div>
""")


fig_trend = go.Figure()

fig_trend.add_trace(
    go.Scatter(
        x=yearly_df["year"],
        y=yearly_df["total_crashes"],
        mode="lines+markers",
        name="Total Crashes",
        line=dict(
            color="#38bdf8",
            width=3
        ),
        marker=dict(
            size=8,
            color="#38bdf8"
        ),
        hovertemplate=
            "<b>%{x}</b><br>"
            "Total Crashes: %{y:,.0f}"
            "<extra></extra>"
    )
)

fig_trend.update_layout(
    height=370,
    margin=dict(l=20, r=20, t=15, b=20),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        color="#aebccc",
        family="Arial"
    ),
    xaxis=dict(
        title=None,
        dtick=1,
        gridcolor="rgba(148,163,184,0.08)",
        zeroline=False
    ),
    yaxis=dict(
        title="Crashes",
        gridcolor="rgba(148,163,184,0.10)",
        zeroline=False
    ),
    hoverlabel=dict(
        bgcolor="#0b1725",
        bordercolor="#38bdf8",
        font_color="#f8fafc"
    ),
    showlegend=False
)


st.html("""
<div class="chart-panel card">

    <div class="chart-panel-title">
        TOTAL CRASHES BY YEAR
    </div>

    <div class="chart-panel-subtitle">
        Annual citywide crash activity from 2018–2025
    </div>

</div>
""")

st.plotly_chart(
    fig_trend,
    use_container_width=True,
    config={"displayModeBar": False}
)


# ============================================================
# FATAL VS NON-FATAL
# ============================================================

st.html("""
<div class="section-label">
    CRASH COMPOSITION
</div>

<div class="section-title">
    Fatal vs Non-Fatal Crashes
</div>
""")


fig_composition = go.Figure()

fig_composition.add_trace(
    go.Bar(
        x=yearly_df["year"],
        y=yearly_df["fatal_crashes"],
        name="Fatal",
        marker_color="#ef4444",
        hovertemplate=
            "<b>%{x}</b><br>"
            "Fatal: %{y:,.0f}"
            "<extra></extra>"
    )
)

fig_composition.add_trace(
    go.Bar(
        x=yearly_df["year"],
        y=yearly_df["nonfatal_crashes"],
        name="Non-Fatal",
        marker_color="#38bdf8",
        hovertemplate=
            "<b>%{x}</b><br>"
            "Non-Fatal: %{y:,.0f}"
            "<extra></extra>"
    )
)

fig_composition.update_layout(
    height=380,
    barmode="group",
    margin=dict(l=20, r=20, t=15, b=20),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        color="#aebccc",
        family="Arial"
    ),
    xaxis=dict(
        title=None,
        dtick=1,
        gridcolor="rgba(148,163,184,0.05)"
    ),
    yaxis=dict(
        title="Number of Crashes",
        gridcolor="rgba(148,163,184,0.10)"
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.01,
        xanchor="right",
        x=1
    ),
    hoverlabel=dict(
        bgcolor="#0b1725",
        font_color="#f8fafc"
    )
)


st.plotly_chart(
    fig_composition,
    use_container_width=True,
    config={"displayModeBar": False}
)


# ============================================================
# YEAR-OVER-YEAR CHANGE
# ============================================================

st.html("""
<div class="section-label">
    YEAR-OVER-YEAR CHANGE
</div>

<div class="section-title">
    Annual Change in Crash Activity
</div>
""")


fig_yoy = go.Figure()

yoy_colors = [
    "#ef4444" if value >= 0 else "#22c55e"
    for value in yearly_df["yoy_change"].fillna(0)
]

fig_yoy.add_trace(
    go.Bar(
        x=yearly_df["year"],
        y=yearly_df["yoy_change"],
        marker_color=yoy_colors,
        hovertemplate=
            "<b>%{x}</b><br>"
            "YoY Change: %{y:+.2f}%"
            "<extra></extra>"
    )
)

fig_yoy.add_hline(
    y=0,
    line_width=1,
    line_color="rgba(148,163,184,0.35)"
)

fig_yoy.update_layout(
    height=350,
    margin=dict(l=20, r=20, t=15, b=20),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        color="#aebccc",
        family="Arial"
    ),
    xaxis=dict(
        title=None,
        dtick=1
    ),
    yaxis=dict(
        title="YoY Change (%)",
        ticksuffix="%",
        gridcolor="rgba(148,163,184,0.10)"
    ),
    hoverlabel=dict(
        bgcolor="#0b1725",
        font_color="#f8fafc"
    ),
    showlegend=False
)


st.plotly_chart(
    fig_yoy,
    use_container_width=True,
    config={"displayModeBar": False}
)


# ============================================================
# CRASH ACTIVITY HIGHLIGHTS
# ============================================================

st.html("""
<div class="section-label">
    CRASH ACTIVITY HIGHLIGHTS
</div>

<div class="section-title">
    Historical Highs, Lows & Changes
</div>
""")


st.html(f"""
<div class="highlight-grid">

    <div class="highlight highlight-red card">

        <div class="highlight-title"
             style="color:#f87171;">
            PEAK CRASH YEAR
        </div>

        <div class="highlight-number">
            {int(peak_row["total_crashes"]):,}
        </div>

        <div class="highlight-year">
            {int(peak_row["year"])}
        </div>

        <div class="highlight-description">
            Highest recorded annual crash volume
            in the analysis period.
        </div>

    </div>


    <div class="highlight highlight-green card">

        <div class="highlight-title"
             style="color:#4ade80;">
            LOWEST CRASH YEAR
        </div>

        <div class="highlight-number">
            {int(lowest_row["total_crashes"]):,}
        </div>

        <div class="highlight-year">
            {int(lowest_row["year"])}
        </div>

        <div class="highlight-description">
            Lowest recorded annual crash volume
            in the analysis period.
        </div>

    </div>


    <div class="highlight highlight-red card">

        <div class="highlight-title"
             style="color:#f87171;">
            LARGEST INCREASE
        </div>

        <div class="highlight-number">
            +{largest_increase["yoy_change"]:.1f}%
        </div>

        <div class="highlight-year">
            {int(largest_increase["year"])}
        </div>

        <div class="highlight-description">
            Largest year-over-year increase
            in total crash activity.
        </div>

    </div>


    <div class="highlight highlight-green card">

        <div class="highlight-title"
             style="color:#4ade80;">
            LARGEST DECREASE
        </div>

        <div class="highlight-number">
            {largest_decrease["yoy_change"]:.1f}%
        </div>

        <div class="highlight-year">
            {int(largest_decrease["year"])}
        </div>

        <div class="highlight-description">
            Largest year-over-year reduction
            in total crash activity.
        </div>

    </div>

</div>
""")


# ============================================================
# TREND INTERPRETATION
# ============================================================

st.html("""
<div class="section-label">
    TREND INTERPRETATION
</div>

<div class="section-title">
    What Changed?
</div>
""")


peak_year = int(peak_row["year"])
lowest_year = int(lowest_row["year"])


st.html(f"""
<div class="insight-grid">

    <div class="insight card">

        <div class="insight-title">
            📈 Overall Pattern
        </div>

        <div class="insight-text">
            Total crashes changed by
            <strong style="color:#38bdf8;">
                {overall_change:+.1f}%
            </strong>
            between {first_year} and {last_year}.
            Crash activity reached its highest level in
            <strong style="color:#f87171;">
                {peak_year}
            </strong>
            and its lowest level in
            <strong style="color:#4ade80;">
                {lowest_year}
            </strong>.
        </div>

    </div>


    <div class="insight card">

        <div class="insight-title">
            ⚠️ Recent Movement
        </div>

        <div class="insight-text">
            The latest annual comparison shows a
            <strong style="color:#38bdf8;">
                {overall_change:+.1f}%
            </strong>
            change between the first and latest
            years of the dataset. Year-over-year
            values should be interpreted alongside
            the longer historical pattern.
        </div>

    </div>

</div>
""")


# ============================================================
# YEARLY TABLE
# ============================================================

st.html("""
<div class="section-label">
    YEARLY SUMMARY
</div>

<div class="section-title">
    Crash Trend Data
</div>
""")


display_df = yearly_df[
    [
        "year",
        "total_crashes",
        "fatal_crashes",
        "nonfatal_crashes",
        "yoy_change"
    ]
].copy()

display_df.columns = [
    "Year",
    "Total Crashes",
    "Fatal Crashes",
    "Non-Fatal Crashes",
    "YoY Change (%)"
]

display_df["Year"] = display_df["Year"].astype(int)

display_df["Total Crashes"] = (
    display_df["Total Crashes"]
    .map(lambda x: f"{x:,.0f}")
)

display_df["Fatal Crashes"] = (
    display_df["Fatal Crashes"]
    .map(lambda x: f"{x:,.0f}")
)

display_df["Non-Fatal Crashes"] = (
    display_df["Non-Fatal Crashes"]
    .map(lambda x: f"{x:,.0f}")
)

display_df["YoY Change (%)"] = (
    display_df["YoY Change (%)"]
    .map(
        lambda x:
        "—" if pd.isna(x)
        else f"{x:+.2f}%"
    )
)


st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# DATA NOTE
# ============================================================

st.html("""
<div class="data-note">

    <strong style="color:#94a3b8;">
        DATA NOTE
    </strong>

    &nbsp;

    Year-over-year comparisons describe changes in the
    available station-level crash records. Missing
    people-killed and people-injured values in 2024 and
    2025 are not treated as zero.

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