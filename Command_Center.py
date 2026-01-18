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
# GLOBAL CSS STREAMLIT
# =========================
st.markdown(
    """
<style>
html, body {height:100%; margin:0;}
header[data-testid="stHeader"] {display:none;}
footer {visibility:hidden;}
.block-container { padding:0 !important; max-width:100% !important; }
section.main > div { padding:0 !important; }
</style>
""",
    unsafe_allow_html=True,
)

# =========================
# HERO + MENU + SECTIONS CSS (NO JS)
# =========================
css = """
<style>
* { box-sizing:border-box; }
html, body { background:#000; overflow-y:auto; }

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
  z-index: 0;
}

/* OVERLAY */
.overlay-dark {
  position:absolute;
  inset:0;
  background:rgba(0,0,0,0.35);
  z-index:1;
  pointer-events:none;
}

/* TOP BAR */
.topbar {
  position:absolute;
  top:0; left:0; right:0;
  z-index:5;
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:22px 28px;
  color:#fff;
  font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
}

.brand {
  display:flex;
  align-items:center;
  gap:12px;
  font-weight:800;
  letter-spacing:1px;
  text-transform:uppercase;
}

.brand img {
  width:36px;
  height:36px;
  background:#fff;
  padding:6px;
  border-radius:10px;
}

/* CENTER */
.center {
  position:absolute;
  inset:0;
  z-index:4;
  display:flex;
  align-items:center;
  justify-content:center;
  text-align:center;
  color:white;
}

.center h1 {
  font-size:clamp(2.4rem,5vw,4.4rem);
  font-weight:900;
  margin:0;
  text-shadow:0 10px 30px rgba(0,0,0,0.6);
}

/* ACCENTS */
.accents { position:absolute; inset:0; z-index:3; pointer-events:none; }
.line { position:absolute; height:3px; background:#ff2a2a; opacity:.9; }
.l1 { top:92px; right:130px; width:120px; }
.l2 { top:122px; right:40px; width:240px; }
.l3 { bottom:70px; left:40px; width:220px; opacity:.55; }
.l4 { top:30%; left:55%; width:250px; transform:rotate(-55deg); opacity:.5; }

/* =========================
   MENU (Checkbox hack)
========================= */

/* checkbox oculto */
#navToggle {
  position: fixed;
  opacity: 0;
  pointer-events: none;
}

/* Burger button (abre/cierra) */
.burger {
  position: fixed;
  top: 22px;
  right: 28px;
  z-index: 10000;
  width:52px;
  height:52px;
  background:#ff2a2a;
  display:grid;
  place-items:center;
  box-shadow:0 10px 25px rgba(0,0,0,.25);
  cursor: pointer;
  user-select:none;
}

.burger span {
  display:block;
  width:22px;
  height:2px;
  background:#fff;
  margin:3px 0;
  transition: .25s ease;
}

/* animación a X cuando está abierto */
#navToggle:checked + label.burger span:nth-child(1){transform:translateY(5px) rotate(45deg);}
#navToggle:checked + label.burger span:nth-child(2){opacity:0;}
#navToggle:checked + label.burger span:nth-child(3){transform:translateY(-5px) rotate(-45deg);}

/* Drawer */
.drawer {
  position: fixed;
  top:0;
  right:0;
  width:min(380px,90vw);
  height:100vh;
  background:rgba(10,10,12,.92);
  backdrop-filter:blur(10px);
  border-left:1px solid rgba(255,255,255,.08);
  padding:90px 28px 28px;
  transform:translateX(110%);
  transition:transform .3s ease;
  z-index:9999;
}

/* abrir drawer cuando checkbox checked */
#navToggle:checked ~ .drawer { transform:translateX(0%); }

/* Items del drawer: usamos label para cerrar, y dentro va el link */
.drawer .nav-item {
  display:block;
  margin:10px 0;
  cursor:pointer;
  user-select:none;
}

/* estilo del link/botón */
.drawer .nav-item a {
  display:block;
  padding:16px;
  border:1px solid rgba(255,255,255,.12);
  border-radius:14px;
  color:white;
  text-decoration:none;
  font-weight:800;
  letter-spacing:.5px;
}

.drawer .nav-item a:hover {
  background:rgba(255,42,42,.18);
  border-color:rgba(255,42,42,.7);
}

/* SECTIONS */
.section {
  width: calc(100vw - 64px);
  margin-left: 64px;
  padding: 70px 28px;
  color: #fff;
  font-family: system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
  border-top: 1px solid rgba(255,255,255,0.06);
  background: #060607;
}

.anchor { position:relative; top:-90px; }
</style>
"""

logo_html = f"<img src='data:image/png;base64,{logo_b64}'>" if logo_b64 else ""

about_link = "#about"
projects_link = "#projects"
contact_link = "#contact"

html = f"""
{css}

<!-- ✅ Control del menú -->
<input id="navToggle" type="checkbox" />

<!-- ✅ Burger (mismo botón abre/cierra) -->
<label for="navToggle" class="burger" aria-label="Toggle menu">
  <span></span><span></span><span></span>
</label>

<!-- ✅ Drawer (se abre/cierra por CSS) -->
<div class="drawer">
  <!-- ✅ Cada item es LABEL (cierra) + A (scroll) -->
  <label for="navToggle" class="nav-item">
    <a href="{about_link}">About me</a>
  </label>

  <label for="navToggle" class="nav-item">
    <a href="{projects_link}">Projects</a>
  </label>

  <label for="navToggle" class="nav-item">
    <a href="{contact_link}">Contact</a>
  </label>
</div>

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

<div id="about" class="anchor"></div>
<section class="section"><h2>About me</h2></section>

<div id="projects" class="anchor"></div>
<section class="section"><h2>Projects</h2></section>

<div id="contact" class="anchor"></div>
<section class="section"><h2>Contact</h2></section>
"""

st.markdown(html, unsafe_allow_html=True)
