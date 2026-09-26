import base64
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Risk Intelligence | Urban Mobility Risk Intelligence",
    page_icon="⚠️",
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

station_file = PROCESSED_PATH / "dashboard_station_master.csv"
priority_file = PROCESSED_PATH / "final_intervention_priority_ranking.csv"

station_df = pd.read_csv(station_file)
priority_df = pd.read_csv(priority_file)


# ============================================================
# PREPARATION
# ============================================================

station_df = station_df.copy()
priority_df = priority_df.copy()

station_df = station_df.sort_values(
    "risk_score",
    ascending=False
).reset_index(drop=True)

priority_df = priority_df.sort_values(
    "priority_index",
    ascending=False
).reset_index(drop=True)


# ============================================================
# CALCULATIONS
# ============================================================

total_stations = station_df["station"].nunique()

high_risk = (
    station_df["risk_category"]
    .eq("High")
    .sum()
)

medium_risk = (
    station_df["risk_category"]
    .eq("Medium")
    .sum()
)

low_risk = (
    station_df["risk_category"]
    .eq("Low")
    .sum()
)

average_risk = station_df["risk_score"].mean()

top_station = station_df.iloc[0]["station"]
top_risk_score = station_df.iloc[0]["risk_score"]

top_severity_station = station_df.loc[
    station_df["fatal_crash_pct"].idxmax()
]

