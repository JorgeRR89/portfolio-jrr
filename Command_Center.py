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

ASSETS = Path(__file__).parent / "assets"
VIDEO_PATH = ASSETS / "data.mp4"
LOGO_PATH = ASSETS / "DS.png"


def b64_file(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")


video_b64 = b64_file(VIDEO_PATH) if VIDEO_PATH.exists() else ""
logo_b64 = b64_file(LOGO_PATH) if LOGO_PATH.exists() else ""

if not video_b64:
    st.error("No encuentro el video. Coloca tu archivo en: assets/data.mp4")
    st.stop()

# =========================
# FULL HEIGHT + ALIGNMENT
# =========================
st.markdown(
    """
<style>
html, body {height: 100%;}

/* Quitar chrome */
header[data-testid="stHeader"] {display:none;}
footer {visibility:hidden;}

/* Quitar paddings default */
.block-container { padding: 0 !important; max-width: 100% !important; }
section.main > div { padding: 0 !important; }
</style>
""",
    unsafe_allow_html=True,
)

# =========================
# CSS + HTML (YA NO IFRAME)
# =========================
css = """
<style>
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; height: 100%; background: #000; overflow: hidden; }

.hero {
  position: relative;
  width: calc(100vw - 64px);
  height: 100vh;
  margin-left: 64px;
  overflow: hidden;
  background: #000;
}

/* Video background */
.hero video {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: contrast(1.05) saturate(1.05);
  z-index: 0;
}

.overlay-dark {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.35);
  z-index: 1;
}

/* Top bar */
.topbar {
  position: absolute;
  top: 0; left: 0; right: 0;
  z-index: 6;
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
  font-weight: 800;
  letter-spacing: 1px;
  text-transform: uppercase;
  user-select: none;
}

.brand img {
  width: 36px;
  height: 36px;
  object-fit: contain;
  background: #fff;
  padding: 6px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.25);
}

/* Center headline */
.center {
  position: absolute;
  inset: 0;
  z-index: 5;
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
  font-weight: 900;
  text-shadow: 0 10px 30px rgba(0,0,0,0.55);
}

/* Tech accents */
.accents {
  position: absolute;
  inset: 0;
  z-index: 4;
  pointer-events: none;
}
.line { position: absolute; height: 3px; background: #ff2a2a; opacity: 0.9; }
.l1 { top: 92px; right: 130px; width: 120px; }
.l2 { top: 122px; right: 40px; width: 240px; }
.l3 { bottom: 70px; left: 40px; width: 220px; opacity: 0.55; }
.l4 { top: 30%; left: 55%; width: 250px; transform: rotate(-55deg); opacity: 0.50; }

/* Burger + Drawer */
#menuToggle { display: none; }

.burger {
  width: 52px;
  height: 52px;
  background: #ff2a2a;
  display: grid;
  place-items: center;
  cursor: pointer;
  box-shadow: 0 10px 25px rgba(0,0,0,0.25);
  user-select: none;
}
.burger span {
  display: block;
  width: 22px;
  height: 2px;
  background: #fff;
  margin: 3px 0;
  transition: transform .25s ease, opacity .25s ease;
}
#menuToggle:checked + label.burger span:nth-child(1) { transform: translateY(5px) rotate(45deg); }
#menuToggle:checked + label.burger span:nth-child(2) { opacity: 0; }
#menuToggle:checked + label.burger span:nth-child(3) { transform: translateY(-5px) rotate(-45deg); }

.drawer {
  position: absolute;
  top: 0;
  right: 0;
  width: min(380px, 90vw);
  height: 100%;
  z-index: 7;
  transform: translateX(110%);
  transition: transform .28s ease;
  background: rgba(10,10,12,0.92);
  backdrop-filter: blur(10px);
  border-left: 1px solid rgba(255,255,255,0.08);
  padding: 90px 28px 28px;
  color: #fff;
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
}
#menuToggle:checked ~ .drawer { transform: translateX(0%); }

.drawer a {
  display: block;
  padding: 16px 14px;
  margin: 10px 0;
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 14px;
  text-decoration: none;
  color: #fff;
  font-weight: 800;
  letter-spacing: .5px;
  transition: background .2s ease, border-color .2s ease, transform .2s ease;
}
.drawer a:hover {
  background: rgba(255,42,42,0.16);
  border-color: rgba(255,42,42,0.65);
