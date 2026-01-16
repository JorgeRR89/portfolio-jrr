import base64
from pathlib import Path
import streamlit as st

# -------------------
# Config
# -------------------
st.set_page_config(
    page_title="Portfolio JRR",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ASSETS = Path(__file__).parent / "assets"
VIDEO_PATH = ASSETS / "data.mp4"
LOGO_PATH = ASSETS / "logo.png"

def b64_file(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")

video_b64 = b64_file(VIDEO_PATH) if VIDEO_PATH.exists() else ""
logo_b64 = b64_file(LOGO_PATH) if LOGO_PATH.exists() else ""

# -------------------
# Global CSS
# -------------------
st.markdown(
    """
<style>
/* Hide streamlit chrome */
header[data-testid="stHeader"] {display:none;}
footer {visibility:hidden;}
section[data-testid="stSidebar"] {display:none;}

/* Remove padding/margins */
.block-container { padding: 0 !important; max-width: 100% !important; }
section.main > div { padding: 0 !important; }

/* Hero wrapper */
.hero {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: #000;
}

/* Video background */
.hero video {
  position: absolute;
  top: 50%;
  left: 50%;
  min-width: 100%;
  min-height: 100%;
  width: auto;
  height: auto;
  transform: translate(-50%, -50%);
  object-fit: cover;
  filter: contrast(1.05) saturate(1.05);
}

/* Dark overlay */
.hero::after {
  content: "";
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.35);
  z-index: 1;
}

/* Top bar */
.topbar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  z-index: 3;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 22px 28px;
  color: #fff;
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.brand img {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  object-fit: cover;
}

/* Center headline */
.center {
  position: absolute;
  inset: 0;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 0 24px;
  color: #fff;
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
}

.center h1 {
  font-size: clamp(2.2rem, 5vw, 4.2rem);
  line-height: 1.05;
  letter-spacing: 0.5px;
  margin: 0;
  font-weight: 800;
}

/* Red tech accents (optional) */
.accents {
  position: absolute;
  inset: 0;
  z-index: 2;
  pointer-events: none;
}

.line {
  position: absolute;
  height: 3px;
  background: #ff2a2a;
  opacity: 0.9;
}

.l1 { top: 90px; right: 120px; width: 120px; }
.l2 { top: 120px; right: 40px; width: 220px; }
.l3 { bottom: 70px; left: 40px; width: 200px; opacity: 0.6; }
.l4 { top: 30%; left: 55%; width: 240px; transform: rotate(-55deg); opacity: 0.55; }

/* ===== Burger + Drawer (checkbox hack) ===== */
#menuToggle {
  display: none;
}

/* Burger button */
.burger {
  width: 52px;
  height: 52px;
  background: #ff2a2a;
  border-radius: 0px;
  display: grid;
  place-items: center;
  cursor: pointer;
  box-shadow: 0 10px 25px rgba(0,0,0,0.25);
}

.burger span {
  display: block;
  width: 22px;
  height: 2px;
  background: #fff;
  margin: 3px 0;
  transition: transform .25s ease, opacity .25s ease;
}

/* Animate burger to X */
#menuToggle:checked + label.burger span:nth-child(1) {
  transform: translateY(5px) rotate(45deg);
}
#menuToggle:checked + label.burger span:nth-child(2) {
  opacity: 0;
}
#menuToggle:checked + label.burger span:nth-child(3) {
  transform: translateY(-5px) rotate(-45deg);
}

/* Drawer */
.drawer {
  position: absolute;
  top: 0;
  right: 0;
  width: min(380px, 90vw);
  height: 100%;
  z-index: 4;
  transform: translateX(110%);
  transition: transform .28s ease;
  background: rgba(10,10,12,0.92);
  backdrop-filter: blur(10px);
  border-left: 1px solid rgba(255,255,255,0.08);
  padding: 90px 28px 28px;
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
  color: #fff;
}

/* Open drawer when checked */
#menuToggle:checked ~ .drawer {
  transform: translateX(0%);
}

/* Drawer links */
.drawer a {
  display: block;
  padding: 16px 14px;
  margin: 10px 0;
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 14px;
  text-decoration: none;
  color: #fff;
  font-weight: 700;
  letter-spacing: .5px;
  transition: background .2s ease, border-color .2s ease, transform .2s ease;
}

.drawer a:hover {
  background: rgba(255,42,42,0.16);
  border-color: rgba(255,42,42,0.65);
  transform: translateY(-1px);
}

/* small helper line */
.drawer .hint {
  opacity: 0.65;
  margin-top: 18px;
  font-size: 0.95rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# -------------------
# HTML Layout
# -------------------
brand_logo_html = (
    f'<img src="data:image/png;base64,{logo_b64}" alt="logo"/>'
    if logo_b64
    else ""
)

st.markdown(
    f"""
<div class="hero">
  <video autoplay muted loop playsinline>
    <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
  </video>

  <div class="topbar">
    <div class="brand">
      {brand_logo_html}
      <div>Portfolio JRR</div>
    </div>

    <!-- checkbox + burger label -->
    <div style="display:flex;align-items:center;gap:14px;">
      <input id="menuToggle" type="checkbox" />
      <label for="menuToggle" class="burger" aria-label="Open menu">
        <span></span><span></span><span></span>
      </label>
    </div>
  </div>

  <div class="center">
    <h1>Welcome to my lab</h1>
  </div>

  <!-- Red accents -->
  <div class="accents">
    <div class="line l1"></div>
    <div class="line l2"></div>
    <div class="line l3"></div>
    <div class="line l4"></div>
  </div>

  <!-- Drawer -->
  <div class="drawer">
    <a href="#about">About me</a>
    <a href="#projects">Projects</a>
    <a href="#contact">Contacto</a>
    <div class="hint">Tip: vuelve a presionar el botón para cerrar.</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)
