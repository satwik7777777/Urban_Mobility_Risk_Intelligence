import base64
from pathlib import Path

import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Urban Mobility Risk Intelligence",
    page_icon="🚦",
    layout="wide"
)


# ============================================================
# PATHS
# ============================================================
# The previous single hardcoded path silently failed whenever the
# folder layout didn't match exactly, showing the fallback pattern
# instead of the real image. This checks several likely locations
# and falls back to a recursive search for the filename before
# giving up.

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
IMAGE_STEM = "bengaluru_ai_visual"
IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg", ".svg"]

CANDIDATE_DIRS = [
    PROJECT_ROOT / "dashboard" / "assets",
    SCRIPT_DIR / "dashboard" / "assets",
    SCRIPT_DIR / "assets",
    PROJECT_ROOT / "assets",
    SCRIPT_DIR,
    PROJECT_ROOT,
]

CANDIDATE_PATHS = [
    d / f"{IMAGE_STEM}{ext}"
    for d in CANDIDATE_DIRS
    for ext in IMAGE_EXTENSIONS
]

IMAGE_PATH = next((p for p in CANDIDATE_PATHS if p.exists()), None)

if IMAGE_PATH is None:
    # Last resort: search a couple of levels down from the project
    # root for a file with this stem, in case it's nested somewhere
    # none of the guesses above covered.
    for ext in IMAGE_EXTENSIONS:
        matches = list(PROJECT_ROOT.rglob(f"{IMAGE_STEM}{ext}"))
        if matches:
            IMAGE_PATH = matches[0]
            break



# ============================================================
# GLOBAL CSS
# ============================================================
# NOTE: Colors/gradients pulled into CSS custom properties so the
# four KPI variants (red/orange/green/purple) share one ruleset
# instead of four near-duplicate blocks. Added hover states on
# .module and .kpi so the dashboard feels interactive, not static.

