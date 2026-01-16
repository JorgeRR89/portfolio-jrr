import base64
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


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
    st.error("No encuentro el video. Coloca tu archivo en: assets/hero.mp4")
    st.stop()


# =========================
# Make Streamlit page truly full-height
# (evita área blanca fuera del iframe)
# =========================
st.markdown(
    """
<style>
html, body {height: 100%;}
/* Quitar chrome y paddings */
header[data-testid="stHeader"] {display:none;}
footer {visibility:hidden;}
/*section[data-testid="stSidebar"] {display:none;}/*
.block-container { padding: 0 !important; max-width: 100% !important; }
section.main > div { padding: 0 !important; }

/* MUY IMPORTANTE: hacer que el iframe de components.html tenga alto de viewport */
iframe {
  width: 100% !important;
  height: 100vh !important;
  border: 0 !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# =========================
# CSS dentro del iframe
# =========================
css = """
<style>
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; height: 100%; background: #000; overflow: hidden; }

/* Hero wrapper */
.hero {
  position: relative;
  width: calc(100vw - 24px);  /* deja espacio para la flecha */
  height: 100vh;
  margin-left: 24px;          /* corre todo un poco a la derecha */
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

/* Dark overlay */
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

/* Logo con fondo blanco SOLO detrás */
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
  z-index: 5; /* arriba del overlay y de los acentos */
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

/* Red tech accents */
.accents {
  position: absolute;
  inset: 0;
  z-index: 4;
  pointer-events: none;
}

.line {
  position: absolute;
  height: 3px;
  background: #ff2a2a;
  opacity: 0.9;
}

.l1 { top: 92px; right: 130px; width: 120px; }
.l2 { top: 122px; right: 40px; width: 240px; }
.l3 { bottom: 70px; left: 40px; width: 220px; opacity: 0.55; }
.l4 { top: 30%; left: 55%; width: 250px; transform: rotate(-55deg); opacity: 0.50; }

/* ===== Burger + Drawer (checkbox hack) ===== */
#menuToggle { display: none; }

/* Burger button */
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

/* Animate burger to X */
#menuToggle:checked + label.burger span:nth-child(1) { transform: translateY(5px) rotate(45deg); }
#menuToggle:checked + label.burger span:nth-child(2) { opacity: 0; }
#menuToggle:checked + label.burger span:nth-child(3) { transform: translateY(-5px) rotate(-45deg); }

/* Drawer */
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

/* Open drawer when checked */
#menuToggle:checked ~ .drawer { transform: translateX(0%); }

/* Drawer links */
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
  transform: translateY(-1px);
}

.drawer .hint {
  opacity: 0.65;
  margin-top: 18px;
  font-size: 0.95rem;
}

@media (max-width: 600px) {
  .topbar { padding: 16px 16px; }
  .center h1 { font-size: 2.1rem; }
  .l1, .l2, .l3, .l4 { display: none; }
}
</style>
"""

logo_html = (
    f"<img src='data:image/png;base64,{logo_b64}' alt='logo' />" if logo_b64 else ""
)

html = f"""
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
      <input id="menuToggle" type="checkbox" />
      <label for="menuToggle" class="burger" aria-label="Open menu">
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
    <a href="#about">About me</a>
    <a href="#projects">Projects</a>
    <a href="#contact">Contacto</a>
    <div class="hint">Tip: presiona el botón para cerrar.</div>
  </div>
</div>
"""

# Render full screen
components.html(css + html, height=1100, scrolling=False)
