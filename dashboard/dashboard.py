from pathlib import Path
from io import BytesIO
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# E-COMMERCE EXECUTIVE ANALYTICS DASHBOARD
# Streamlit + Pandas + Plotly
# ============================================================

st.set_page_config(
    page_title="E-Commerce Executive Analytics",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------
# Theme
# ------------------------------------------------------------
BG = "#07111F"
BG_2 = "#091827"
SIDEBAR = "#06101D"
CARD = "#0D1B2A"
CARD_2 = "#102235"
CARD_3 = "#122A40"
BORDER = "#1B3952"
TEXT = "#F5F8FC"
MUTED = "#8FA7BA"
BLUE = "#5B7FFF"
CYAN = "#22D3EE"
TEAL = "#2DD9B5"
GREEN = "#3EE08A"
AMBER = "#FBBF3D"
ORANGE = "#FF9152"
RED = "#FB6B7A"
PURPLE = "#A78BFA"
INDIGO = "#6C5CE7"
GOLD = "#F4C86A"
ROSE = "#FB7DA8"
GRID = "#1B344A"
WHITE = "#FFFFFF"

PALETTE = [BLUE, CYAN, TEAL, AMBER, PURPLE, ORANGE, RED, GREEN]

# Per-page identity — icon + accent color used across the hero, section heads and nav
PAGE_META = {
    "Overview":  {"icon": "◈", "color": BLUE,   "gradient": (BLUE, CYAN)},
    "Sales":     {"icon": "📈", "color": TEAL,   "gradient": (TEAL, GREEN)},
    "Customers": {"icon": "👥", "color": PURPLE, "gradient": (PURPLE, ROSE)},
    "Products":  {"icon": "📦", "color": AMBER,  "gradient": (AMBER, GOLD)},
    "Refunds":   {"icon": "↩",  "color": RED,    "gradient": (RED, ORANGE)},
    "Payments":  {"icon": "💳", "color": CYAN,   "gradient": (CYAN, BLUE)},
}

# ------------------------------------------------------------
# Global CSS — premium dashboard shell
# ------------------------------------------------------------
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=Manrope:wght@500;700;800&display=swap');
    html, body, [class*="css"] {{ font-family: 'Plus Jakarta Sans', Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    .stApp {{
        background:
            radial-gradient(circle at 88% -8%, rgba(108,92,231,.30) 0%, transparent 42%),
            radial-gradient(circle at 12% 8%, rgba(34,211,238,.10) 0%, transparent 40%),
            radial-gradient(circle at -6% 105%, rgba(244,200,106,.08) 0%, transparent 46%),
            linear-gradient(180deg, {BG} 0%, #050912 55%, #030710 100%);
        color: {TEXT};
    }}
    [data-testid="stHeader"] {{ background: rgba(0,0,0,0); }}
    [data-testid="stToolbar"] {{ right: 1rem; }}
    [data-testid="stSidebar"] {{ background: linear-gradient(180deg, {SIDEBAR} 0%, #071421 100%); border-right: 1px solid {BORDER}; }}
    [data-testid="stSidebar"] * {{ color: {TEXT}; }}
    .block-container {{ max-width: 1500px; padding: 1.2rem 2rem 2.5rem 2rem; }}
    h1, h2, h3, h4 {{ color: {TEXT} !important; font-weight:800; letter-spacing:-.3px; }}
    .hero {{
        position: relative; overflow: hidden; border: 1px solid {BORDER};
        border-radius: 26px; padding: 28px 30px 26px; margin-bottom: 20px;
        background: linear-gradient(135deg, rgba(19,46,71,.97), rgba(7,17,29,.99));
        box-shadow: 0 22px 50px rgba(0,0,0,.30), inset 0 1px 0 rgba(255,255,255,.04);
    }}
    .hero:before {{
        content:""; position:absolute; top:0; left:0; right:0; height:3px;
        background:linear-gradient(90deg, var(--h1,{BLUE}), var(--h2,{CYAN}));
        opacity:.9; z-index:2;
    }}
    .hero:after {{ content:""; position:absolute; width:280px; height:280px; border-radius:50%;
        right:-100px; top:-150px; background: rgba(39,212,232,.06); filter: blur(4px); }}
    .hero-glow {{
        position:absolute; width:320px; height:320px; border-radius:50%;
        right:-90px; bottom:-160px;
        background:linear-gradient(135deg, var(--h1,{BLUE}), var(--h2,{CYAN}));
        opacity:.14; filter:blur(50px); z-index:0;
    }}
    .hero-kicker {{ color:{CYAN}; font-size:10.5px; font-weight:850; letter-spacing:2.2px; text-transform:uppercase; }}
    .hero-title {{
        font-size:36px; line-height:1.08; font-weight:900; margin-top:8px; letter-spacing:-1px;
        background:linear-gradient(90deg, #FFFFFF 45%, var(--h1,{CYAN}) 130%);
        -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; color:transparent;
        display:inline-block;
    }}
    .hero-subtitle {{ color:{MUTED}; font-size:13.5px; margin-top:9px; max-width:850px; line-height:1.55; }}
    .hero-row {{ display:flex; align-items:flex-start; gap:18px; position:relative; z-index:1; }}
    .hero-icon-badge {{
        flex:none; width:58px; height:58px; border-radius:18px; display:flex; align-items:center; justify-content:center;
        font-size:27px; color:#04101C; box-shadow:0 14px 28px rgba(0,0,0,.40), inset 0 1px 0 rgba(255,255,255,.35);
    }}
    .hero-chip-row {{ display:flex; flex-wrap:wrap; gap:9px; margin-top:18px; position:relative; z-index:1; }}
    .hero-chip {{ display:inline-block; padding:7px 12px; border-radius:999px;
        background:rgba(76,141,255,.11); border:1px solid rgba(76,141,255,.25); color:#BFD4FF; font-size:11px; font-weight:600; }}
    .hero-chip-gold {{
        background:linear-gradient(90deg, rgba(244,200,106,.18), rgba(244,200,106,.06));
        border:1px solid rgba(244,200,106,.40); color:{GOLD}; font-weight:800;
    }}
    .section-head {{ display:flex; align-items:center; gap:13px; margin:26px 0 12px; }}
    .section-icon {{
        width:36px; height:36px; border-radius:11px; display:flex; align-items:center; justify-content:center;
        font-size:16px; flex:none; box-shadow:inset 0 1px 0 rgba(255,255,255,.08);
    }}
    .section-title {{ font-size:18px; font-weight:850; letter-spacing:-.2px; }}
    .section-sub {{ color:{MUTED}; font-size:11px; margin-top:2px; }}
    .kpi {{
        position:relative; overflow:hidden;
        background: linear-gradient(145deg, rgba(16,34,53,.98), rgba(10,25,40,.98));
        border:1px solid {BORDER}; border-radius:17px; padding:17px 17px 16px;
        min-height:116px; box-shadow:0 10px 28px rgba(0,0,0,.15);
    }}
    .kpi:before {{
        content:""; position:absolute; top:0; left:0; right:0; height:3px;
        background:var(--k-accent, {CYAN}); opacity:.9;
    }}
    .kpi-top {{ display:flex; align-items:center; justify-content:space-between; }}
    .kpi-label {{ color:{MUTED}; font-size:10px; font-weight:800; text-transform:uppercase; letter-spacing:1px; }}
    .kpi-icon {{
        width:32px; height:32px; border-radius:10px; display:flex; align-items:center; justify-content:center;
        font-size:14px; flex:none; box-shadow:inset 0 1px 0 rgba(255,255,255,.08);
    }}
    .kpi-dot {{ width:8px; height:8px; border-radius:50%; background:{CYAN}; box-shadow:0 0 12px rgba(39,212,232,.55); }}
    .kpi-value {{ color:{TEXT}; font-size:26px; font-weight:900; margin-top:12px; letter-spacing:-.5px; }}
    .kpi-note {{ color:{MUTED}; font-size:10px; margin-top:5px; }}
    .signal {{ background:linear-gradient(135deg, rgba(76,141,255,.10), rgba(39,212,232,.05));
        border:1px solid rgba(76,141,255,.22); border-radius:15px; padding:13px 15px; color:{TEXT}; font-size:12px; }}
    .mini-card {{ background:{CARD}; border:1px solid {BORDER}; border-radius:16px; padding:15px; }}
    .mini-label {{ color:{MUTED}; font-size:10px; text-transform:uppercase; letter-spacing:.8px; font-weight:800; }}
    .mini-value {{ color:{TEXT}; font-size:20px; font-weight:800; margin-top:6px; }}
    .sidebar-brand {{ padding:5px 3px 15px; }}
    .sidebar-logo {{ width:42px; height:42px; border-radius:13px; display:inline-flex; align-items:center; justify-content:center;
        background:linear-gradient(135deg,{INDIGO},{CYAN}); color:#04101C; font-weight:950; font-size:19px;
        box-shadow:0 8px 20px rgba(108,92,231,.45), inset 0 1px 0 rgba(255,255,255,.25); }}
    .sidebar-title {{ font-size:18px; font-weight:850; }}
    .sidebar-sub {{ color:{MUTED}; font-size:11px; margin-top:2px; }}
    .pro-badge {{
        display:inline-flex; align-items:center; gap:5px; margin-top:12px; padding:5px 10px;
        border-radius:999px; background:linear-gradient(90deg, rgba(244,200,106,.16), rgba(244,200,106,.05));
        border:1px solid rgba(244,200,106,.35); color:{GOLD}; font-size:9.5px; font-weight:900;
        letter-spacing:.9px;
    }}
    .filter-title {{ color:{MUTED}; font-size:10px; font-weight:800; letter-spacing:1.1px; text-transform:uppercase; margin:12px 0 8px; }}
    .foot {{ color:{MUTED}; font-size:10px; text-align:center; padding:18px 0 2px; }}
    div[data-testid="stMetric"] {{ background:{CARD}; border:1px solid {BORDER}; border-radius:15px; }}
    div[data-testid="stMetricLabel"] {{ color:{MUTED}; }}
    div[data-testid="stMetricValue"] {{ color:{TEXT}; }}
    .stSelectbox label, .stMultiSelect label, .stDateInput label {{ color:#FFFFFF !important; font-size:11px !important; }}
    .stSelectbox > div > div, .stMultiSelect > div > div, .stDateInput > div > div {{ background:{CARD}; border-color:{BORDER}; }}
    button[data-baseweb="tab"] {{ color:{MUTED}; }}
    button[data-baseweb="tab"][aria-selected="true"] {{ color:{TEXT}; }}
    .stDataFrame {{ border:1px solid {BORDER}; border-radius:14px; overflow:hidden; background:{CARD}; }}

    /* --- Pro polish v4 --- */
    [data-testid="stSidebar"] {{ box-shadow: 8px 0 30px rgba(0,0,0,.16); }}
    [data-testid="stSidebar"] .block-container {{ padding: 1.1rem .9rem 1.5rem .9rem; }}
    [data-testid="stSidebar"] hr {{ border-color:{BORDER}; opacity:.65; }}
    [data-testid="stSidebar"] [data-testid="stRadio"] > div {{ gap:6px; }}
    [data-testid="stSidebar"] [data-testid="stRadio"] input[type="radio"] {{
        display:none;
    }}
    [data-testid="stSidebar"] [data-testid="stRadio"] label {{
        background:rgba(13,27,42,.52); border:1px solid transparent; border-radius:12px;
        padding:9px 12px; margin:0; transition:.18s ease; cursor:pointer;
        position:relative; overflow:hidden;
    }}
    [data-testid="stSidebar"] [data-testid="stRadio"] label p {{
        display:flex; align-items:center; gap:10px;
        font-size:12px !important; font-weight:750 !important; color:{MUTED} !important;
        margin:0;
    }}
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {{
        background:rgba(39,212,232,.07); border-color:rgba(39,212,232,.18);
        transform:translateX(2px);
    }}
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover p {{ color:{TEXT} !important; }}
    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {{
        background:linear-gradient(90deg, rgba(76,141,255,.24), rgba(39,212,232,.09));
        border-color:rgba(76,141,255,.38);
        box-shadow:inset 3px 0 0 {BLUE}, 0 8px 22px rgba(76,141,255,.14);
    }}
    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p {{
        color:{TEXT} !important; font-weight:850 !important;
    }}
    [data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked):after {{
        content:"›"; position:absolute; right:12px; top:50%; transform:translateY(-50%);
        color:{CYAN}; font-weight:900; font-size:16px;
    }}
    [data-testid="stSidebar"] .stSelectbox > div > div,
    [data-testid="stSidebar"] .stDateInput > div > div {{
        border-radius:10px !important; min-height:38px; background:#0A1826 !important;
    }}
    [data-testid="stSidebar"] [data-baseweb="select"] {{ background:#0A1826 !important; }}
    .hero {{ backdrop-filter: blur(12px); }}
    .hero-chip {{ box-shadow:inset 0 1px 0 rgba(255,255,255,.04); }}
    .kpi {{ transition:transform .18s ease, border-color .18s ease, box-shadow .18s ease; }}
    .kpi:hover {{ transform:translateY(-2px); border-color:rgba(76,141,255,.42); box-shadow:0 16px 34px rgba(0,0,0,.22); }}
    .kpi-value {{ text-shadow:0 3px 18px rgba(0,0,0,.20); }}
    .section-title {{ letter-spacing:-.35px; }}
    div[data-testid="stPlotlyChart"] {{
        border:1px solid rgba(27,57,82,.85); border-radius:17px; overflow:hidden;
        box-shadow:0 10px 26px rgba(0,0,0,.10); background:{CARD};
    }}
    div[data-testid="stDataFrame"] {{ box-shadow:0 10px 26px rgba(0,0,0,.10); }}
    .stAlert {{ border-radius:14px; border:1px solid {BORDER}; }}
    button[kind="secondary"], button[kind="primary"] {{ border-radius:10px !important; }}
    ::-webkit-scrollbar {{ width:8px; height:8px; }}
    ::-webkit-scrollbar-track {{ background:#07111F; }}
    ::-webkit-scrollbar-thumb {{ background:#1A3850; border-radius:20px; }}
    ::-webkit-scrollbar-thumb:hover {{ background:#28536F; }}
    .topnav {{ display:flex; align-items:center; justify-content:space-between; gap:14px; margin:0 0 16px; padding:9px 11px; background:rgba(9,24,39,.82); border:1px solid {BORDER}; border-radius:16px; box-shadow:0 10px 28px rgba(0,0,0,.13); backdrop-filter:blur(12px); }}
    .topnav-brand {{ display:flex; align-items:center; gap:9px; min-width:155px; }}
    .topnav-mark {{ width:30px; height:30px; border-radius:9px; display:flex; align-items:center; justify-content:center; background:linear-gradient(135deg,{BLUE},{CYAN}); color:#04101C; font-weight:950; }}
    .topnav-brandtext {{ font-size:11px; font-weight:850; letter-spacing:.4px; color:{TEXT}; }}
    .topnav-brandsub {{ font-size:9px; color:{MUTED}; margin-top:1px; }}

    .navwrap {{
        flex:1;
        display:flex;
        justify-content:center;
    }}
    .navwrap [data-testid="stRadio"] > div {{
        display:flex;
        flex-direction:row;
        gap:4px;
        width:100%;
        justify-content:center;
    }}
    .navwrap [data-testid="stRadio"] label {{
        border:1px solid transparent;
        border-radius:10px;
        padding:7px 12px;
        margin:0;
        background:transparent;
        transition:.18s ease;
        cursor:pointer;
    }}

    /* Navigation text: bright white */
    /* IMPORTANT: Streamlit creates the radio widget outside the HTML div used for navwrap.
       Target the main-page radio directly so the six navigation labels are always white. */
    [data-testid="stMain"] [data-testid="stRadio"] label,
    [data-testid="stMain"] [data-testid="stRadio"] label p,
    [data-testid="stMain"] [data-testid="stRadio"] label span,
    [data-testid="stMain"] [data-testid="stRadio"] label div,
    [data-testid="stMain"] [data-testid="stRadio"] label div *,
    [data-testid="stMain"] [data-testid="stRadio"] label [data-testid="stMarkdownContainer"],
    [data-testid="stMain"] [data-testid="stRadio"] label [data-testid="stMarkdownContainer"] *,
    [data-testid="stMain"] [data-testid="stRadio"] label [class*="stMarkdown"],
    [data-testid="stMain"] [data-testid="stRadio"] label [class*="stMarkdown"] * {{
        color:#FFFFFF !important;
        -webkit-text-fill-color:#FFFFFF !important;
        font-size:12px !important;
        font-weight:800 !important;
    }}

    .navwrap [data-testid="stRadio"] label:hover {{
        background:rgba(76,141,255,.08);
        border-color:rgba(76,141,255,.18);
    }}

    .navwrap [data-testid="stRadio"] label:has(input:checked) {{
        background:linear-gradient(135deg,rgba(76,141,255,.20),rgba(39,212,232,.08));
        border-color:rgba(76,141,255,.32);
        box-shadow:0 5px 18px rgba(0,0,0,.12);
    }}

    .navwrap [data-testid="stRadio"] input {{
        display:none;
    }}

    /* Final white-text override for the actual main-page navigation radio. */
    [data-testid="stMain"] [data-testid="stRadio"] label * {{
        color:#FFFFFF !important;
        -webkit-text-fill-color:#FFFFFF !important;
    }}

    [data-testid="stSidebar"] .stDownloadButton > button {{
        width:100%; border-radius:10px !important; border:1px solid {BORDER} !important;
        background:#0A1826 !important; color:#FFFFFF !important; font-size:11px !important;
        font-weight:800 !important; min-height:36px;
    }}
    [data-testid="stSidebar"] .stDownloadButton > button:hover {{
        border-color:rgba(76,141,255,.45) !important; background:#102A43 !important;
    }}
    .live-pill {{ white-space:nowrap; padding:7px 10px; border-radius:999px; border:1px solid rgba(75,212,122,.22); background:rgba(75,212,122,.06); color:#9BE5B1; font-size:9px; font-weight:850; letter-spacing:.7px; text-transform:uppercase; }}
    .exec-grid {{ display:grid; grid-template-columns:1.35fr 1fr 1fr; gap:12px; margin:15px 0 4px; }}
    .exec-card {{ position:relative; overflow:hidden; min-height:132px; padding:18px 18px 17px; border-radius:17px; border:1px solid {BORDER}; background:linear-gradient(145deg,rgba(16,34,53,.96),rgba(8,21,34,.98)); box-shadow:0 10px 28px rgba(0,0,0,.12); }}
    .exec-card:after {{ content:""; position:absolute; top:0; left:0; right:0; height:3px; background:var(--e-accent,{CYAN}); opacity:.85; }}
    .exec-card:before {{ content:""; position:absolute; width:120px; height:120px; right:-35px; bottom:-55px; border-radius:50%; border:1px solid rgba(39,212,232,.10); box-shadow:0 0 0 16px rgba(39,212,232,.025),0 0 0 32px rgba(39,212,232,.018); }}
    .exec-icon {{ display:inline-flex; align-items:center; justify-content:center; width:20px; height:20px; border-radius:6px; font-size:10px; margin-right:7px; vertical-align:-4px; }}
    .exec-kicker {{ color:{MUTED}; font-size:9px; font-weight:850; letter-spacing:1px; text-transform:uppercase; }}
    .exec-title {{ font-size:17px; font-weight:850; margin-top:7px; letter-spacing:-.25px; }}
    .exec-copy {{ color:{MUTED}; font-size:10px; line-height:1.55; margin-top:6px; max-width:620px; }}
    .exec-stat {{ font-size:24px; font-weight:900; margin-top:9px; }}
    .exec-svg {{ position:absolute; right:14px; top:14px; width:72px; height:72px; opacity:.9; }}
    .ring-track {{ fill:none; stroke:#18344A; stroke-width:7; }}
    .ring-value {{ fill:none; stroke:{CYAN}; stroke-width:7; stroke-linecap:round; stroke-dasharray:188; stroke-dashoffset:48; transform:rotate(-90deg); transform-origin:36px 36px; animation:ringPulse 2.6s ease-in-out infinite alternate; }}
    @keyframes ringPulse {{ from {{ stroke-dashoffset:62; }} to {{ stroke-dashoffset:34; }} }}
    .spark {{ fill:none; stroke:{BLUE}; stroke-width:3; stroke-linecap:round; stroke-linejoin:round; stroke-dasharray:140; animation:sparkMove 3.2s linear infinite; }}
    @keyframes sparkMove {{ 0% {{ stroke-dashoffset:140; opacity:.35; }} 45% {{ opacity:1; }} 100% {{ stroke-dashoffset:0; opacity:.55; }} }}
    .insight-row {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px; margin:12px 0 4px; }}
    .insight-card {{ border:1px solid {BORDER}; background:rgba(13,27,42,.72); border-radius:13px; padding:11px 13px; }}
    .insight-label {{ color:{MUTED}; font-size:9px; text-transform:uppercase; letter-spacing:.8px; font-weight:850; }}
    .insight-value {{ color:{TEXT}; font-size:15px; font-weight:850; margin-top:4px; }}
    .insight-note {{ color:{MUTED}; font-size:9px; margin-top:2px; }}

    /* --- Sidebar insight / plan card --- */
    .side-plan-card {{
        position:relative; margin:16px 1px 8px; padding:16px 15px 15px;
        border-radius:16px; overflow:hidden;
        background:linear-gradient(160deg, rgba(76,141,255,.16), rgba(9,24,39,.94));
        border:1px solid rgba(76,141,255,.28);
        box-shadow:0 14px 30px rgba(0,0,0,.28);
    }}
    .side-plan-card:before {{
        content:""; position:absolute; width:130px; height:130px; border-radius:50%;
        right:-45px; top:-65px; background:rgba(39,212,232,.18); filter:blur(6px);
    }}
    .side-plan-avatars {{ display:flex; margin-bottom:10px; position:relative; z-index:1; }}
    .side-plan-avatars .avatar {{
        width:26px; height:26px; border-radius:50%; border:2px solid #0A1826;
        margin-right:-8px; display:inline-block; box-shadow:0 3px 8px rgba(0,0,0,.35);
    }}
    .avatar.a1 {{ background:linear-gradient(135deg,{BLUE},{CYAN}); }}
    .avatar.a2 {{ background:linear-gradient(135deg,{TEAL},{GREEN}); }}
    .avatar.a3 {{ background:linear-gradient(135deg,{AMBER},{ORANGE}); }}
    .side-plan-title {{ font-size:13.5px; font-weight:850; color:{TEXT}; position:relative; z-index:1; }}
    .side-plan-copy {{ font-size:10.5px; color:{MUTED}; margin-top:6px; line-height:1.55; position:relative; z-index:1; max-width:210px; }}
    .side-plan-pill {{
        display:inline-flex; align-items:center; gap:6px; margin-top:11px; padding:6px 10px;
        border-radius:999px; background:rgba(75,212,122,.10); border:1px solid rgba(75,212,122,.25);
        color:#9BE5B1; font-size:9.5px; font-weight:850; letter-spacing:.4px; text-transform:uppercase;
        position:relative; z-index:1;
    }}

    @media (max-width: 900px) {{
        .topnav {{ flex-wrap:wrap; }}
        .topnav-brand {{ min-width:130px; }}
        .navwrap {{ order:3; flex-basis:100%; }}
        .navwrap [data-testid="stRadio"] > div {{ overflow-x:auto; justify-content:flex-start; }}
        .exec-grid,.insight-row {{ grid-template-columns:1fr; }}
    }}

    footer {{ visibility:hidden; }}
    #MainMenu {{ visibility:hidden; }}
    header {{ background:transparent !important; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def money(v):
    if pd.isna(v):
        return "—"
    v = float(v)
    sign = "-" if v < 0 else ""
    v = abs(v)
    if v >= 1_000_000_000:
        return f"PKR {sign}{v/1_000_000_000:.2f}B"
    if v >= 1_000_000:
        return f"PKR {sign}{v/1_000_000:.2f}M"
    if v >= 1_000:
        return f"PKR {sign}{v/1_000:.1f}K"
    return f"PKR {sign}{v:,.0f}"


def number(v):
    return "—" if pd.isna(v) else f"{float(v):,.0f}"


def percent(v, digits=1):
    return "—" if pd.isna(v) else f"{float(v):.{digits}f}%"


def safe_div(a, b):
    return float(a) / float(b) if b not in (0, None) and pd.notna(b) else 0.0


def clean_title(text):
    return str(text).replace("_", " ").strip().title()


def chart_layout(fig, height=350, title=None):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        title=dict(
            text=title or fig.layout.title.text,
            x=0.02,
            xanchor="left",
            font=dict(size=14, color=TEXT),
        ),
        margin=dict(l=12, r=12, t=50, b=12),
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font=dict(color=TEXT, size=11),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=MUTED, size=10)),
        hoverlabel=dict(bgcolor="#102235", bordercolor=BORDER, font_color=TEXT),
    )
    fig.update_xaxes(gridcolor=GRID, zerolinecolor=GRID, linecolor=BORDER)
    fig.update_yaxes(gridcolor=GRID, zerolinecolor=GRID, linecolor=BORDER)
    return fig


def show_kpi(label, value, note="", accent=CYAN, icon="◆"):
    st.markdown(
        f'<div class="kpi" style="--k-accent:{accent};"><div class="kpi-top"><div class="kpi-label">{label}</div>'
        f'<div class="kpi-icon" style="background:{accent}26; color:{accent}; border:1px solid {accent}55;">{icon}</div></div>'
        f'<div class="kpi-value">{value}</div><div class="kpi-note">{note}</div></div>',
        unsafe_allow_html=True,
    )


def section(title, subtitle="", icon="◆", accent=CYAN):
    st.markdown(
        f'<div class="section-head">'
        f'<div class="section-icon" style="background:{accent}22; color:{accent}; border:1px solid {accent}55;">{icon}</div>'
        f'<div><div class="section-title">{title}</div><div class="section-sub">{subtitle}</div></div></div>',
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------
# Dashboard export helpers
# ------------------------------------------------------------
def build_dashboard_export(df_export, orders_export, filtered_orders, filtered_items, page_name,
                           start_date_export, end_date_export, category_export, payment_export,
                           status_export, customer_type_export, refund_filter_export):
    """Create a complete export of every dashboard section from the current filters.

    Returns:
        full_png_bytes: one long PNG containing Overview + Sales + Customers + Products + Refunds + Payments.
        full_pdf_bytes: a multi-page PDF with one dashboard section per page.
    """
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_pdf import PdfPages
    except ImportError as exc:
        raise RuntimeError(
            "Dashboard export needs matplotlib. Install it with: pip install matplotlib"
        ) from exc

    # ---------- Shared calculations ----------
    monthly = (
        filtered_orders.groupby("Month_Label", as_index=False)
        .agg(Orders=("increment_id", "nunique"), Revenue=("grand_total", "sum"))
        .sort_values("Month_Label")
    )

    customer = filtered_orders.groupby("Customer ID", dropna=True).agg(
        Orders=("increment_id", "nunique"), Revenue=("grand_total", "sum")
    ).reset_index()
    if not customer.empty:
        customer["Customer_Type"] = np.where(customer["Orders"] > 1, "Repeat", "One-time")

    product = filtered_items.copy()
    product["sku"] = product["sku"].fillna("Unknown")

    category_rev = (
        product.groupby("category_name_1", dropna=False)["Product_Revenue"]
        .sum().reset_index().sort_values("Product_Revenue", ascending=False)
    )
    category_rev["category_name_1"] = category_rev["category_name_1"].fillna("Unknown")

    top_sku = (
        product.groupby("sku").agg(Revenue=("Product_Revenue", "sum"), Quantity=("qty_ordered", "sum"))
        .reset_index().nlargest(10, "Revenue").sort_values("Revenue", ascending=True)
    )

    refund = filtered_orders[filtered_orders["Is_Refund"]].copy()
    nonrefund = filtered_orders[~filtered_orders["Is_Refund"]].copy()
    refund_monthly = (
        filtered_orders.groupby("Month_Label")
        .agg(Orders=("increment_id", "nunique"), Refunds=("Is_Refund", "sum"))
        .reset_index().sort_values("Month_Label")
    )
    if not refund_monthly.empty:
        refund_monthly["Refund Rate"] = refund_monthly.apply(
            lambda r: safe_div(r["Refunds"], r["Orders"]) * 100, axis=1
        )

    refund_ids = set(refund["increment_id"])
    if len(product):
        rc = product.assign(Is_Refund=product["increment_id"].isin(refund_ids)).groupby(
            "category_name_1", dropna=False
        ).agg(Orders=("increment_id", "nunique"), Refund_Orders=("Is_Refund", "sum")).reset_index()
        rc["category_name_1"] = rc["category_name_1"].fillna("Unknown")
        rc["Refund Rate"] = rc.apply(lambda r: safe_div(r["Refund_Orders"], r["Orders"]) * 100, axis=1)
        rc = rc.sort_values("Refund Rate", ascending=True).tail(10)
    else:
        rc = pd.DataFrame(columns=["category_name_1", "Orders", "Refund_Orders", "Refund Rate"])

    payments = filtered_orders.groupby("payment_method").agg(
        Orders=("increment_id", "nunique"), Revenue=("grand_total", "sum")
    ).reset_index()
    if not payments.empty:
        payments["AOV"] = payments["Revenue"] / payments["Orders"].replace(0, np.nan)
        payments = payments.sort_values("Revenue", ascending=False)

    revenue_export = filtered_orders["grand_total"].sum()
    order_count_export = len(filtered_orders)
    customer_count_export = filtered_orders["Customer ID"].nunique()
    quantity_export = filtered_items["qty_ordered"].sum()
    aov_export = safe_div(revenue_export, order_count_export)
    refund_orders_export = int(filtered_orders["Is_Refund"].sum())
    refund_rate_export = safe_div(refund_orders_export, order_count_export) * 100

    kpis = [
        ("Order Value", money(revenue_export), "#4C8DFF"),
        ("Orders", number(order_count_export), "#27D4E8"),
        ("Customers", number(customer_count_export), "#19C7A0"),
        ("AOV", money(aov_export), "#F5B84B"),
        ("Units Sold", number(quantity_export), "#9B82FF"),
        ("Refund Rate", percent(refund_rate_export), "#F15B6A"),
    ]

    filters_text = (
        f"Date: {start_date_export:%d %b %Y} → {end_date_export:%d %b %Y}   |   "
        f"Category: {category_export if category_export != 'All' else 'All'}   |   "
        f"Payment: {payment_export if payment_export != 'All' else 'All'}   |   "
        f"Status: {status_export if status_export != 'All' else 'All'}   |   "
        f"Customer: {customer_type_export}   |   Refund: {refund_filter_export}"
    )

    COLORS = {
        "bg": "#07111F", "card": "#0D1B2A", "border": "#1B3952",
        "text": "#F5F8FC", "muted": "#8FA7BA", "blue": "#4C8DFF",
        "cyan": "#27D4E8", "teal": "#19C7A0", "amber": "#F5B84B",
        "purple": "#9B82FF", "red": "#F15B6A", "orange": "#FF9F43",
        "green": "#38D39F", "grid": "#1B344A"
    }

    section_titles = {
        "Overview": "Performance Overview",
        "Sales": "Sales Performance",
        "Customers": "Customer Behavior",
        "Products": "Products & SKUs",
        "Refunds": "Refund & Returns Risk",
        "Payments": "Payment Channel Performance",
    }

    # ---------- Figure helpers ----------
    def base_fig(title, subtitle="", height=5.8):
        fig = plt.figure(figsize=(16, height), facecolor=COLORS["bg"])
        fig.text(0.035, 0.965, "E-COMMERCE · EXECUTIVE ANALYTICS", color=COLORS["cyan"],
                 fontsize=9, fontweight="bold", va="top")
        fig.text(0.035, 0.925, title, color=COLORS["text"], fontsize=23,
                 fontweight="bold", va="top")
        if subtitle:
            fig.text(0.035, 0.885, subtitle, color=COLORS["muted"], fontsize=9, va="top")
        fig.text(0.035, 0.842, filters_text, color="#BFD4FF", fontsize=7.5, va="top")
        return fig

    def style_ax(ax, title):
        ax.set_facecolor(COLORS["card"])
        for spine in ax.spines.values():
            spine.set_color(COLORS["border"])
        ax.set_title(title, loc="left", color=COLORS["text"], fontsize=11,
                     fontweight="bold", pad=10)
        ax.tick_params(colors=COLORS["muted"], labelsize=7)
        ax.grid(color=COLORS["grid"], alpha=.65, linewidth=.55)
        ax.set_axisbelow(True)

    def draw_kpi_strip(fig, y=0.68):
        for i, (label, value, accent) in enumerate(kpis):
            x = 0.035 + i * 0.158
            ax = fig.add_axes([x, y, 0.145, 0.105])
            ax.set_facecolor(COLORS["card"])
            for spine in ax.spines.values():
                spine.set_color(COLORS["border"])
            ax.set_xticks([]); ax.set_yticks([])
            ax.text(.06, .72, label.upper(), transform=ax.transAxes,
                    color=COLORS["muted"], fontsize=7, fontweight="bold", va="center")
            ax.text(.06, .34, value, transform=ax.transAxes,
                    color=COLORS["text"], fontsize=12, fontweight="bold", va="center")
            ax.plot([.06, .22], [.92, .92], transform=ax.transAxes,
                    color=accent, linewidth=3, solid_capstyle="round")

    def finish_fig(fig):
        fig.text(0.035, 0.018,
                 f"Filtered rows: {len(filtered_items):,}  •  Filtered orders: {len(filtered_orders):,}  •  "
                 f"Full dataset: {len(df_export):,} rows / {len(orders_export):,} orders",
                 color="#6F8799", fontsize=7)
        fig.subplots_adjust(left=.055, right=.97, top=.80, bottom=.09, hspace=.45, wspace=.25)
        return fig

    def page_overview():
        fig = base_fig(section_titles["Overview"], "All major commercial signals in the selected period.")
        draw_kpi_strip(fig, .68)
        ax1 = fig.add_axes([.055, .40, .57, .23]); style_ax(ax1, "Monthly Order Value")
        if not monthly.empty:
            ax1.plot(monthly["Month_Label"].astype(str), monthly["Revenue"], color=COLORS["blue"], linewidth=2.5, marker="o", markersize=3.5)
            ax1.fill_between(range(len(monthly)), monthly["Revenue"], 0, color=COLORS["blue"], alpha=.10)
            ax1.tick_params(axis="x", rotation=45)
        else:
            ax1.text(.5,.5,"No monthly data",transform=ax1.transAxes,ha="center",color=COLORS["muted"])
        ax2 = fig.add_axes([.67, .40, .275, .23]); style_ax(ax2, "Top Categories by Product Revenue")
        c = category_rev.head(8).sort_values("Product_Revenue")
        if not c.empty:
            ax2.barh(c["category_name_1"].astype(str), c["Product_Revenue"], color=COLORS["cyan"])
            ax2.tick_params(axis="y", labelsize=6)
        else:
            ax2.text(.5,.5,"No category data",transform=ax2.transAxes,ha="center",color=COLORS["muted"])
        ax3 = fig.add_axes([.055, .11, .28, .20]); style_ax(ax3, "Customer Type")
        if not customer.empty:
            vc=customer["Customer_Type"].value_counts(); ax3.pie(vc.values, labels=vc.index, autopct="%1.0f%%", textprops={"color":COLORS["text"],"fontsize":8})
        ax4 = fig.add_axes([.37, .11, .28, .20]); style_ax(ax4, "Payment Revenue")
        p=payments.head(8).sort_values("Revenue")
        if not p.empty: ax4.barh(p["payment_method"].astype(str),p["Revenue"],color=COLORS["teal"])
        ax5 = fig.add_axes([.685, .11, .26, .20]); style_ax(ax5, "Refund vs Non-Refund")
        vals=[len(refund),len(nonrefund)]
        ax5.pie(vals,labels=["Refund","Non-refund"],autopct="%1.0f%%",textprops={"color":COLORS["text"],"fontsize":8})
        return finish_fig(fig)

    def page_sales():
        fig=base_fig(section_titles["Sales"],"Revenue movement, order volume and order-value distribution.")
        draw_kpi_strip(fig,.68)
        ax1=fig.add_axes([.055,.40,.43,.23]); style_ax(ax1,"Monthly Revenue Trend")
        if not monthly.empty:
            ax1.plot(monthly["Month_Label"].astype(str),monthly["Revenue"],color=COLORS["blue"],marker="o",linewidth=2.5); ax1.tick_params(axis="x",rotation=45)
        ax2=fig.add_axes([.535,.40,.41,.23]); style_ax(ax2,"Monthly Order Volume")
        if not monthly.empty: ax2.bar(monthly["Month_Label"].astype(str),monthly["Orders"],color=COLORS["purple"]); ax2.tick_params(axis="x",rotation=45)
        ax3=fig.add_axes([.055,.11,.43,.23]); style_ax(ax3,"Order Value Distribution")
        vals=filtered_orders["grand_total"].dropna()
        if len(vals): ax3.hist(vals,bins=50,color=COLORS["cyan"],alpha=.85)
        ax4=fig.add_axes([.535,.11,.41,.23]); style_ax(ax4,"Product Revenue by Category")
        c=category_rev.head(10).sort_values("Product_Revenue")
        if not c.empty: ax4.barh(c["category_name_1"].astype(str),c["Product_Revenue"],color=COLORS["teal"]); ax4.tick_params(axis="y",labelsize=6)
        return finish_fig(fig)

    def page_customers():
        fig=base_fig(section_titles["Customers"],"Customer frequency, revenue contribution and concentration.")
        draw_kpi_strip(fig,.68)
        ax1=fig.add_axes([.055,.40,.28,.23]); style_ax(ax1,"Customer Type Mix")
        if not customer.empty:
            vc=customer["Customer_Type"].value_counts(); ax1.pie(vc.values,labels=vc.index,autopct="%1.0f%%",textprops={"color":COLORS["text"],"fontsize":8})
        ax2=fig.add_axes([.37,.40,.28,.23]); style_ax(ax2,"Orders vs Customer Revenue")
        if len(customer):
            sm=customer.sample(min(12000,len(customer)),random_state=42); ax2.scatter(sm["Orders"],sm["Revenue"],s=8,alpha=.35,color=COLORS["orange"]); ax2.set_xscale("symlog"); ax2.set_yscale("symlog")
        ax3=fig.add_axes([.685,.40,.26,.23]); style_ax(ax3,"Purchase Frequency")
        if len(customer):
            bins=[-1,1,2,5,10,np.inf]; labels=["1","2","3–5","6–10","11+"]; f=pd.cut(customer["Orders"],bins=bins,labels=labels); vc=f.value_counts().reindex(labels,fill_value=0); ax3.bar(labels,vc.values,color=COLORS["teal"])
        ax4=fig.add_axes([.055,.11,.43,.23]); style_ax(ax4,"Top Customers by Revenue")
        top=customer.nlargest(10,"Revenue").sort_values("Revenue");
        if not top.empty: ax4.barh(top["Customer ID"].astype(str),top["Revenue"],color=COLORS["blue"]); ax4.tick_params(axis="y",labelsize=6)
        ax5=fig.add_axes([.535,.11,.41,.23]); style_ax(ax5,"Customer Revenue Distribution")
        if len(customer): ax5.hist(customer["Revenue"].dropna(),bins=50,color=COLORS["purple"],alpha=.85)
        return finish_fig(fig)

    def page_products():
        fig=base_fig(section_titles["Products"],"SKU performance, category contribution, pricing and demand.")
        draw_kpi_strip(fig,.68)
        ax1=fig.add_axes([.055,.40,.43,.23]); style_ax(ax1,"Top 10 SKUs by Product Revenue")
        if not top_sku.empty: ax1.barh(top_sku["sku"].astype(str),top_sku["Revenue"],color=COLORS["blue"]); ax1.tick_params(axis="y",labelsize=6)
        ax2=fig.add_axes([.535,.40,.41,.23]); style_ax(ax2,"Category Product Revenue")
        c=category_rev.head(10).sort_values("Product_Revenue")
        if not c.empty: ax2.barh(c["category_name_1"].astype(str),c["Product_Revenue"],color=COLORS["amber"]); ax2.tick_params(axis="y",labelsize=6)
        ax3=fig.add_axes([.055,.11,.43,.23]); style_ax(ax3,"Quantity vs Price")
        if len(product):
            sm=product.sample(min(12000,len(product)),random_state=42); ax3.scatter(sm["qty_ordered"],sm["price"],s=7,alpha=.35,color=COLORS["cyan"])
        ax4=fig.add_axes([.535,.11,.41,.23]); style_ax(ax4,"Product Price Distribution")
        if len(product): ax4.hist(product["price"].dropna(),bins=55,color=COLORS["purple"],alpha=.85)
        return finish_fig(fig)

    def page_refunds():
        fig=base_fig(section_titles["Refunds"],"Refund exposure, monthly return pressure and category-level risk.")
        draw_kpi_strip(fig,.68)
        ax1=fig.add_axes([.055,.40,.43,.23]); style_ax(ax1,"Monthly Refund Rate")
        if not refund_monthly.empty: ax1.plot(refund_monthly["Month_Label"].astype(str),refund_monthly["Refund Rate"],color=COLORS["red"],marker="o",linewidth=2.5); ax1.tick_params(axis="x",rotation=45)
        ax2=fig.add_axes([.535,.40,.41,.23]); style_ax(ax2,"Refund vs Non-Refund Orders")
        ax2.pie([len(refund),len(nonrefund)],labels=["Refund","Non-refund"],autopct="%1.0f%%",textprops={"color":COLORS["text"],"fontsize":8})
        ax3=fig.add_axes([.055,.11,.43,.23]); style_ax(ax3,"Category Refund Rate")
        if not rc.empty: ax3.barh(rc["category_name_1"].astype(str),rc["Refund Rate"],color=COLORS["red"]); ax3.tick_params(axis="y",labelsize=6)
        ax4=fig.add_axes([.535,.11,.41,.23]); style_ax(ax4,"Refund Value by Category")
        if len(product):
            rv=product.assign(Is_Refund=product["increment_id"].isin(refund_ids)).groupby("category_name_1",dropna=False).apply(lambda x: x.loc[x["Is_Refund"],"Product_Revenue"].sum(),include_groups=False).sort_values().tail(10); rv.index=rv.index.fillna("Unknown"); ax4.barh(rv.index.astype(str),rv.values,color=COLORS["orange"]); ax4.tick_params(axis="y",labelsize=6)
        return finish_fig(fig)

    def page_payments():
        fig=base_fig(section_titles["Payments"],"Order volume, revenue contribution and average order value by payment method.")
        draw_kpi_strip(fig,.68)
        ax1=fig.add_axes([.055,.40,.43,.23]); style_ax(ax1,"Payment Methods by Order Count")
        p=payments.head(10).sort_values("Orders")
        if not p.empty: ax1.barh(p["payment_method"].astype(str),p["Orders"],color=COLORS["blue"]); ax1.tick_params(axis="y",labelsize=6)
        ax2=fig.add_axes([.535,.40,.41,.23]); style_ax(ax2,"Payment Methods by Revenue")
        p=payments.head(10).sort_values("Revenue")
        if not p.empty: ax2.barh(p["payment_method"].astype(str),p["Revenue"],color=COLORS["teal"]); ax2.tick_params(axis="y",labelsize=6)
        ax3=fig.add_axes([.055,.11,.43,.23]); style_ax(ax3,"Payment Volume vs AOV")
        if not payments.empty:
            ax3.scatter(payments["Orders"],payments["AOV"],s=np.maximum(payments["Revenue"].fillna(0)/payments["Revenue"].max()*700,25),color=COLORS["amber"],alpha=.8)
            for _,r in payments.iterrows(): ax3.annotate(str(r["payment_method"]),(r["Orders"],r["AOV"]),fontsize=5,color=COLORS["muted"])
        ax4=fig.add_axes([.535,.11,.41,.23]); style_ax(ax4,"Payment Revenue Share")
        if not payments.empty:
            pp=payments.head(8); ax4.pie(pp["Revenue"],labels=pp["payment_method"],autopct="%1.0f%%",textprops={"color":COLORS["text"],"fontsize":6})
        return finish_fig(fig)

    pages = [page_overview(), page_sales(), page_customers(), page_products(), page_refunds(), page_payments()]

    # ---------- Multi-page PDF ----------
    pdf_buffer = BytesIO()
    with PdfPages(pdf_buffer) as pdf:
        for fig in pages:
            pdf.savefig(fig, facecolor=fig.get_facecolor(), bbox_inches="tight")
    pdf_buffer.seek(0)

    # ---------- One long PNG containing the entire dashboard ----------
    # Rebuild as a tall canvas and copy each page into it using image buffers.
    rendered = []
    for fig in pages:
        b = BytesIO()
        fig.savefig(b, format="png", dpi=240, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.08)
        b.seek(0)
        rendered.append(plt.imread(b))
        plt.close(fig)

    widths = [img.shape[1] for img in rendered]
    target_w = max(widths)
    padded = []
    for img in rendered:
        if img.shape[1] < target_w:
            pad = np.zeros((img.shape[0], target_w-img.shape[1], img.shape[2]), dtype=img.dtype)
            if img.shape[2] == 4:
                pad[..., 3] = 1
            img = np.concatenate([img, pad], axis=1)
        padded.append(img)
    long_img = np.concatenate(padded, axis=0)

    png_buffer = BytesIO()
    plt.imsave(png_buffer, long_img, format="png")
    png_buffer.seek(0)

    return png_buffer.getvalue(), pdf_buffer.getvalue()

# ------------------------------------------------------------
# Data loading
# ------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "DATA" / "processed" / "ecommerce_cleaned.csv"
if not DATA_PATH.exists():
    fallback = Path(r"C:\Users\123\OneDrive\Desktop\project\DATA\processed\ecommerce_cleaned.csv")
    if fallback.exists():
        DATA_PATH = fallback


@st.cache_data(show_spinner="Loading cleaned e-commerce data...")
def load_data(path_str):
    path = Path(path_str)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    df = pd.read_csv(path, low_memory=False)
    df.columns = [str(c).strip() for c in df.columns]
    for col in [
        "status", "sku", "category_name_1", "sales_commission_code",
        "payment_method", "BI Status", "increment_id"
    ]:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()

    for col in ["price", "qty_ordered", "grand_total", "discount_amount", "MV"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    df["Product_Revenue"] = df["price"].fillna(0) * df["qty_ordered"].fillna(0)
    df["Month_Label"] = df["created_at"].dt.to_period("M").astype("string")

    orders = (
        df.sort_values(["increment_id", "created_at"])
        .drop_duplicates("increment_id")
        .copy()
    )

    refund_statuses = {"order_refunded", "refund"}
    refund_by_order = (
        df.assign(_refund=df["status"].fillna("").str.lower().isin(refund_statuses))
        .groupby("increment_id")["_refund"]
        .any()
    )
    orders["Is_Refund"] = orders["increment_id"].map(refund_by_order).fillna(False)

    customer_counts = orders.groupby("Customer ID", dropna=True)["increment_id"].nunique()
    orders["Customer_Order_Count"] = orders["Customer ID"].map(customer_counts)
    orders["Customer_Type"] = np.where(
        orders["Customer_Order_Count"].fillna(0) > 1, "Repeat", "One-time"
    )
    orders["Month_Label"] = orders["created_at"].dt.to_period("M").astype("string")

    return df, orders


try:
    df, orders = load_data(str(DATA_PATH))
except Exception as exc:
    st.error("Dashboard could not load the cleaned dataset.")
    st.code(str(exc))
    st.info("Expected: project/DATA/processed/ecommerce_cleaned.csv")
    st.stop()

required = {
    "increment_id", "created_at", "grand_total", "status",
    "payment_method", "Customer ID", "category_name_1"
}
missing = sorted(required - set(df.columns))
if missing:
    st.error(f"Required columns are missing: {missing}")
    st.stop()

# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------
with st.sidebar:
    st.markdown(
        '<div class="sidebar-brand"><div style="display:flex;align-items:center;gap:10px;">'
        '<div class="sidebar-logo">E</div>'
        '<div><div class="sidebar-title">E-Commerce</div>'
        '<div class="sidebar-sub">Executive Analytics Suite</div></div></div>'
        '<div class="pro-badge">◆ PRO INSIGHTS</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div style="display:flex;align-items:center;gap:7px;margin:0 0 14px 2px;color:#8FA7BA;font-size:10px;">'
        '<span style="width:7px;height:7px;border-radius:50%;background:#4BD47A;box-shadow:0 0 10px #4BD47A88;"></span>'
        '<span style="letter-spacing:.8px;font-weight:800;text-transform:uppercase;">Data connected</span></div>',
        unsafe_allow_html=True,
    )
    # Navigation
    st.markdown('<div class="filter-title">Navigation</div>', unsafe_allow_html=True)
    page = st.radio(
        "NAVIGATION",
        list(PAGE_META.keys()),
        format_func=lambda name: f"{PAGE_META[name]['icon']}  {name}",
        label_visibility="collapsed",
    )

    st.markdown(
        """
        <div class="side-plan-card">
            <div class="side-plan-avatars">
                <span class="avatar a1"></span>
                <span class="avatar a2"></span>
                <span class="avatar a3"></span>
            </div>
            <div class="side-plan-title">Live Dashboard</div>
            <div class="side-plan-copy">Every chart updates instantly as you change filters — explore freely, nothing is cached against you.</div>
            <div class="side-plan-pill">● Real-time filters</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    export_slot = st.empty()

    st.divider()
    st.caption(f"Raw rows: {len(df):,}  •  Unique orders: {len(orders):,}")

# ------------------------------------------------------------
# Hero placeholder — reserved at the top so the page title always
# leads, even though its content depends on the filters below it.
# ------------------------------------------------------------
hero_slot = st.empty()

# ------------------------------------------------------------
# Dashboard Filters
# ------------------------------------------------------------
st.markdown(
    '<div style="display:flex;align-items:center;gap:8px;margin:2px 0 10px;">'
    '<span style="width:26px;height:26px;border-radius:8px;display:flex;align-items:center;justify-content:center;'
    'background:rgba(76,141,255,.14);border:1px solid rgba(76,141,255,.30);font-size:12px;">🎛</span>'
    '<span style="font-size:11px;font-weight:850;letter-spacing:1px;text-transform:uppercase;color:#8FA7BA;">Filters</span>'
    '</div>',
    unsafe_allow_html=True,
)

min_date = df["created_at"].min().date()
max_date = df["created_at"].max().date()
categories = sorted(df["category_name_1"].dropna().unique().tolist())
payments = sorted(orders["payment_method"].dropna().unique().tolist())
statuses = sorted(orders["status"].dropna().unique().tolist())

f1, f2, f3, f4, f5, f6 = st.columns([1.55, 1.1, 1.1, 1.1, 1.1, 1.1])

with f1:
    date_value = st.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
if isinstance(date_value, tuple) and len(date_value) == 2:
    start_date, end_date = date_value
else:
    start_date, end_date = min_date, max_date

with f2:
    category = st.selectbox("Category", ["All"] + categories)
with f3:
    payment = st.selectbox("Payment method", ["All"] + payments)
with f4:
    status = st.selectbox("Order status", ["All"] + statuses)
with f5:
    customer_type = st.selectbox("Customer type", ["All", "Repeat", "One-time"])
with f6:
    refund_filter = st.selectbox("Refund status", ["All", "Refund Orders", "Non-Refund Orders"])

st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# Filtering
# ------------------------------------------------------------
def filter_orders(base_orders):
    x = base_orders[base_orders["created_at"].dt.date.between(start_date, end_date)].copy()

    if payment != "All":
        x = x[x["payment_method"] == payment]
    if status != "All":
        x = x[x["status"] == status]
    if customer_type != "All":
        x = x[x["Customer_Type"] == customer_type]
    if refund_filter == "Refund Orders":
        x = x[x["Is_Refund"]]
    elif refund_filter == "Non-Refund Orders":
        x = x[~x["Is_Refund"]]
    if category != "All":
        category_order_ids = set(
            df.loc[
                df["category_name_1"].eq(category)
                & df["created_at"].dt.date.between(start_date, end_date),
                "increment_id",
            ].dropna()
        )
        x = x[x["increment_id"].isin(category_order_ids)]
    return x


def filter_items(base_df, filtered_orders):
    ids = set(filtered_orders["increment_id"].dropna())
    x = base_df[base_df["increment_id"].isin(ids)].copy()
    if category != "All":
        x = x[x["category_name_1"] == category]
    return x


fo = filter_orders(orders)
fi = filter_items(df, fo)

# ------------------------------------------------------------
# Export current dashboard selection
# ------------------------------------------------------------
try:
    export_png, export_pdf = build_dashboard_export(
        df, orders, fo, fi, page, start_date, end_date, category, payment,
        status, customer_type, refund_filter
    )
    with export_slot.container():
        st.markdown('<div class="filter-title" style="margin-top:12px;">Export Dashboard</div>', unsafe_allow_html=True)
        st.download_button(
            "Download PNG",
            data=export_png,
            file_name=f"ecommerce_dashboard_full_dashboard.png",
            mime="image/png",
            use_container_width=True,
            key="download_dashboard_png",
        )
        st.download_button(
            "Download PDF",
            data=export_pdf,
            file_name=f"ecommerce_dashboard_full_dashboard.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="download_dashboard_pdf",
        )
except Exception as export_exc:
    with export_slot.container():
        st.markdown('<div class="filter-title" style="margin-top:12px;">Export Dashboard</div>', unsafe_allow_html=True)
        st.warning(str(export_exc))

# ------------------------------------------------------------
# Header / hero — filled into the placeholder reserved at the top
# ------------------------------------------------------------
page_subtitles = {
    "Overview": "A compact executive view of sales, customers, products, refunds and payments.",
    "Sales": "Track revenue movement, order volume and order-value distribution.",
    "Customers": "Understand customer frequency, repeat behavior and revenue concentration.",
    "Products": "Explore SKU performance, category contribution, pricing and product demand.",
    "Refunds": "Monitor refund exposure, monthly refund movement and category-level return pressure.",
    "Payments": "Compare payment channels by order volume, revenue and average order value.",
}

_meta = PAGE_META[page]
_g1, _g2 = _meta["gradient"]
with hero_slot.container():
    st.markdown(
        f'<div class="hero" style="--h1:{_g1};--h2:{_g2};">'
        f'<div class="hero-glow"></div>'
        f'<div class="hero-row">'
        f'<div class="hero-icon-badge" style="background:linear-gradient(135deg,{_g1},{_g2});">{_meta["icon"]}</div>'
        f'<div><div class="hero-kicker">E-COMMERCE · EXECUTIVE ANALYTICS</div>'
        f'<div class="hero-title">{page}</div><div class="hero-subtitle">{page_subtitles[page]}</div></div></div>'
        f'<div class="hero-chip-row">'
        f'<div class="hero-chip">{start_date:%d %b %Y} → {end_date:%d %b %Y} &nbsp; • &nbsp; {len(fo):,} filtered orders</div>'
        f'<div class="hero-chip hero-chip-gold">◆ Premium Analytics</div>'
        f'</div></div>',
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------
# Global KPIs
# ------------------------------------------------------------
revenue = fo["grand_total"].sum()
order_count = len(fo)
customer_count = fo["Customer ID"].nunique()
quantity = fi["qty_ordered"].sum()
aov = safe_div(revenue, order_count)
refund_orders = int(fo["Is_Refund"].sum())
refund_rate = safe_div(refund_orders, order_count) * 100

k1, k2, k3, k4, k5, k6 = st.columns(6)
with k1:
    show_kpi("Order Value", money(revenue), "Unique order-level revenue", BLUE, icon="💰")
with k2:
    show_kpi("Orders", number(order_count), "Unique orders", CYAN, icon="🧾")
with k3:
    show_kpi("Customers", number(customer_count), "Unique customers", TEAL, icon="👥")
with k4:
    show_kpi("AOV", money(aov), "Average order value", AMBER, icon="⚖")
with k5:
    show_kpi("Units Sold", number(quantity), "Filtered product quantity", PURPLE, icon="📦")
with k6:
    show_kpi("Refund Rate", percent(refund_rate), f"{refund_orders:,} refund orders", RED, icon="↩")

# Compact context strip keeps the dashboard feeling like an executive product rather than a notebook.
st.markdown(
    f'<div style="display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 2px;">'
    f'<span style="padding:6px 10px;border-radius:999px;background:rgba(76,141,255,.08);border:1px solid rgba(76,141,255,.18);color:#BFD4FF;font-size:10px;font-weight:700;">📦 {category if category != "All" else "All categories"}</span>'
    f'<span style="padding:6px 10px;border-radius:999px;background:rgba(39,212,232,.07);border:1px solid rgba(39,212,232,.17);color:#A8EEF4;font-size:10px;font-weight:700;">💳 {payment if payment != "All" else "All payments"}</span>'
    f'<span style="padding:6px 10px;border-radius:999px;background:rgba(25,199,160,.07);border:1px solid rgba(25,199,160,.17);color:#9FE8D5;font-size:10px;font-weight:700;">👥 {customer_type if customer_type != "All" else "All customers"}</span>'
    f'<span style="padding:6px 10px;border-radius:999px;background:rgba(245,184,75,.07);border:1px solid rgba(245,184,75,.17);color:#F6D69A;font-size:10px;font-weight:700;">↩ {refund_filter}</span>'
    '</div>',
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# Executive summary cards
# ------------------------------------------------------------
repeat_revenue = fo.loc[fo["Customer_Type"] == "Repeat", "grand_total"].sum()
repeat_share = safe_div(repeat_revenue, revenue) * 100
refund_value = fo.loc[fo["Is_Refund"], "grand_total"].sum()
refund_value_share = safe_div(refund_value, revenue) * 100
exec_html = f"""
<div class="exec-grid">
  <div class="exec-card" style="--e-accent:{GOLD};">
    <div class="exec-kicker"><span class="exec-icon" style="background:{GOLD}22;color:{GOLD};border:1px solid {GOLD}55;">◆</span>Executive summary</div>
    <div class="exec-title">Commercial performance at a glance</div>
    <div class="exec-copy">This workspace keeps the analysis unchanged while presenting the selected period as a decision-ready analytics view: sales movement, customer contribution and refund exposure.</div>
    <svg class="exec-svg" viewBox="0 0 72 72" aria-hidden="true"><circle class="ring-track" cx="36" cy="36" r="30"/><circle class="ring-value" cx="36" cy="36" r="30" style="stroke:{GOLD}"/></svg>
  </div>
  <div class="exec-card" style="--e-accent:{PURPLE};">
    <div class="exec-kicker"><span class="exec-icon" style="background:{PURPLE}22;color:{PURPLE};border:1px solid {PURPLE}55;">👥</span>Repeat customer value</div>
    <div class="exec-stat" style="color:{PURPLE};">{repeat_share:.1f}%</div>
    <div class="exec-copy">Share of selected order value generated by repeat customers.</div>
    <svg class="exec-svg" viewBox="0 0 72 72" aria-hidden="true"><path class="spark" style="stroke:{PURPLE}" d="M5 53 L17 45 L28 48 L40 30 L51 35 L67 17"/></svg>
  </div>
  <div class="exec-card" style="--e-accent:{RED};">
    <div class="exec-kicker"><span class="exec-icon" style="background:{RED}22;color:{RED};border:1px solid {RED}55;">↩</span>Refund exposure</div>
    <div class="exec-stat" style="color:{RED};">{refund_value_share:.1f}%</div>
    <div class="exec-copy">Share of selected order value associated with refund orders.</div>
    <svg class="exec-svg" viewBox="0 0 72 72" aria-hidden="true"><path class="spark" style="stroke:{RED}" d="M5 22 L18 28 L29 25 L42 39 L54 34 L67 52"/></svg>
  </div>
</div>
"""
st.markdown(exec_html, unsafe_allow_html=True)

# ------------------------------------------------------------
# Pages
# ------------------------------------------------------------
if page == "Overview":
    section("Performance snapshot", "The main commercial signals in the selected period.", icon="◈", accent=BLUE)
    left, right = st.columns([1.55, 1])

    monthly = (
        fo.groupby("Month_Label", as_index=False)
        .agg(Orders=("increment_id", "nunique"), Revenue=("grand_total", "sum"))
        .sort_values("Month_Label")
    )
    with left:
        if not monthly.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=monthly["Month_Label"], y=monthly["Revenue"], mode="lines+markers",
                line=dict(color=BLUE, width=3), marker=dict(color=CYAN, size=7),
                fill="tozeroy", fillcolor="rgba(76,141,255,.10)", name="Revenue"
            ))
            chart_layout(fig, 365, "Monthly Order Value")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No sales data for the selected filters.")

    with right:
        cat = (
            fi.groupby("category_name_1", dropna=False)["Product_Revenue"]
            .sum().reset_index().sort_values("Product_Revenue", ascending=False).head(8)
        )
        cat["category_name_1"] = cat["category_name_1"].fillna("Unknown")
        if not cat.empty:
            fig = px.bar(cat, x="Product_Revenue", y="category_name_1", orientation="h")
            fig.update_traces(marker_color=CYAN, marker_line_width=0)
            chart_layout(fig, 365, "Top Categories by Product Revenue")
            st.plotly_chart(fig, use_container_width=True)

    section("Business mix", "How orders and value are distributed across the selected filters.", icon="◇", accent=PURPLE)
    a, b, c = st.columns(3)
    with a:
        mix = fo["Customer_Type"].value_counts().reset_index()
        mix.columns = ["Customer Type", "Orders"]
        fig = px.pie(mix, names="Customer Type", values="Orders", hole=.62)
        fig.update_traces(marker_colors=[BLUE, CYAN], textinfo="percent")
        chart_layout(fig, 310, "Repeat vs One-time Orders")
        st.plotly_chart(fig, use_container_width=True)
    with b:
        pm = fo.groupby("payment_method")["grand_total"].sum().reset_index().sort_values("grand_total", ascending=False).head(7)
        fig = px.bar(pm, x="payment_method", y="grand_total")
        fig.update_traces(marker_color=TEAL)
        chart_layout(fig, 310, "Payment Channels by Value")
        st.plotly_chart(fig, use_container_width=True)
    with c:
        refund_mix = pd.DataFrame({"Type": ["Refund", "Non-refund"], "Orders": [refund_orders, order_count-refund_orders]})
        fig = px.pie(refund_mix, names="Type", values="Orders", hole=.62)
        fig.update_traces(marker_colors=[RED, GREEN], textinfo="percent")
        chart_layout(fig, 310, "Refund Exposure")
        st.plotly_chart(fig, use_container_width=True)

    repeat_rev = fo.loc[fo["Customer_Type"] == "Repeat", "grand_total"].sum()
    top_cat_share = safe_div(cat["Product_Revenue"].head(3).sum(), fi["Product_Revenue"].sum()) * 100 if not cat.empty else 0
    st.markdown(
        f'<div class="insight-row">'
        f'<div class="insight-card" style="border-left:3px solid {TEAL};">💎 <span class="insight-label">Repeat value</span><div class="insight-value">{money(repeat_rev)}</div><div class="insight-note">selected-period order value</div></div>'
        f'<div class="insight-card" style="border-left:3px solid {AMBER};">🏆 <span class="insight-label">Top category concentration</span><div class="insight-value">{top_cat_share:.1f}%</div><div class="insight-note">top 3 categories by product revenue</div></div>'
        f'<div class="insight-card" style="border-left:3px solid {RED};">⚠ <span class="insight-label">Refund exposure</span><div class="insight-value">{money(refund_value)}</div><div class="insight-note">order value from refund orders</div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="signal">💡 <b>Executive signal:</b> Repeat-customer order value in the current selection is '
        f'<b>{money(repeat_rev)}</b>. Use the Customers page to inspect purchase frequency and concentration.</div>',
        unsafe_allow_html=True,
    )

elif page == "Sales":
    section("Sales performance", "Revenue and order-volume movement over time.", icon="📈", accent=TEAL)
    monthly = fo.groupby("Month_Label").agg(
        Orders=("increment_id", "nunique"), Revenue=("grand_total", "sum")
    ).reset_index().sort_values("Month_Label")
    a, b = st.columns(2)
    with a:
        fig = px.line(monthly, x="Month_Label", y="Revenue", markers=True)
        fig.update_traces(line_color=BLUE, marker_color=CYAN, line_width=3)
        chart_layout(fig, 370, "Monthly Revenue Trend")
        st.plotly_chart(fig, use_container_width=True)
    with b:
        fig = px.bar(monthly, x="Month_Label", y="Orders")
        fig.update_traces(marker_color=PURPLE)
        chart_layout(fig, 370, "Monthly Order Volume")
        st.plotly_chart(fig, use_container_width=True)

    a, b, c = st.columns(3)
    with a:
        show_kpi("Highest Order", money(fo["grand_total"].max() if not fo.empty else 0), "Filtered maximum", ORANGE, icon="🚀")
    with b:
        show_kpi("Median Order", money(fo["grand_total"].median() if not fo.empty else 0), "Filtered median", CYAN, icon="📊")
    with c:
        show_kpi("Product Revenue", money(fi["Product_Revenue"].sum()), "Price × quantity", TEAL, icon="💹")

    section("Order value distribution", "The distribution shows how concentrated the order values are.", icon="📊", accent=CYAN)
    hist = fo["grand_total"].dropna()
    fig = px.histogram(hist, nbins=55)
    fig.update_traces(marker_color=CYAN)
    chart_layout(fig, 350, "Distribution of Order Values")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Customers":
    section("Customer behavior", "Frequency, revenue contribution and customer-level concentration.", icon="👥", accent=PURPLE)
    cust = fo.groupby("Customer ID", dropna=True).agg(
        Orders=("increment_id", "nunique"), Revenue=("grand_total", "sum")
    ).reset_index()
    cust["Customer_Type"] = np.where(cust["Orders"] > 1, "Repeat", "One-time")

    a, b = st.columns(2)
    with a:
        mix = cust["Customer_Type"].value_counts().reset_index()
        mix.columns = ["Customer Type", "Customers"]
        fig = px.pie(mix, names="Customer Type", values="Customers", hole=.60)
        fig.update_traces(marker_colors=[BLUE, CYAN])
        chart_layout(fig, 350, "Customer Type Mix")
        st.plotly_chart(fig, use_container_width=True)
    with b:
        sample = cust.sample(min(12000, len(cust)), random_state=42) if len(cust) else cust
        fig = px.scatter(sample, x="Orders", y="Revenue", log_x=True, log_y=True, opacity=.55)
        fig.update_traces(marker_color=ORANGE, marker_size=6)
        chart_layout(fig, 350, "Orders vs Customer Revenue")
        st.plotly_chart(fig, use_container_width=True)

    bins = [-1, 1, 2, 5, 10, np.inf]
    labels = ["1 order", "2 orders", "3–5 orders", "6–10 orders", "11+ orders"]
    cust["Frequency"] = pd.cut(cust["Orders"], bins=bins, labels=labels)
    freq = cust.groupby("Frequency", observed=False).agg(Customers=("Customer ID", "count"), Revenue=("Revenue", "sum")).reset_index()
    fig = px.bar(freq, x="Frequency", y="Customers")
    fig.update_traces(marker_color=TEAL)
    chart_layout(fig, 335, "Customer Purchase Frequency")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### 🏆 Highest-value customers")
    top = cust.nlargest(10, "Revenue").sort_values("Revenue", ascending=False)
    st.dataframe(top, use_container_width=True, hide_index=True)

elif page == "Products":
    section("Products & SKUs", "Product-level revenue, demand and pricing patterns.", icon="📦", accent=AMBER)
    prod = fi.copy()
    prod["sku"] = prod["sku"].fillna("Unknown")
    top_sku = prod.groupby("sku").agg(Revenue=("Product_Revenue", "sum"), Quantity=("qty_ordered", "sum")).reset_index().nlargest(15, "Revenue")
    cat = prod.groupby("category_name_1", dropna=False)["Product_Revenue"].sum().reset_index().sort_values("Product_Revenue", ascending=False)
    cat["category_name_1"] = cat["category_name_1"].fillna("Unknown")

    a, b = st.columns(2)
    with a:
        fig = px.bar(top_sku.head(10), x="Revenue", y="sku", orientation="h")
        fig.update_traces(marker_color=BLUE)
        chart_layout(fig, 410, "Top 10 SKUs by Product Revenue")
        st.plotly_chart(fig, use_container_width=True)
    with b:
        fig = px.bar(cat.head(10), x="Product_Revenue", y="category_name_1", orientation="h")
        fig.update_traces(marker_color=AMBER)
        chart_layout(fig, 410, "Category Product Revenue")
        st.plotly_chart(fig, use_container_width=True)

    a, b = st.columns(2)
    with a:
        sample = prod.sample(min(12000, len(prod)), random_state=42) if len(prod) else prod
        fig = px.scatter(sample, x="qty_ordered", y="price", size="Product_Revenue", opacity=.45)
        fig.update_traces(marker_color=CYAN)
        chart_layout(fig, 360, "Quantity vs Price")
        st.plotly_chart(fig, use_container_width=True)
    with b:
        fig = px.histogram(prod, x="price", nbins=55)
        fig.update_traces(marker_color=PURPLE)
        chart_layout(fig, 360, "Product Price Distribution")
        st.plotly_chart(fig, use_container_width=True)

elif page == "Refunds":
    section("Refund & returns risk", "Refund exposure at order level and its movement across categories and time.", icon="↩", accent=RED)
    refund = fo[fo["Is_Refund"]].copy()
    nonrefund = fo[~fo["Is_Refund"]].copy()
    r1, r2, r3 = st.columns(3)
    with r1:
        show_kpi("Refund Orders", number(len(refund)), "Unique refund orders", RED, icon="↩")
    with r2:
        show_kpi("Refund Value", money(refund["grand_total"].sum()), "Unique order value", ORANGE, icon="💸")
    with r3:
        show_kpi("Refund Rate", percent(safe_div(len(refund), len(fo))*100), "Refund orders / orders", AMBER, icon="⚠")

    monthly = fo.groupby("Month_Label").agg(Orders=("increment_id", "nunique"), Refunds=("Is_Refund", "sum")).reset_index()
    monthly["Refund Rate"] = monthly.apply(lambda r: safe_div(r["Refunds"], r["Orders"])*100, axis=1)

    a, b = st.columns(2)
    with a:
        fig = px.line(monthly, x="Month_Label", y="Refund Rate", markers=True)
        fig.update_traces(line_color=RED, marker_color=ORANGE, line_width=3)
        chart_layout(fig, 370, "Monthly Refund Rate")
        st.plotly_chart(fig, use_container_width=True)
    with b:
        comp = pd.DataFrame({"Type": ["Refund Orders", "Non-Refund Orders"], "Orders": [len(refund), len(nonrefund)]})
        fig = px.pie(comp, names="Type", values="Orders", hole=.58)
        fig.update_traces(marker_colors=[RED, GREEN])
        chart_layout(fig, 370, "Refund vs Non-Refund Orders")
        st.plotly_chart(fig, use_container_width=True)

    refund_ids = set(refund["increment_id"])
    rc = fi.assign(Is_Refund=fi["increment_id"].isin(refund_ids)).groupby("category_name_1").agg(
        Orders=("increment_id", "nunique"), Refund_Orders=("Is_Refund", "sum")
    ).reset_index()
    rc["Refund Rate"] = rc.apply(lambda r: safe_div(r["Refund_Orders"], r["Orders"])*100, axis=1)
    rc = rc.sort_values("Refund Rate", ascending=False).head(10)
    fig = px.bar(rc, x="Refund Rate", y="category_name_1", orientation="h")
    fig.update_traces(marker_color=RED)
    chart_layout(fig, 390, "Category Refund Rate")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Payments":
    section("Payment channel performance", "Order volume, revenue contribution and average order value by payment method.", icon="💳", accent=CYAN)
    pm = fo.groupby("payment_method").agg(
        Orders=("increment_id", "nunique"), Revenue=("grand_total", "sum")
    ).reset_index()
    pm["AOV"] = pm["Revenue"] / pm["Orders"].replace(0, np.nan)
    pm = pm.sort_values("Revenue", ascending=False)

    a, b = st.columns(2)
    with a:
        fig = px.bar(pm.head(10), x="payment_method", y="Orders")
        fig.update_traces(marker_color=BLUE)
        chart_layout(fig, 380, "Payment Methods by Order Count")
        st.plotly_chart(fig, use_container_width=True)
    with b:
        fig = px.bar(pm.head(10), x="payment_method", y="Revenue")
        fig.update_traces(marker_color=TEAL)
        chart_layout(fig, 380, "Payment Methods by Revenue")
        st.plotly_chart(fig, use_container_width=True)

    fig = px.scatter(pm, x="Orders", y="AOV", size="Revenue", text="payment_method")
    fig.update_traces(marker_color=AMBER, textposition="top center")
    chart_layout(fig, 390, "Payment Volume vs Average Order Value")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### 💳 Payment method detail")
    st.dataframe(pm.sort_values("Revenue", ascending=False), use_container_width=True, hide_index=True)

# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------
st.markdown(
    '<div style="height:1px;margin:26px 0 14px;background:linear-gradient(90deg,transparent,rgba(76,141,255,.35),rgba(244,200,106,.35),transparent);"></div>',
    unsafe_allow_html=True,
)
st.markdown(
    f'<div class="foot">◆ &nbsp; Data period: {df["created_at"].min():%d %b %Y} → {df["created_at"].max():%d %b %Y} &nbsp; • &nbsp; '
    f'{len(df):,}+ cleaned rows &nbsp; • &nbsp; {len(orders):,} unique orders &nbsp; • &nbsp; '
    f'<span style="color:#F4C86A;font-weight:800;">Executive Analytics Suite</span> — built with Python, Pandas, Plotly &amp; Streamlit</div>',
    unsafe_allow_html=True,
)