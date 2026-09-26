import base64
from pathlib import Path

import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Risk Map | Urban Mobility Risk Intelligence",
    page_icon="🗺️",
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
geo_file = PROCESSED_PATH / "station_risk_geocoded_final.csv"

station_df = pd.read_csv(station_file)
geo_df = pd.read_csv(geo_file)


# ============================================================
# PREPARE DATA
# ============================================================

station_df = station_df.copy()
geo_df = geo_df.copy()

# dashboard_station_master already contains
# latitude and longitude, so use those directly.
map_df = station_df.copy()

# If coordinates are missing from the dashboard dataset,
# fill them from the geocoded file.
if "latitude" not in map_df.columns or "longitude" not in map_df.columns:

    geo_keep = [
        "station",
        "latitude",
        "longitude",
        "location_status"
    ]

    geo_keep = [
        col for col in geo_keep
        if col in geo_df.columns
    ]

    geo_coords = geo_df[geo_keep].copy()

    map_df = map_df.merge(
        geo_coords,
        on="station",
        how="left"
    )

# Remove stations without valid coordinates
map_df = map_df.dropna(
    subset=["latitude", "longitude"]
).copy()


# ============================================================
# CALCULATIONS
# ============================================================

mapped_stations = map_df["station"].nunique()

high_risk = (
    map_df["risk_category"]
    .eq("High")
    .sum()
)

medium_risk = (
    map_df["risk_category"]
    .eq("Medium")
    .sum()
)

low_risk = (
    map_df["risk_category"]
    .eq("Low")
    .sum()
)


# Top 5 risk locations
top_risk = (
    map_df
    .sort_values("risk_score", ascending=False)
    .drop_duplicates(subset=["station"])
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

    max-width: 900px;

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
   CARD HOVER
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
    color: #4ade80;
}


/* ============================================================
   MAP CONTAINER
   ============================================================ */

.map-shell {
    background:
        linear-gradient(
            145deg,
            rgba(8,26,43,0.96),
            rgba(5,15,27,0.96)
        );

    border:
        1px solid rgba(56,189,248,0.15);

    border-radius: 16px;

    padding: 10px;

    box-shadow:
        0 15px 40px rgba(0,0,0,0.30);

    overflow: hidden;
}


/* ============================================================
   TOP RISK CARDS
   ============================================================ */

.risk-grid {
    display: grid;

    grid-template-columns:
        repeat(5, minmax(0, 1fr));

    gap: 12px;
}


.risk-card {
    position: relative;

    min-height: 135px;

    padding: 17px 18px;

    border-radius: 14px;

    overflow: hidden;

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease;
}


.risk-card:hover {
    transform: translateY(-4px);

    box-shadow:
        0 18px 40px rgba(0,0,0,0.40);
}


.risk-card::before {
    content: "";

    position: absolute;

    left: 0;
    top: 0;
    bottom: 0;

    width: 4px;

    background: #ef4444;
}


.risk-rank {
    color: #64748b;

    font-size: 0.62rem;

    font-weight: 850;

    letter-spacing: 1px;

    margin-bottom: 7px;
}


.risk-station {
    color: #f8fafc;

    font-size: 0.90rem;

    font-weight: 850;

    white-space: nowrap;

    overflow: hidden;

    text-overflow: ellipsis;

    margin-bottom: 10px;
}


.risk-score {
    color: #f87171;

    font-size: 1.65rem;

    font-weight: 900;

    line-height: 1;
}


.risk-category {
    color: #94a3b8;

    font-size: 0.63rem;

    margin-top: 5px;
}


.risk-card-red {
    background:
        linear-gradient(
            145deg,
            rgba(58,18,27,0.97),
            rgba(28,10,17,0.97)
        );

    border:
        1px solid rgba(239,68,68,0.20);
}


.risk-card-orange {
    background:
        linear-gradient(
            145deg,
            rgba(61,39,8,0.97),
            rgba(29,19,6,0.97)
        );

    border:
        1px solid rgba(245,158,11,0.20);
}


.risk-card-orange::before {
    background: #f59e0b;
}


.risk-card-orange .risk-score {
    color: #fbbf24;
}


/* ============================================================
   MAP GUIDE
   ============================================================ */

.guide-grid {
    display: grid;

    grid-template-columns:
        repeat(3, minmax(0, 1fr));

    gap: 13px;
}