st.html("""
<style>

:root {
    --bg-base: #060a12;
    --card-border: rgba(56,189,248,0.13);
    --text-dim: #718198;
    --text-faint: #64748b;
    --text-bright: #f8fafc;

    --red-a: #471522;   --red-b: #220b13;   --red-border: rgba(239,68,68,0.30);   --red-label: #fb7185;
    --orange-a: #4b3108; --orange-b: #241905; --orange-border: rgba(245,158,11,0.30); --orange-label: #fbbf24;
    --green-a: #063c2c;  --green-b: #052219;  --green-border: rgba(34,197,94,0.30);  --green-label: #4ade80;
    --purple-a: #3c1850; --purple-b: #210c2e; --purple-border: rgba(168,85,247,0.30); --purple-label: #d8b4fe;
}

/* -----------------------------------------------------------
   SIDEBAR
----------------------------------------------------------- */
/* Transparent so the same .stApp gradient/background shows
   through underneath it instead of a separate solid block —
   this is what makes the sidebar feel merged into the page
   rather than a different-colored panel next to it. */

section[data-testid="stSidebar"] {
    background: transparent;
    border-right: 1px solid rgba(56,189,248,0.10);
}

/* -----------------------------------------------------------
   APP BACKGROUND
----------------------------------------------------------- */

.stApp {
    background:
        radial-gradient(circle at 15% 15%, rgba(14,165,233,0.10), transparent 35%),
        radial-gradient(circle at 85% 80%, rgba(168,85,247,0.10), transparent 38%),
        var(--bg-base);
}

/* -----------------------------------------------------------
   MAIN CONTAINER
----------------------------------------------------------- */

.block-container {
    max-width: 1450px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

/* -----------------------------------------------------------
   HERO
----------------------------------------------------------- */

.hero {
    position: relative;
    min-height: 470px;
    overflow: hidden;
    border-radius: 24px;
    border: 1px solid rgba(56,189,248,0.20);
    background: linear-gradient(105deg,
        rgba(4,22,39,0.98) 0%,
        rgba(4,18,32,0.94) 47%,
        rgba(3,10,20,0.78) 100%);
    box-shadow: 0 25px 70px rgba(0,0,0,0.45);
}

.hero-image {
    position: absolute;
    right: 0;
    top: 0;
    width: 58%;
    height: 100%;
    background-size: cover;
    background-position: center right;
}

.hero-image.no-image {
    /* Fallback pattern shown when the asset file is missing,
       so a broken path doesn't just render blank/silent. */
    background-image:
        linear-gradient(135deg, rgba(56,189,248,0.08) 25%, transparent 25%),
        linear-gradient(225deg, rgba(56,189,248,0.08) 25%, transparent 25%),
        linear-gradient(45deg, rgba(56,189,248,0.08) 25%, transparent 25%),
        linear-gradient(315deg, rgba(56,189,248,0.08) 25%, transparent 25%);
    background-position: 20px 0, 20px 0, 0 0, 0 0;
    background-size: 40px 40px;
    background-color: #061321;
}

.hero-content {
    position: relative;
    z-index: 5;
    width: 72%;
    padding: 58px 45px;
}

.kicker {
    color: #22d3ee;
    font-size: 0.82rem;
    font-weight: 900;
    letter-spacing: 2.8px;
    margin-bottom: 18px;
}

.title-box {
    display: inline-block;
    background: rgba(8,28,45,0.75);
    border: 1px solid rgba(56,189,248,0.25);
    border-radius: 18px;
    padding: 26px 32px;
    margin-bottom: 22px;
}

.title {
    color: var(--text-bright);
    font-size: 3.7rem;
    font-weight: 900;
    line-height: 1.04;
    letter-spacing: -1.3px;
    margin-bottom: 0;
}

.title span {
    color: #22d3ee;
}

.description {
    color: #b4c2d3;
    font-size: 1.05rem;
    line-height: 1.75;
    max-width: 650px;
}

.badges {
    display: flex;
    gap: 10px;
    margin-top: 27px;
}

.badge {
    padding: 12px 15px;
    border-radius: 11px;
    background: rgba(4,15,27,0.82);
    border: 1px solid rgba(56,189,248,0.15);
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.badge:hover {
    transform: translateY(-2px);
    border-color: rgba(56,189,248,0.40);
}

.badge-number {
    color: var(--text-bright);
    font-size: 1.05rem;
    font-weight: 900;
}

.badge-label {
    color: var(--text-faint);
    font-size: 0.56rem;
    font-weight: 850;
    letter-spacing: 0.7px;
    margin-top: 3px;
}

/* -----------------------------------------------------------
   SECTION LABEL
----------------------------------------------------------- */

.section-label {
    color: var(--text-faint);
    font-size: 0.66rem;
    font-weight: 900;
    letter-spacing: 2px;
    margin-top: 30px;
    margin-bottom: 12px;
}

/* -----------------------------------------------------------
   MODULES
----------------------------------------------------------- */

.modules {
    display: grid;
    grid-template-columns: repeat(6, minmax(0,1fr));
    gap: 11px;
}

.module {
    min-height: 125px;
    padding: 16px;
    border-radius: 14px;
    background: linear-gradient(145deg, rgba(8,28,45,0.98), rgba(5,15,27,0.98));
    border: 1px solid var(--card-border);
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    cursor: default;
}

.module:hover {
    transform: translateY(-3px);
    border-color: rgba(56,189,248,0.45);
    box-shadow: 0 12px 30px rgba(0,0,0,0.35);
}

.module-icon {
    font-size: 2.1rem;
    margin-bottom: 10px;
}

.module-title {
    color: var(--text-bright);
    font-size: 0.88rem;
    font-weight: 900;
    margin-bottom: 6px;
}

.module-text {
    color: var(--text-dim);
    font-size: 0.7rem;
    line-height: 1.45;
}

/* -----------------------------------------------------------
   KPI CARDS
----------------------------------------------------------- */

.kpi {
    padding: 17px;
    min-height: 105px;
    border-radius: 14px;
    transition: transform 0.2s ease;
}

.kpi:hover {
    transform: translateY(-3px);
}

.kpi-label {
    font-size: 0.72rem;
    font-weight: 900;
    letter-spacing: 0.7px;
}

.kpi-value {
    color: var(--text-bright);
    font-size: 2.2rem;
    font-weight: 900;
    margin-top: 8px;
}

.red    { background: linear-gradient(145deg, var(--red-a), var(--red-b));       border: 1px solid var(--red-border); }
.red .kpi-label { color: var(--red-label); }

.orange { background: linear-gradient(145deg, var(--orange-a), var(--orange-b)); border: 1px solid var(--orange-border); }
.orange .kpi-label { color: var(--orange-label); }

.green  { background: linear-gradient(145deg, var(--green-a), var(--green-b));   border: 1px solid var(--green-border); }
.green .kpi-label { color: var(--green-label); }

.purple { background: linear-gradient(145deg, var(--purple-a), var(--purple-b)); border: 1px solid var(--purple-border); }
.purple .kpi-label { color: var(--purple-label); }

/* -----------------------------------------------------------
   FOOTER
----------------------------------------------------------- */

.footer {
    text-align: center;
    color: #405069;
    font-size: 0.60rem;
    letter-spacing: 1px;
    margin-top: 30px;
}

/* -----------------------------------------------------------
   MOBILE
----------------------------------------------------------- */

@media (max-width: 1000px) {
    .hero-content {
        width: 100%;
        background: rgba(4,18,32,0.78);
    }
    .title {
        font-size: 2.3rem;
    }
    .hero-image {
        width: 100%;
        opacity: 0.35;
    }
    .modules {
        grid-template-columns: repeat(2,1fr);
    }
}

</style>
""")


