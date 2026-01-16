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
VIDEO_FILENAME = "digital-wall.mp4"  # tu video
VIDEO_PATH = ASSETS / VIDEO_FILENAME

LOGO_FILENAME = "logo.png"  # opcional
LOGO_PATH = ASSETS / LOGO_FILENAME

# ----------------------------
# Helpers
# ----------------------------
def b64_file(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")

video_b64 = b64_file(VIDEO_PATH) if VIDEO_PATH.exists() else ""
logo_b64 = b64_file(LOGO_PATH) if LOGO_PATH.exists() else ""

# ----------------------------
# Global CSS (remove Streamlit chrome + padding)
# ----------------------------
st.markdown(
    """
<style>
header[data-testid="stHeader"] {display:none;}
footer {visibility:hidden;}

/* remove all default padding so it feels like a website */
.block-container { padding: 0 !important; max-width: 100% !important; }
section.main > div { padding: 0 !important; }

/* hide the empty space above */
div[data-testid="stVerticalBlock"] { gap: 0rem; }
</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------
# HERO (video fullscreen)
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
    opacity: 0.92;
    filter: none;
  }}

  .overlay {{
    position: absolute;
    inset: 0;
    background:
      radial-gradient(ellipse at center,
        rgba(0,0,0,0.35),
        rgba(0,0,0,0.78) 55%,
        rgba(0,0,0,0.92) 100%);
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

# Use a large height so the iframe covers most screens
components.html(hero_html, height=1100, scrolling=False)
st.markdown(
    """
<style>
/* HARD reset spacing so nothing pushes content */
.block-container { padding: 0 !important; margin: 0 !important; }
section.main > div { padding: 0 !important; margin: 0 !important; }
div[data-testid="stVerticalBlock"] { gap: 0rem; padding: 0 !important; margin: 0 !important; }

/* --- FIXED BRAND (top-left) --- */
.overlay-brand {
  position: fixed;
  top: 18px;
  left: 22px;
  z-index: 100000;
  display:flex;
  align-items:center;
  gap:10px;
  padding: 10px 14px;
  border-radius: 999px;
  background: rgba(0,0,0,0.38);
  border: 1px solid rgba(255,255,255,0.14);
  color: #fff;
  font-weight: 850;
  letter-spacing: 0.2px;
  backdrop-filter: blur(10px);
}
.overlay-brand img { width: 22px; height: 22px; border-radius: 7px; }

/* --- BIG CENTER CTA (true center) --- */
.overlay-cta {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 100000;
}

/* make the Streamlit button huge and premium */
.overlay-cta div.stButton > button {
  border-radius: 999px !important;
  padding: 22px 36px !important;
  border: 1px solid rgba(255,255,255,0.24) !important;
  background: rgba(0,0,0,0.62) !important;
  color: #fff !important;
  font-weight: 950 !important;
  font-size: 18px !important;
  letter-spacing: 4.2px !important;
  text-transform: uppercase !important;
  backdrop-filter: blur(14px);
  box-shadow: 0 24px 90px rgba(0,0,0,0.65);
}
.overlay-cta div.stButton > button:hover {
  border-color: rgba(255,255,255,0.36) !important;
  background: rgba(0,0,0,0.76) !important;
  transform: translateY(-1px);
}

/* --- BURGER TOP-RIGHT --- */
.overlay-burger {
  position: fixed;
  top: 18px;
  right: 22px;
  z-index: 100000;
}
.overlay-burger div.stButton > button {
  width: 56px !important;
  height: 56px !important;
  border-radius: 16px !important;
  padding: 0 !important;
  border: 1px solid rgba(255,255,255,0.18) !important;
  background: rgba(0,0,0,0.52) !important;
  color: #fff !important;
  font-weight: 950 !important;
  font-size: 22px !important;
  backdrop-filter: blur(14px);
}
.overlay-burger div.stButton > button:hover {
  border-color: rgba(255,255,255,0.30) !important;
  background: rgba(0,0,0,0.70) !important;
}

/* --- MENU PANEL (under burger) --- */
.menu-panel {
  position: fixed;
  top: 84px;
  right: 22px;
  z-index: 100000;
  width: 220px;
  border-radius: 16px;
  padding: 10px;
  background: rgba(0,0,0,0.74);
  border: 1px solid rgba(255,255,255,0.14);
  backdrop-filter: blur(14px);
}
.menu-panel div.stButton > button{
  width: 100%;
  border-radius: 12px !important;
  padding: 11px 12px !important;
  border: 1px solid rgba(255,255,255,0.14) !important;
  background: rgba(255,255,255,0.06) !important;
  color: #fff !important;
  font-weight: 780 !important;
}
.menu-panel div.stButton > button:hover{
  border-color: rgba(255,255,255,0.28) !important;
  background: rgba(255,255,255,0.10) !important;
}

/* --- hide Streamlit's bottom “ghost space” from columns/buttons --- */
div[data-testid="stAppViewContainer"] { background: transparent !important; }
</style>
""",
    unsafe_allow_html=True,
)

# Brand (top-left)
brand_img_html = f"<img src='data:image/png;base64,{logo_b64}' />" if logo_b64 else ""
st.markdown(f'<div class="overlay-brand">{brand_img_html}Portfolio JRR</div>', unsafe_allow_html=True)

# Center CTA (true center)
st.markdown('<div class="overlay-cta">', unsafe_allow_html=True)
if st.button("WELCOME TO MY LAB", key="cta_welcome"):
    st.switch_page("pages/1_Industries.py")
st.markdown('</div>', unsafe_allow_html=True)

# Burger (top-right)
st.markdown('<div class="overlay-burger">', unsafe_allow_html=True)
if st.button("≡", key="burger_menu"):
    st.session_state["menu_open"] = not st.session_state.get("menu_open", False)
st.markdown('</div>', unsafe_allow_html=True)

# Burger menu items
if st.session_state.get("menu_open", False):
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

    st.markdown("</div>", unsafe_allow_html=True)

# Fixed wrapper (visual)
brand_img_html = f"<img src='data:image/png;base64,{logo_b64}' />" if logo_b64 else ""
st.markdown(
    f"""
<div class="topbar">
  <div class="left">
    <div class="brand-chip">{brand_img_html}Portfolio JRR</div>
  </div>
  <div class="center"></div>
  <div class="right"></div>
</div>
""",
    unsafe_allow_html=True,
)

# ----------------------------
# FIXED OVERLAY CONTROLS (center CTA + top-right burger)
# ----------------------------
st.markdown(
    """
<style>
/* Big center CTA wrapper */
.overlay-cta {
  position: fixed;
  top: 44%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 100000;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Make Streamlit button look like a big hero CTA */
.overlay-cta .stButton > button {
  border-radius: 999px !important;
  padding: 18px 28px !important;
  border: 1px solid rgba(255,255,255,0.22) !important;
  background: rgba(0,0,0,0.55) !important;
  color: #fff !important;
  font-weight: 900 !important;
  font-size: 16px !important;
  letter-spacing: 3.4px !important;
  text-transform: uppercase !important;
  backdrop-filter: blur(12px);
  box-shadow: 0 18px 60px rgba(0,0,0,0.55);
}
.overlay-cta .stButton > button:hover {
  border-color: rgba(255,255,255,0.34) !important;
  background: rgba(0,0,0,0.68) !important;
  transform: translateY(-1px);
}

/* Top-right burger wrapper */
.overlay-burger {
  position: fixed;
  top: 18px;
  right: 22px;
  z-index: 100000;
}
.overlay-burger .stButton > button {
  width: 54px !important;
  height: 54px !important;
  border-radius: 16px !important;
  padding: 0 !important;
  border: 1px solid rgba(255,255,255,0.18) !important;
  background: rgba(0,0,0,0.45) !important;
  color: #fff !important;
  font-weight: 950 !important;
  font-size: 20px !important;
  backdrop-filter: blur(12px);
}
.overlay-burger .stButton > button:hover {
  border-color: rgba(255,255,255,0.30) !important;
  background: rgba(0,0,0,0.62) !important;
}

/* Optional: small left brand (if you want it) */
.overlay-brand {
  position: fixed;
  top: 18px;
  left: 22px;
  z-index: 100000;
  display:flex;
  align-items:center;
  gap:10px;
  padding: 10px 14px;
  border-radius: 999px;
  background: rgba(0,0,0,0.38);
  border: 1px solid rgba(255,255,255,0.14);
  color: #fff;
  font-weight: 850;
  letter-spacing: 0.2px;
  backdrop-filter: blur(10px);
}
.overlay-brand img { width: 22px; height: 22px; border-radius: 7px; }
</style>
""",
    unsafe_allow_html=True,
)

# (Optional) left brand chip (keep it if you want)
brand_img_html = f"<img src='data:image/png;base64,{logo_b64}' />" if logo_b64 else ""

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
              <div style="font-weight:760; margin-bottom:6px; color:#fff;">{name}</div>
              <div style="opacity:0.82; font-size:12.5px; line-height:1.35; color:rgba(255,255,255,0.78);">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
