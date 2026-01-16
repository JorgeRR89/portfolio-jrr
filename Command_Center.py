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

/* Iframe alineado (como lo dejaste bien) */
iframe {
  width: calc(100vw - 64px) !important;
  height: 100vh !important;
  border: 0 !important;
  display: block !important;
  margin-left: 64px !important;
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
  width: calc(100vw - 24px);
  height: 100vh;
  margin-left: 24px;
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

/* Drawer buttons */
.drawer button {
  width: 100%;
  text-align: left;
  padding: 16px 14px;
  margin: 10px 0;
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 14px;
  background: transparent;
  color: #fff;
  cursor: pointer;
  font-weight: 800;
  letter-spacing: .5px;
  transition: background .2s ease, border-color .2s ease, transform .2s ease;
}

.drawer button:hover {
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

# =========================
# JS NAVEGACION (click + scroll)
# =========================
# IMPORTANTE:
# Estos links asumen tu estructura multipage:
# pages/1_About_Me.py, pages/2_Projects.py, pages/3_Contact.py
# Streamlit normalmente navega con ?page=<page_name_sin_.py>
js = """
<script>
(function () {
  function closeDrawer(){
    const t = document.getElementById('menuToggle');
    if (t) t.checked = false;
  }

  function goTo(page){
    // Construye URL para multipage de Streamlit
    // Ej: ?page=1_About_Me
    const base = window.parent.location.origin + window.parent.location.pathname;
    const url = base + "?page=" + encodeURIComponent(page);
    window.parent.location.href = url;
  }

  // Exponer funciones para onclick
  window.__nav = {
    about:  function(){ closeDrawer(); goTo("1_About_Me"); },
    projects:function(){ closeDrawer(); goTo("2_Projects"); },
    contact:function(){ closeDrawer(); goTo("3_Contact"); }
  };

  // Scroll-to-next: wheel down => About
  let armed = true;
  window.addEventListener("wheel", function(e){
    if (!armed) return;
    if (e.deltaY > 35) {
      armed = false;
      goTo("1_About_Me");
    }
  }, { passive: true });

  // Touch (mobile): swipe up => About
  let y0 = null;
  window.addEventListener("touchstart", (e)=>{ y0 = e.touches?.[0]?.clientY ?? null; }, {passive:true});
  window.addEventListener("touchmove", (e)=>{
    if (!armed || y0 === null) return;
    const y1 = e.touches?.[0]?.clientY ?? y0;
    const dy = y0 - y1; // swipe up => positive
    if (dy > 60) {
      armed = false;
      goTo("1_About_Me");
    }
  }, {passive:true});
})();
</script>
"""

html = f"""
{js}
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
    <button onclick="window.__nav.about()">About me</button>
    <button onclick="window.__nav.projects()">Projects</button>
    <button onclick="window.__nav.contact()">Contact</button>
    <div class="hint">Tip: presiona el botón para cerrar.</div>
  </div>
</div>
"""

components.html(css + html, height=1100, scrolling=False)
