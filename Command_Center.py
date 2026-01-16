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
VIDEO_FILENAME = "bothhands-hud-fingerprint.mp4"   # <-- tu video ya subido
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
    --card: #ffffff;
    --text: #0b0f14;
    --muted: #5b6675;
    --border: rgba(0,0,0,0.10);
  }}

  body {{
    margin: 0;
    background: transparent;
    font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
  }}

  /* HERO WRAPPER - FULLSCREEN */
  .hero-wrap {{
    position: relative;
    width: 100vw;
    height: 100vh;
    min-height: 100vh;
    overflow: hidden;
    background: var(--bg);
  }}

  /* VIDEO BG */
  .hero-wrap video {{
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    opacity: 1;
    filter: contrast(1.08) saturate(1.1);
  }}

  .fallback {{
    position:absolute;
    inset:0;
    display:flex;
    align-items:center;
    justify-content:center;
    color: rgba(255,255,255,0.75);
    font-size: 14px;
    letter-spacing: 1.2px;
  }}

  /* CINEMATIC OVERLAY */
  .hero-overlay {{
    position: absolute;
    inset: 0;
    background: radial-gradient(
      ellipse at center,
      rgba(0,0,0,0.05),
      rgba(0,0,0,0.75) 45%,
      rgba(0,0,0,0.95) 100%
    );
  }}

  /* SMALLER CENTER CARD */
  .command-card {{
    position: absolute;
    top: 54%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: min(820px, 90%);
    background: var(--card);
    border-radius: 22px;
    box-shadow: 0 25px 90px rgba(0,0,0,0.65);
    border: 1px solid var(--border);
    padding: 24px 30px 22px 30px;
  }}

  /* TOP BAR */
  

  .brand img {{
    width: 26px;
    height: 26px;
    border-radius: 8px;
  }}

  /* BODY */
  .card-body {{
    padding: 26px 8px 4px 8px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }}

  .kicker {{
    letter-spacing: 3.2px;
    font-size: 11px;
    color: var(--muted);
    font-weight: 750;
    text-transform: uppercase;
  }}

  .h1 {{
    margin-top: 8px;
    font-size: 46px;
    line-height: 1.03;
    font-weight: 900;
    color: var(--text);
  }}

  .sub {{
    margin-top: 10px;
    max-width: 620px;
    font-size: 16px;
    line-height: 1.5;
    color: rgba(11,15,20,0.80);
  }}

  .cta {{
    margin-top: 18px;
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    justify-content: center;
  }}

  .pill {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 11px 16px;
    border-radius: 999px;
    border: 1px solid rgba(0,0,0,0.14);
    font-weight: 750;
    color: var(--text);
    background: rgba(0,0,0,0.02);
    transition: transform .12s ease, box-shadow .12s ease, background .12s ease;
  }}

  .pill.primary {{
    background: #0b0f14;
    color: #ffffff;
    border-color: #0b0f14;
    box-shadow: 0 10px 28px rgba(11,15,20,0.25);
  }}

  .pill:hover {{
    transform: translateY(-1px);
  }}

  .card-foot {{
    margin-top: 18px;
    padding-top: 12px;
    border-top: 1px solid rgba(0,0,0,0.08);
    width: 100%;
    display: flex;
    justify-content: space-between;
    color: rgba(11,15,20,0.55);
    font-size: 12px;
    font-weight: 650;
  }}

  @media (max-width: 780px) {{
    .nav span {{ display: none; }}
    .h1 {{ font-size: 38px; }}
  }}
</style>
</head>
<body>
  <div class="hero-wrap">
    {"<video autoplay muted loop playsinline><source src='data:video/mp4;base64," + video_b64 + "' type='video/mp4'></video>" if video_b64 else "<div class='fallback'>Add assets/" + VIDEO_FILENAME + " to enable video background</div>"}
    <div class="hero-overlay"></div>

    <div class="command-card">
        <div class="nav">
          <span>About</span>
          <span>Projects</span>
          <span>Contact</span>
          <div class="burger">☰</div>
        </div>
      </div>

      <div class="card-body">
        <div class="kicker">COMMAND CENTER</div>
        <div class="h1">WELCOME TO MY LAB</div>
        <div class="sub">
          Engineering futuristic intelligence systems — predictive models, simulation engines,
          and decision frameworks across critical industries.
        </div>

        <div class="cta">
          <span class="pill primary">Enter the Lab</span>
          <span class="pill">Open Simulation Lab</span>
        </div>

        <div class="card-foot">
          <span>Intelligence • Engineering • Systems</span>
          <span>Scroll ↓</span>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""
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
# Real Streamlit navigation buttons (functional)
# ----------------------------
c1, c2, c3 = st.columns([0.22, 0.22, 0.56])
with c1:
    if st.button("Enter the Lab", use_container_width=True):
        try:
            st.switch_page("pages/1_Industries.py")
        except Exception:
            st.warning("Industries page not created yet.")
with c2:
    if st.button("Open Simulation Lab", use_container_width=True):
        try:
            st.switch_page("pages/2_Simulation_Lab.py")
        except Exception:
            st.warning("Simulation Lab page not created yet.")

st.write("")

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