# ============================================================
# HERO IMAGE (with graceful fallback if the asset is missing)
# ============================================================

if IMAGE_PATH is not None:
    with open(IMAGE_PATH, "rb") as f:
        encoded_image = base64.b64encode(f.read()).decode()
    mime_type = "image/svg+xml" if IMAGE_PATH.suffix == ".svg" else "image/png"
    image_url = f"data:{mime_type};base64,{encoded_image}"
    hero_image_class = "hero-image"
    hero_image_style = (
        "background-image: linear-gradient(90deg,"
        "#061321 0%, rgba(6,19,33,0.9) 12%,"
        "rgba(6,19,33,0.55) 35%, rgba(6,19,33,0.15) 65%,"
        "rgba(6,19,33,0) 100%),"
        f"url('{image_url}');"
    )
else:
    hero_image_class = "hero-image no-image"
    hero_image_style = ""
    st.toast(
        f"Hero visual '{IMAGE_STEM}' not found — showing fallback pattern.",
        icon="⚠️",
    )


# ============================================================
# HERO
# ============================================================

hero_html = f"""
<div class="hero">

    <div class="{hero_image_class}" style="{hero_image_style}"></div>

    <div class="hero-content">

        <div class="kicker">
            URBAN MOBILITY RISK INTELLIGENCE
        </div>

        <div class="title-box">
            <div class="title">
                Bengaluru Road Crash
                <br>
                <span>Risk Intelligence</span>
            </div>
        </div>

        <div class="description">
            A data-driven dashboard analyzing Bengaluru's
            road-crash patterns from 2018–2025 through
            historical trends, station-level risk assessment,
            geographic visualization, intervention
            prioritization, and predictive analysis.
        </div>

        <div class="badges">

            <div class="badge">
                <div class="badge-number">2018–2025</div>
                <div class="badge-label">8 YEARS OF DATA</div>
            </div>

            <div class="badge">
                <div class="badge-number">60</div>
                <div class="badge-label">STATIONS ANALYZED</div>
            </div>

            <div class="badge">
                <div class="badge-number">2026</div>
                <div class="badge-label">PREDICTIVE OUTLOOK</div>
            </div>

        </div>

    </div>

</div>
"""

st.html(hero_html)


# ============================================================
# EXPLORE — module data driven from a single list so adding /
# reordering sections later means editing one place, not the HTML.
# ============================================================

MODULES = [
    ("📊", "Overview", "Project insights, data coverage and key findings."),
    ("📈", "Crash Trends", "Historical crash patterns from 2018–2025."),
    ("⚠️", "Risk Intelligence", "Station-level risk, severity and trends."),
    ("🗺️", "Risk Map", "Geographic distribution of station risk."),
    ("🔮", "Predictive Risk", "Historical baseline for the 2026 outlook."),
    ("📋", "Summary Results", "Final findings, applications and limitations."),
]

modules_html = "".join(
    f"""
    <div class="module">
        <div class="module-icon">{icon}</div>
        <div class="module-title">{title}</div>
        <div class="module-text">{text}</div>
    </div>
    """
    for icon, title, text in MODULES
)

st.html(f"""
<div class="section-label">EXPLORE THE COMPLETE ANALYSIS</div>
<div class="modules">
{modules_html}
</div>
""")


# ============================================================
# PROJECT METRICS
# ============================================================

st.html('<div class="section-label">KEY PROJECT METRICS</div>')

KPIS = [
    ("red", "🚗 TOTAL CRASHES", "34,229"),
    ("orange", "🚨 FATAL CRASHES", "5,941"),
    ("green", "📈 HIGH-RISK STATIONS", "3"),
    ("purple", "🎯 CRITICAL PRIORITIES", "5"),
]

cols = st.columns(4, gap="medium")

for col, (color, label, value) in zip(cols, KPIS):
    with col:
        st.html(f"""
        <div class="kpi {color}">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
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