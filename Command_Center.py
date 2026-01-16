import base64
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="Portfolio JRR",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------
# Paths
# ----------------------------
ASSETS = Path(__file__).parent / "assets"
VIDEO_FILENAME = "digital-wall.mp4"   # <-- tu video ya subido
VIDEO_PATH = ASSETS / VIDEO_FILENAME

# (Opcional) Logo mini. Si no existe, no pasa nada.
LOGO_FILENAME = "logo.png"
LOGO_PATH = ASSETS / LOGO_FILENAME

# ----------------------------
# Helpers
# ----------------------------
def b64_file(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")

video_b64 = b64_file(VIDEO_PATH) if VIDEO_PATH.exists() else ""
logo_b64 = b64_file(LOGO_PATH) if LOGO_PATH.exists() else ""

# ----------------------------
# Global CSS (Streamlit chrome cleanup)
# ----------------------------
st.markdown(
    """
<style>
header[data-testid="stHeader"] {display:none;}
footer {visibility:hidden;}
.block-container {padding-top: 22px !important;}
</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------
# HERO (rendered with components.html to avoid HTML escaping issues)
# ----------------------------
hero_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<style>
  :root {{
    --bg: #000000;
  }}
  body {{ margin:0; background: transparent; }}

  .hero {{
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100vh;
    background: var(--bg);
    overflow: hidden;
  }}

  video {{
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    opacity: 0.92; /* nitido */
    filter: none;
  }}

  .overlay {{
    position: absolute;
    inset: 0;
    background:
      radial-gradient(ellipse at center,
        rgba(0,0,0,0.18),
        rgba(0,0,0,0.78) 55%,
        rgba(0,0,0,0.94) 100%);
  }}
</style>
</head>
<body>
  <div class="hero">
    {"<video autoplay muted loop playsinline><source src='data:video/mp4;base64," + video_b64 + "' type='video/mp4'></video>" if video_b64 else ""}
    <div class="overlay"></div>
  </div>
</body>
</html>
"""
components.html(hero_html, height=1000, scrolling=False)
st.markdown("""
<style>
/* Remove Streamlit padding so it feels like a real website */
.block-container { padding: 0 !important; max-width: 100% !important; }
section.main > div { padding: 0 !important; }

/* Top bar overlay */
.topbar {
  position: fixed;
  top: 18px;
  left: 22px;
  right: 22px;
  z-index: 99999;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  pointer-events: none;
}

.topbar .left,
.topbar .center,
.topbar .right {
  pointer-events: auto;
  display: flex;
  align-items: center;
}

.topbar .left { justify-content: flex-start; }
.topbar .center { justify-content: center; }
.topbar .right { justify-content: flex-end; }

.brand {
  color: #fff;
  font-weight: 850;
  letter-spacing: 0.2px;
  padding: 10px 14px;
  border-radius: 999px;
  background: rgba(0,0,0,0.38);
  border: 1px solid rgba(255,255,255,0.14);
  backdrop-filter: blur(10px);
}

.center-cta .stButton > button {
  border-radius: 999px !important;
  padding: 12px 18px !important;
  border: 1px solid rgba(255,255,255,0.18) !important;
  background: rgba(255,255,255,0.06) !important;
  color: #fff !important;
  font-weight: 850 !important;
  letter-spacing: 2.6px !important;
  text-transform: uppercase !important;
  backdrop-filter: blur(10px);
}
.center-cta .stButton > button:hover {
  border-color: rgba(255,255,255,0.30) !important;
  background: rgba(255,255,255,0.10) !important;
}

.burger .stButton > button {
  width: 46px !important;
  height: 46px !important;
  border-radius: 14px !important;
  padding: 0 !important;
  border: 1px solid rgba(255,255,255,0.18) !important;
  background: rgba(0,0,0,0.38) !important;
  color: #fff !important;
  font-weight: 900 !important;
  backdrop-filter: blur(10px);
}
.burger .stButton > button:hover {
  border-color: rgba(255,255,255,0.30) !important;
}
</style>
""", unsafe_allow_html=True)

# Topbar layout (real clickable Streamlit widgets)
left, center, right = st.columns([1, 1, 1])

# We place them inside a fixed-position wrapper using HTML.
st.markdown('<div class="topbar"><div class="left"><div class="brand">Portfolio JRR</div></div><div class="center"></div><div class="right"></div></div>', unsafe_allow_html=True)

# Now render Streamlit buttons aligned by placing them in columns and styling them
with center:
    st.markdown('<div class="center-cta">', unsafe_allow_html=True)
    if st.button("WELCOME TO MY LAB", key="cta_welcome"):
        st.switch_page("pages/1_Industries.py")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="burger">', unsafe_allow_html=True)
    if st.button("≡", key="burger_menu"):
        st.session_state["menu_open"] = not st.session_state.get("menu_open", False)
    st.markdown('</div>', unsafe_allow_html=True)
if st.session_state.get("menu_open", False):
    st.markdown("""
    <style>
    .menu-panel{
      position: fixed;
      top: 76px;
      right: 22px;
      z-index: 99999;
      width: 220px;
      border-radius: 16px;
      padding: 10px;
      background: rgba(0,0,0,0.72);
      border: 1px solid rgba(255,255,255,0.14);
      backdrop-filter: blur(12px);
    }
    .menu-panel .stButton > button{
      width: 100%;
      border-radius: 12px !important;
      padding: 10px 12px !important;
      border: 1px solid rgba(255,255,255,0.14) !important;
      background: rgba(255,255,255,0.06) !important;
      color: #fff !important;
      font-weight: 750 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="menu-panel">', unsafe_allow_html=True)
    if st.button("About", key="menu_about"):
        st.session_state["menu_open"] = False
        st.switch_page("pages/3_About_Me.py")
    if st.button("Projects", key="menu_projects"):
        st.session_state["menu_open"] = False
        st.switch_page("pages/4_Projects.py")
    if st.button("Contact", key="menu_contact"):
        st.session_state["menu_open"] = False
        st.switch_page("pages/5_Contact.py")
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# TOP NAV (global, outside the card)
# ----------------------------
st.markdown(
    """
<style>
.topnav{
  position: fixed;
  top: 14px;
  left: 24px;
  right: 24px;
  z-index: 9999;
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap: 14px;
  pointer-events: none; /* allow clicks only on buttons */
}
.topnav .left, .topnav .right { pointer-events: auto; }

.brand-chip{
  display:flex;
  align-items:center;
  gap:10px;
  padding:10px 14px;
  border-radius: 999px;
  background: rgba(0,0,0,0.42);
  border: 1px solid rgba(255,255,255,0.14);
  color: #fff;
  font-weight: 800;
  letter-spacing: 0.2px;
  backdrop-filter: blur(10px);
}
.brand-chip img{
  width: 22px; height: 22px; border-radius: 7px;
}

.nav-actions{
  display:flex;
  align-items:center;
  gap:10px;
}
.nav-btn button{
  border-radius: 999px !important;
  padding: 10px 14px !important;
  border: 1px solid rgba(255,255,255,0.16) !important;
  background: rgba(0,0,0,0.42) !important;
  color: #fff !important;
  font-weight: 700 !important;
  backdrop-filter: blur(10px);
}
.nav-btn button:hover{
  border-color: rgba(255,255,255,0.28) !important;
}
</style>
<div class="topnav">
  <div class="left">
    <div class="brand-chip">Portfolio JRR</div>
  </div>
  <div class="right"></div>
</div>
""",
    unsafe_allow_html=True,
)

# --- Real clickable nav buttons ---
# We render buttons separately so they truly work (switch_page)
nav_cols = st.columns([0.62, 0.38])
with nav_cols[1]:
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("About", key="nav_about"):
            st.switch_page("pages/3_About_Me.py")
    with b2:
        if st.button("Projects", key="nav_projects"):
            st.switch_page("pages/4_Projects.py")
    with b3:
        if st.button("Contact", key="nav_contact"):
            st.switch_page("pages/5_Contact.py")

# apply the nav button style wrapper
st.markdown(
    """
<style>
div[data-testid="column"] .stButton { margin-top: 0px; }
div[data-testid="column"] .stButton > button {
  border-radius: 999px !important;
  padding: 10px 14px !important;
  border: 1px solid rgba(255,255,255,0.16) !important;
  background: rgba(0,0,0,0.42) !important;
  color: #fff !important;
  font-weight: 700 !important;
  backdrop-filter: blur(10px);
}
div[data-testid="column"] .stButton > button:hover {
  border-color: rgba(255,255,255,0.28) !important;
}
</style>
""",
    unsafe_allow_html=True,
)

components.html(hero_html, height=820, scrolling=False)


# ----------------------------
# Industries preview grid (home)
# ----------------------------
st.subheader("Strategic Domains")
st.caption("Organized like IBM Solutions — projects grouped by industry.")

industries = [
    ("Finance • Banking • Insurance", "Risk modeling, anomaly detection, forecasting, decision engines."),
    ("Sports Analytics", "Simulation, scenario testing, performance & market signals."),
    ("Energy", "Demand forecasting, operational optimization, anomaly detection."),
    ("Manufacturing", "Quality analytics, predictive maintenance, process optimization."),
    ("Healthcare", "Risk prediction, operational intelligence, pattern detection."),
    ("Transportation & Logistics", "Route optimization, ETA forecasting, supply-chain intelligence."),
    ("Politics & Public Systems", "Sentiment, information signals, scenario modeling."),
    ("Marketing & Growth", "Segmentation, uplift/propensity, attribution, demand intelligence."),
]

cols = st.columns(4)
for i, (name, desc) in enumerate(industries):
    with cols[i % 4]:
        st.markdown(
            f"""
            <div style="
              border:1px solid rgba(255,255,255,0.10);
              border-radius:16px;
              padding:14px 14px 12px 14px;
              background: rgba(255,255,255,0.03);
              min-height: 92px;">
              <div style="font-weight:760; margin-bottom:6px;">{name}</div>
              <div style="opacity:0.82; font-size:12.5px; line-height:1.35;">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