.guide {
    min-height: 135px;

    padding: 19px 21px;

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


.guide-title {
    color: #f1f5f9;

    font-size: 0.80rem;

    font-weight: 850;

    margin-bottom: 9px;
}


.guide-text {
    color: #aebccc;

    font-size: 0.75rem;

    line-height: 1.55;
}


/* ============================================================
   MAP INSIGHT
   ============================================================ */

.map-insight {
    min-height: 120px;

    padding: 20px 22px;

    border-radius: 15px;

    background:
        linear-gradient(
            145deg,
            rgba(46,21,62,0.96),
            rgba(23,12,33,0.96)
        );

    border:
        1px solid rgba(168,85,247,0.18);
}


.map-insight-title {
    color: #c084fc;

    font-size: 0.75rem;

    font-weight: 850;

    letter-spacing: 0.8px;

    margin-bottom: 8px;
}


.map-insight-text {
    color: #aebccc;

    font-size: 0.77rem;

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

@media (max-width: 1100px) {

    .kpi-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .risk-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .guide-grid {
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
        BENGALURU &nbsp; • &nbsp; 60 STATIONS MAPPED
    </div>

    <div class="hero-kicker">
        GEOGRAPHIC RISK INTELLIGENCE
    </div>

    <div class="hero-title">
        Bengaluru Risk Intelligence Map
    </div>

    <div class="hero-description">
        Geographic visualization of station-level crash risk
        across Bengaluru, highlighting locations with higher
        historical risk, severity, and intervention priority.
    </div>

</div>
""")


# ============================================================
# KEY FIGURES
# ============================================================

st.html("""
<div class="section-label">
    MAP OVERVIEW
</div>
""")


st.html(f"""
<div class="kpi-grid">

    <div class="kpi kpi-blue card">

        <div class="kpi-top">

            <div class="kpi-label">
                STATIONS MAPPED
            </div>

            <div class="kpi-icon">
                📍
            </div>

        </div>

        <div class="kpi-value">
            {mapped_stations}
        </div>

    </div>


    <div class="kpi kpi-red card">

        <div class="kpi-top">

            <div class="kpi-label">
                HIGH RISK
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
                MEDIUM RISK
            </div>

            <div class="kpi-icon">
                ⚠️
            </div>

        </div>

        <div class="kpi-value">
            {medium_risk}
        </div>

    </div>


    <div class="kpi kpi-green card">

        <div class="kpi-top">

            <div class="kpi-label">
                LOWER RISK
            </div>

            <div class="kpi-icon">
                ✓
            </div>

        </div>

        <div class="kpi-value">
            {low_risk}
        </div>

    </div>

</div>
""")


# ============================================================
# MAP
# ============================================================

st.html("""
<div class="section-label">
    INTERACTIVE RISK MAP
</div>

<div class="section-title">
    Station-Level Geographic Risk
</div>
""")


# Bengaluru center
m = folium.Map(
    location=[12.9716, 77.5946],
    zoom_start=11,
    tiles="OpenStreetMap",
    control_scale=True
)


# ------------------------------------------------------------
# Marker colors
# ------------------------------------------------------------

def marker_color(category):

    if category == "High":
        return "#ef4444"

    if category == "Medium":
        return "#f59e0b"

    return "#22c55e"


# ------------------------------------------------------------
# Add station markers
# ------------------------------------------------------------

for _, row in map_df.iterrows():

    station = row["station"]
    category = row["risk_category"]
    score = row["risk_score"]

    color = marker_color(category)

    fatal_pct = row.get("fatal_crash_pct", None)

    if pd.notna(fatal_pct):
        severity_text = f"{fatal_pct:.2f}%"
    else:
        severity_text = "N/A"

    popup_html = f"""
    <div style="
        font-family:Arial;
        width:230px;
        color:#111827;
    ">

        <h4 style="
            margin-bottom:8px;
            color:#111827;
        ">
            {station}
        </h4>

        <b>Risk Score:</b>
        {score:.2f}
        <br>

        <b>Risk Category:</b>
        {category}
        <br>

        <b>Fatal Crash Share:</b>
        {severity_text}

    </div>
    """

    # High-risk stations receive a larger circle
    if category == "High":

        folium.CircleMarker(
            location=[
                row["latitude"],
                row["longitude"]
            ],
            radius=11,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.30,
            weight=2
        ).add_to(m)

        folium.CircleMarker(
            location=[
                row["latitude"],
                row["longitude"]
            ],
            radius=6,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.95,
            weight=2,
            popup=folium.Popup(
                popup_html,
                max_width=280
            ),
            tooltip=f"{station} • High Risk"
        ).add_to(m)

    else:

        folium.CircleMarker(
            location=[
                row["latitude"],
                row["longitude"]
            ],
            radius=6,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.85,
            weight=1,
            popup=folium.Popup(
                popup_html,
                max_width=280
            ),
            tooltip=f"{station} • {category}"
        ).add_to(m)


# ------------------------------------------------------------
# Legend
# ------------------------------------------------------------

legend_html = """
<div style="
    position: fixed;
    bottom: 25px;
    left: 25px;
    z-index: 9999;

    background: rgba(5,15,28,0.95);

    padding: 12px 15px;

    border-radius: 10px;

    border: 1px solid rgba(56,189,248,0.25);

    box-shadow: 0 8px 25px rgba(0,0,0,0.35);

    font-family: Arial;
    font-size: 12px;
    color: #e2e8f0;
">

    <div style="
        font-weight:700;
        margin-bottom:8px;
        color:#f8fafc;
    ">
        RISK CATEGORY
    </div>

    <div style="margin-bottom:5px;">
        <span style="
            display:inline-block;
            width:10px;
            height:10px;
            border-radius:50%;
            background:#ef4444;
            margin-right:7px;
        "></span>
        High Risk
    </div>

    <div style="margin-bottom:5px;">
        <span style="
            display:inline-block;
            width:10px;
            height:10px;
            border-radius:50%;
            background:#f59e0b;
            margin-right:7px;
        "></span>
        Medium Risk
    </div>

    <div>
        <span style="
            display:inline-block;
            width:10px;
            height:10px;
            border-radius:50%;
            background:#22c55e;
            margin-right:7px;
        "></span>
        Lower Risk
    </div>

</div>
"""

m.get_root().html.add_child(
    folium.Element(legend_html)
)


# ------------------------------------------------------------
# Render map
# ------------------------------------------------------------

st.html("""
<div class="map-shell">
""")

st_folium(
    m,
    use_container_width=True,
    height=650,
    returned_objects=[]
)

st.html("""
</div>
""")


# ============================================================
# TOP RISK LOCATIONS
# ============================================================

st.html("""
<div class="section-label">
    HIGHEST-RISK LOCATIONS
</div>

<div class="section-title">
    Top Risk Stations on the Map
</div>
""")


risk_cards = ""

for i, (_, row) in enumerate(top_risk.iterrows(), start=1):

    category = row["risk_category"]

    if category == "High":
        card_class = "risk-card-red"
    else:
        card_class = "risk-card-orange"

    risk_cards += f"""
    <div class="risk-card {card_class}">

        <div class="risk-rank">
            RANK #{i}
        </div>

        <div class="risk-station">
            {row["station"]}
        </div>

        <div class="risk-score">
            {row["risk_score"]:.1f}
        </div>

        <div class="risk-category">
            {category} Risk
        </div>

    </div>
    """


st.html(f"""
<div class="risk-grid">

    {risk_cards}

</div>
""")


# ============================================================
# HOW TO READ THE MAP
# ============================================================

st.html("""
<div class="section-label">
    MAP INTERPRETATION
</div>

<div class="section-title">
    How to Read the Map
</div>
""")


st.html("""
<div class="guide-grid">

    <div class="guide card">

        <div class="guide-title">
            🔴 High Risk
        </div>

        <div class="guide-text">
            High-risk stations have elevated composite risk
            scores based on crash frequency, fatality,
            severity, and recent activity.
        </div>

    </div>


    <div class="guide card">

        <div class="guide-title">
            🟠 Medium Risk
        </div>

        <div class="guide-text">
            Medium-risk stations show notable crash activity
            or severity but fall below the project's high-risk
            threshold.
        </div>

    </div>


    <div class="guide card">

        <div class="guide-title">
            🟢 Lower Risk
        </div>

        <div class="guide-text">
            Lower-risk stations have comparatively lower
            composite risk scores within the analyzed
            station dataset.
        </div>

    </div>

</div>
""")


# ============================================================
# MAP INSIGHT
# ============================================================

st.html("""
<div class="section-label">
    GEOGRAPHIC INSIGHT
</div>

<div class="section-title">
    What the Map Reveals
</div>
""")


if len(top_risk) >= 3:

    top_three = (
        top_risk["station"]
        .head(3)
        .tolist()
    )

    top_three_text = ", ".join(top_three)

else:

    top_three_text = ", ".join(
        top_risk["station"].tolist()
    )


st.html(f"""
<div class="map-insight card">

    <div class="map-insight-title">
        SPATIAL RISK CONCENTRATION
    </div>

    <div class="map-insight-text">

        The geographic view highlights how station-level
        risk is distributed across Bengaluru. The highest
        composite risk scores in the current analysis are
        associated with locations including
        <strong style="color:#f8fafc;">
            {top_three_text}
        </strong>.

        The map should be interpreted together with the
        historical risk score, data coverage, crash severity,
        and trend analysis rather than as a standalone
        prediction of future crashes.

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

    Station coordinates represent the mapped station or
    locality area. Some coordinates were obtained through
    geocoding while others were manually assigned as
    approximate locality coordinates. They should therefore
    not be interpreted as exact crash locations.

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
    GEOGRAPHIC RISK MAP

</div>
""")