increasing_stations = (
    station_df["trend_category"]
    .eq("Increasing")
    .sum()
    if "trend_category" in station_df.columns
    else 0
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
   INSIGHT CARDS
   ============================================================ */

.insight-grid {
    display: grid;

    grid-template-columns:
        repeat(3, minmax(0, 1fr));

    gap: 13px;
}


.insight {
    min-height: 145px;

    padding: 20px 21px;

    border-radius: 15px;

    position: relative;

    overflow: hidden;
}


.insight-title {
    font-size: 0.68rem;

    font-weight: 850;

    letter-spacing: 0.9px;

    margin-bottom: 11px;
}


.insight-number {
    color: #f8fafc;

    font-size: 1.90rem;

    font-weight: 900;

    line-height: 1;

    margin-bottom: 9px;
}


.insight-description {
    color: #aebccc;

    font-size: 0.75rem;

    line-height: 1.55;
}


.insight-blue {
    background:
        linear-gradient(
            145deg,
            rgba(7,38,63,0.97),
            rgba(6,20,34,0.97)
        );

    border:
        1px solid rgba(56,189,248,0.20);
}


.insight-red {
    background:
        linear-gradient(
            145deg,
            rgba(58,18,27,0.97),
            rgba(28,10,17,0.97)
        );

    border:
        1px solid rgba(239,68,68,0.20);
}


.insight-orange {
    background:
        linear-gradient(
            145deg,
            rgba(61,39,8,0.97),
            rgba(29,19,6,0.97)
        );

    border:
        1px solid rgba(245,158,11,0.20);
}


/* ============================================================
   TABLE
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
        60 STATIONS &nbsp; • &nbsp; RISK INTELLIGENCE
    </div>

    <div class="hero-kicker">
        RISK INTELLIGENCE
    </div>

    <div class="hero-title">
        Station-Level Risk Intelligence
    </div>

    <div class="hero-description">
        A station-level assessment combining crash frequency,
        fatality, severity, recent activity, and historical
        patterns to identify areas with elevated road-crash risk.
    </div>

</div>
""")


# ============================================================
# KEY FIGURES
# ============================================================

st.html("""
<div class="section-label">
    RISK OVERVIEW
</div>
""")


st.html(f"""
<div class="kpi-grid">

    <div class="kpi kpi-red card">

        <div class="kpi-top">

            <div class="kpi-label">
                HIGH-RISK STATIONS
            </div>

            <div class="kpi-icon">
                🚨
            </div>

        </div>

        <div class="kpi-value">
            {high_risk}
        </div>

    </div>


    <div class="kpi kpi-orange card">

        <div class="kpi-top">

            <div class="kpi-label">
                MEDIUM-RISK STATIONS
            </div>

            <div class="kpi-icon">
                ⚠️
            </div>

        </div>

        <div class="kpi-value">
            {medium_risk}
        </div>

    </div>


    <div class="kpi kpi-green card"
         style="
         background:linear-gradient(
             145deg,
             rgba(7,49,37,0.98),
             rgba(6,25,22,0.98)
         );
         border:1px solid rgba(34,197,94,0.23);
         position:relative;
         overflow:hidden;
         min-height:118px;
         padding:18px 19px;
         border-radius:13px;
         box-shadow:0 12px 30px rgba(0,0,0,0.28);
         ">

        <div style="
            position:absolute;
            left:0;
            top:0;
            bottom:0;
            width:5px;
            background:#22c55e;
            box-shadow:0 0 18px rgba(34,197,94,0.65);
        "></div>

        <div class="kpi-top">

            <div class="kpi-label">
                LOWER-RISK STATIONS
            </div>

            <div class="kpi-icon"
                 style="
                 background:rgba(34,197,94,0.12);
                 color:#4ade80;
                 ">
                ✓
            </div>

        </div>

        <div class="kpi-value">
            {low_risk}
        </div>

    </div>


    <div class="kpi kpi-blue card">

        <div class="kpi-top">

            <div class="kpi-label">
                AVERAGE RISK SCORE
            </div>

            <div class="kpi-icon">
                📊
            </div>

        </div>

        <div class="kpi-value">
            {average_risk:.1f}
        </div>

    </div>

</div>
""")


# ============================================================
# RISK SCORE RANKING
# ============================================================

st.html("""
<div class="section-label">
    STATION RISK PROFILE
</div>

<div class="section-title">
    Station Risk Score Ranking
</div>
""")


risk_top = (
    station_df
    .sort_values("risk_score", ascending=True)
    .tail(15)
    .sort_values("risk_score", ascending=True)
)


risk_colors = []

for category in risk_top["risk_category"]:
    if category == "High":
        risk_colors.append("#ef4444")
    elif category == "Medium":
        risk_colors.append("#f59e0b")
    else:
        risk_colors.append("#22c55e")


fig_risk = go.Figure()

fig_risk.add_trace(
    go.Bar(
        x=risk_top["risk_score"],
        y=risk_top["station"],
        orientation="h",
        marker_color=risk_colors,
        hovertemplate=
            "<b>%{y}</b><br>"
            "Risk Score: %{x:.2f}"
            "<extra></extra>"
    )
)

fig_risk.update_layout(
    height=560,
    margin=dict(l=20, r=30, t=15, b=20),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        color="#aebccc",
        family="Arial"
    ),
    xaxis=dict(
        title="Risk Score",
        range=[
            0,
            max(risk_top["risk_score"].max() * 1.10, 100)
        ],
        gridcolor="rgba(148,163,184,0.10)",
        zeroline=False
    ),
    yaxis=dict(
        title=None,
        tickfont=dict(size=11)
    ),
    showlegend=False,
    hoverlabel=dict(
        bgcolor="#0b1725",
        font_color="#f8fafc"
    )
)


st.plotly_chart(
    fig_risk,
    use_container_width=True,
    config={"displayModeBar": False}
)


# ============================================================
# SEVERITY
# ============================================================

st.html("""
<div class="section-label">
    CRASH SEVERITY
</div>

<div class="section-title">
    Fatal Crash Severity by Station
</div>
""")


severity_top = (
    station_df
    .dropna(subset=["fatal_crash_pct"])
    .sort_values("fatal_crash_pct", ascending=False)
    .head(15)
    .sort_values("fatal_crash_pct", ascending=True)
)


fig_severity = go.Figure()

fig_severity.add_trace(
    go.Bar(
        x=severity_top["fatal_crash_pct"],
        y=severity_top["station"],
        orientation="h",
        marker_color="#ef4444",
        hovertemplate=
            "<b>%{y}</b><br>"
            "Fatal Crash Share: %{x:.2f}%"
            "<extra></extra>"
    )
)

fig_severity.update_layout(
    height=560,
    margin=dict(l=20, r=30, t=15, b=20),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        color="#aebccc",
        family="Arial"
    ),
    xaxis=dict(
        title="Fatal Crash Percentage",
        ticksuffix="%",
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
    fig_severity,
    use_container_width=True,
    config={"displayModeBar": False}
)


# ============================================================
# RISK VS SEVERITY
# ============================================================

st.html("""
<div class="section-label">
    RISK RELATIONSHIP
</div>

<div class="section-title">
    Risk Score vs Crash Severity
</div>
""")


scatter_df = station_df.dropna(
    subset=["risk_score", "fatal_crash_pct"]
).copy()


fig_scatter = px.scatter(
    scatter_df,
    x="risk_score",
    y="fatal_crash_pct",
    color="risk_category",
    hover_name="station",
    hover_data={
        "risk_score": ":.2f",
        "fatal_crash_pct": ":.2f",
        "risk_category": True
    },
    color_discrete_map={
        "High": "#ef4444",
        "Medium": "#f59e0b",
        "Low": "#22c55e"
    }
)


fig_scatter.update_traces(
    marker=dict(
        size=10,
        line=dict(
            width=1,
            color="#0b1725"
        )
    )
)


fig_scatter.update_layout(
    height=450,
    margin=dict(l=20, r=20, t=15, b=20),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        color="#aebccc",
        family="Arial"
    ),
    xaxis=dict(
        title="Risk Score",
        gridcolor="rgba(148,163,184,0.10)"
    ),
    yaxis=dict(
        title="Fatal Crash Percentage",
        ticksuffix="%",
        gridcolor="rgba(148,163,184,0.10)"
    ),
    legend=dict(
        title=None
    ),
    hoverlabel=dict(
        bgcolor="#0b1725",
        font_color="#f8fafc"
    )
)


st.plotly_chart(
    fig_scatter,
    use_container_width=True,
    config={"displayModeBar": False}
)


# ============================================================
# STATION CRASH TREND
# ============================================================

st.html("""
<div class="section-label">
    HISTORICAL STATION TREND
</div>

<div class="section-title">
    Crash Trend by Station
</div>
""")


trend_df = (
    station_df
    .dropna(subset=["crash_trend_per_year"])
    .sort_values("crash_trend_per_year", ascending=False)
)


trend_top = pd.concat(
    [
        trend_df.head(8),
        trend_df.tail(7)
    ]
).drop_duplicates(subset=["station"])


trend_top = trend_top.sort_values(
    "crash_trend_per_year"
)


trend_colors = [
    "#ef4444" if x > 0 else "#22c55e"
    for x in trend_top["crash_trend_per_year"]
]


fig_trend = go.Figure()

fig_trend.add_trace(
    go.Bar(
        x=trend_top["crash_trend_per_year"],
        y=trend_top["station"],
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
    height=540,
    margin=dict(l=20, r=30, t=15, b=20),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        color="#aebccc",
        family="Arial"
    ),
    xaxis=dict(
        title="Average Change in Crashes per Year",
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
# RECENT VS HISTORICAL
# ============================================================

st.html("""
<div class="section-label">
    RECENT ACTIVITY
</div>

<div class="section-title">
    Recent vs Historical Crash Activity
</div>
""")


recent_df = station_df[
    [
        "station",
        "avg_annual_crashes",
        "recent_avg_annual_crashes",
        "recent_vs_historical_pct"
    ]
].dropna(
    subset=[
        "avg_annual_crashes",
        "recent_avg_annual_crashes"
    ]
).copy()


recent_df = recent_df.sort_values(
    "recent_vs_historical_pct",
    ascending=False
).head(15)


fig_recent = go.Figure()

fig_recent.add_trace(
    go.Bar(
        x=recent_df["station"],
        y=recent_df["avg_annual_crashes"],
        name="Historical Average",
        marker_color="#64748b"
    )
)

fig_recent.add_trace(
    go.Bar(
        x=recent_df["station"],
        y=recent_df["recent_avg_annual_crashes"],
        name="Recent Average",
        marker_color="#38bdf8"
    )
)

fig_recent.update_layout(
    height=460,
    barmode="group",
    margin=dict(l=20, r=20, t=15, b=100),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        color="#aebccc",
        family="Arial"
    ),
    xaxis=dict(
        title=None,
        tickangle=-45
    ),
    yaxis=dict(
        title="Average Annual Crashes",
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
    fig_recent,
    use_container_width=True,
    config={"displayModeBar": False}
)


# ============================================================
# RISK INSIGHTS
# ============================================================

st.html("""
<div class="section-label">
    RISK INSIGHTS
</div>

<div class="section-title">
    What the Risk Model Shows
</div>
""")


st.html(f"""
<div class="insight-grid">

    <div class="insight insight-red card">

        <div class="insight-title"
             style="color:#f87171;">
            HIGHEST RISK SCORE
        </div>

        <div class="insight-number">
            {top_risk_score:.1f}
        </div>

        <div class="insight-description">
            <strong style="color:#f8fafc;">
                {top_station}
            </strong>
            has the highest composite risk score
            in the station-level risk assessment.
        </div>

    </div>


    <div class="insight insight-orange card">

        <div class="insight-title"
             style="color:#fbbf24;">
            HIGHEST SEVERITY SHARE
        </div>

        <div class="insight-number">
            {top_severity_station["fatal_crash_pct"]:.1f}%
        </div>

        <div class="insight-description">
            <strong style="color:#f8fafc;">
                {top_severity_station["station"]}
            </strong>
            has the highest fatal-crash percentage
            among stations with available severity data.
        </div>

    </div>


    <div class="insight insight-blue card">

        <div class="insight-title"
             style="color:#38bdf8;">
            STATIONS ASSESSED
        </div>

        <div class="insight-number">
            {total_stations}
        </div>

        <div class="insight-description">
            The risk framework evaluates station-level
            crash frequency, fatality, severity, recent
            activity, and historical patterns.
        </div>

    </div>

</div>
""")


# ============================================================
# TOP RISK TABLE
# ============================================================

st.html("""
<div class="section-label">
    PRIORITY STATIONS
</div>

<div class="section-title">
    Top Risk Stations
</div>
""")


top_table = station_df[
    [
        "risk_rank",
        "station",
        "risk_score",
        "risk_category",
        "data_coverage",
        "recent_data_status"
    ]
].head(15).copy()


top_table.columns = [
    "Rank",
    "Station",
    "Risk Score",
    "Risk Category",
    "Data Coverage",
    "Recent Data"
]


top_table["Risk Score"] = (
    top_table["Risk Score"]
    .round(2)
)


st.dataframe(
    top_table,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# INTERPRETATION
# ============================================================

st.html("""
<div class="section-label">
    INTERPRETATION
</div>

<div class="section-title">
    How to Read the Risk Score
</div>
""")


st.html("""
<div class="insight-grid">

    <div class="insight insight-blue card">

        <div class="insight-title"
             style="color:#38bdf8;">
            CRASH FREQUENCY
        </div>

        <div class="insight-description">
            Measures the historical level of crash activity
            associated with a station. Higher historical
            crash activity contributes to a higher risk score.
        </div>

    </div>


    <div class="insight insight-red card">

        <div class="insight-title"
             style="color:#f87171;">
            FATALITY & SEVERITY
        </div>

        <div class="insight-description">
            Fatal crashes and crash severity contribute to
            the assessment so that the model considers not
            only how frequently crashes occur, but also
            their seriousness.
        </div>

    </div>


    <div class="insight insight-orange card">

        <div class="insight-title"
             style="color:#fbbf24;">
            RECENT ACTIVITY
        </div>

        <div class="insight-description">
            Recent crash activity is included to capture
            whether a station's current pattern remains
            elevated compared with its historical record.
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

    Risk categories are based on the project's composite
    station-level risk score. Stations have different
    historical coverage, so the data-coverage field should
    be considered when interpreting comparisons. The risk
    score is a relative analytical measure and should not
    be interpreted as an exact probability of a crash.

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
    RISK INTELLIGENCE

</div>
""")