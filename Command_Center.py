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
# GLOBAL CSS
# =========================
st.markdown(
    """
<style>
html, body {height: 100%; margin:0;}

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
# CSS DEL HERO + MENU
# =========================
css = """
<style>
* { box-sizing: border-box; }
html, body { background: #000; overflow: hidden; }

/* HERO */
.hero {
  position: relative;
  width: calc(100vw - 64px);
  height: 100vh;
  margin-left: 64px;
  overflow: hidden;
  background: #000;
}

/* VIDEO */
.hero video {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: contrast(1.05) saturate(1.05);
  z-index: 0;
}

/* OVERLAY */
.overlay-dark {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.35);
  z-index: 1;
}

/* TOP BAR */
.topbar {
  position: absolute;
  top: 0; left: 0; right: 0;
  z-index: 6;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 22px 28px;
  color: #fff;
  font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 800;
  letter-spacing: 1px;
  text-transform: uppercase;
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

/* CENTER TEXT */
.center {
  position: absolute;
  inset: 0;
  z-index: 5;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #fff;
}

.center h1 {
  font-size: clamp(2.4rem, 5vw, 4.4rem);
  font-weight: 900;
  margin: 0;
  text-shadow: 0 10px 30px rgba(0,0,0,0.6);
}

/* TECH ACCENTS */
.accents { position:absolute; inset:0; z-index:4; pointer-events:none; }
.line { position:absolute; height:3px; background:#ff2a2a; opacity:.9; }
.l1 { top:92px; right:130px; width:120px; }
.l2 { top:122px; right:40px; width:240px; }
.l3 { bottom:70px; left:40px; width:220px; opacity:.55; }
.l4 { top:30%; left:55%; width:250px; transform:rotate(-55deg); opacity:.5; }

/* BURGER + DRAWER */
#menuToggle { display:none; }

.burger {
  width: 52px;
  height: 52px;
  background: #ff2a2a;
  display: grid;
  place-items: center;
  cursor: pointer;
  box-shadow: 0 10px 25px rgba(0,0,0,0.25);
}

.burger span {
  display:block;
  width:22px;
  height:2px;
  background:white;
  margin:3px 0;
  transition:.25s;
}

#menuToggle:checked + label span:nth-child(1){transform:translateY(5px) rotate(45deg);}
#menuToggle:checked + label span:nth-child(2){opacity:0;}
#menuToggle:checked + label span:nth-child(3){transform:translateY(-5px) rotate(-45deg);}

.drawer {
  position:absolute;
  top:0;
  right:0;
  width:min(380px,90vw);
  height:100%;
  background:rgba(10,10,12,.92);
  backdrop-filter: blur(10px);
  border-left:1px solid rgba(255,255,255,.08);
  padding:90px 28px;
  transform:translateX(110%);
  transition:.3s ease;
  z-index:7;
}

#menuToggle:checked ~ .drawer { transform:translateX(0%); }

.drawer a {
  display:block;
  padding:16px;
  margin:10px 0;
  border:1px solid rgba(255,255,255,.12);
  border-radius:14px;
  color:white;
  text-decoration:none;
  font-weight:800;
  letter-spacing:.5px;
  transition:.2s;
}

.drawer a:hover {
  background:rgba(255,42,42,.18);
  border-color:rgba(255,42,42,.7);
  transform:translateY(-1px);
}
</style>
"""

logo_html = f"<img src='data:image/png;base64,{logo_b64}' />" if logo_b64 else ""

# LINKS A TUS PAGINAS MULTIPAGE
about_link = "?page=1_About_Me"
projects_link = "?page=2_Projects"
contact_link = "?page=3_Contact"

html = f"""
{css}
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

    <div>
      <input id="menuToggle" type="checkbox">
      <label for="menuToggle" class="burger">
        <span></span><span></span><span></span>
      </label>
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

  <div class="drawer">
    <a href="{about_link}">About me</a>
    <a href="{projects_link}">Projects</a>
    <a href="{contact_link}">Contact</a>
  </div>
</div>
"""

st.markdown(html, unsafe_allow_html=True)

