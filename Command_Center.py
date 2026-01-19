import base64
from pathlib import Path

import streamlit as st

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Portfolio JRR",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================
# SIDEBAR NATIVO (NAV)
# =========================
with st.sidebar:
    st.markdown("## Portfolio JRR")
    nav = st.radio(
        "Navigate",
        ["Home", "About", "Projects", "Lab", "Contact"],
        index=0,
        label_visibility="collapsed",
    )

if nav == "About":
    st.switch_page("pages/1_About_Me.py")
elif nav == "Projects":
    st.switch_page("pages/2_Projects.py")
elif nav == "Lab":
    st.switch_page("pages/4_Lab.py")
elif nav == "Contact":
    st.switch_page("pages/3_Contact.py")

# =========================
# ASSETS
# =========================
ASSETS = Path(__file__).parent / "assets"
VIDEO_PATH = ASSETS / "Data.mp4"
LOGO_PATH = ASSETS / "DS.png"


def b64_file(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")


video_b64 = b64_file(VIDEO_PATH) if VIDEO_PATH.exists() else ""
logo_b64 = b64_file(LOGO_PATH) if LOGO_PATH.exists() else ""

if not video_b64:
    st.error("No encuentro el video. Coloca tu archivo en: assets/data.mp4")
    st.stop()

# =========================
# GLOBAL CSS (FULLSCREEN + HIDE CHROME)
# =========================
st.markdown(
    """
<style>
/* Quitar chrome Streamlit */
header[data-testid="stHeader"] { display:none; }
footer { visibility:hidden; }

/* Sin padding/márgenes */
.block-container { padding:0 !important; max-width:100% !important; }
section.main > div { padding:0 !important; }

/* Evitar scroll blanco extra */
html, body { height:100%; margin:0; background:#000; overflow:hidden; }
</style>
""",
    unsafe_allow_html=True,
)

# =========================
# HOME HERO (VIDEO FULLSCREEN + RED LINES)
# =========================
logo_html = (
    f"<img src='data:image/png;base64,{logo_b64}' alt='logo' />" if logo_b64 else ""
)

hero_html = f"""
<style>
/* HERO WRAPPER */
.hero {{
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: #000;
  font-family: system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
}}

/* VIDEO */
.hero video {{
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 0;
}}

/* DARK OVERLAY */
.overlay-dark {{
  position:absolute;
  inset:0;
  background: rgba(0,0,0,0.35);
  z-index:1;
  pointer-events:none;
}}

/* TOP BAR (LOGO + TITLE) */
.topbar {{
  position:absolute;
  top:0; left:0; right:0;
  z-index: 5;
  display:flex;
  align-items:center;
  justify-content:flex-start;
  padding: 22px 28px;
  color:#fff;
}}

.brand {{
  display:flex;
  align-items:center;
  gap: 12px;
  font-weight: 800;
  letter-spacing: 1px;
  text-transform: uppercase;
  user-select:none;
}}

.brand img {{
  width: 36px;
  height: 36px;
  object-fit: contain;
  background: #fff;
  padding: 6px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.25);
}}

/* CENTER TEXT */
.center {{
  position:absolute;
  inset:0;
  z-index:4;
  display:flex;
  align-items:center;
  justify-content:center;
  text-align:center;
  color:#fff;
  padding: 0 24px;
}}

.center h1 {{
  font-size: clamp(2.4rem, 5vw, 4.4rem);
  font-weight: 900;
  margin: 0;
  text-shadow: 0 10px 30px rgba(0,0,0,0.6);
}}

/* RED LINES */
.accents {{
  position:absolute;
  inset:0;
  z-index:3;
  pointer-events:none;
}}

.line {{
  position:absolute;
  height: 3px;
  background: #ff2a2a;
  opacity: 0.9;
}}

.l1 {{ top: 92px; right: 130px; width: 120px; }}
.l2 {{ top: 122px; right: 40px; width: 240px; }}
.l3 {{ bottom: 70px; left: 40px; width: 220px; opacity: 0.55; }}
.l4 {{ top: 30%; left: 55%; width: 250px; transform: rotate(-55deg); opacity: 0.50; }}

@media (max-width: 650px) {{
  .l1, .l2, .l3, .l4 {{ display:none; }}
  .topbar {{ padding: 16px 16px; }}
}}
</style>

<div class="hero">
  <video autoplay muted loop playsinline>
    <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
  </video>

  <div class="overlay-dark"></div>

  <div class="topbar">
    <div class="brand">
      {logo_html}
      <div>Portfolio JRR</div>
    </div>
  </div>

  <div class="accents">
    <div class="line l1"></div>
    <div class="line l2"></div>
    <div class="line l3"></div>
    <div class="line l4"></div>
  </div>

  <div class="center">
    <h1>Welcome to my lab</h1>
  </div>
</div>
"""

st.components.v1.html(hero_html, height=1, scrolling=False)
