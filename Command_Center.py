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

# =========================
# ROUTING (HTML -> query param -> switch_page)
# =========================
go = st.query_params.get("go", None)

if go == "about":
    st.switch_page("pages/1_About_Me.py")
elif go == "projects":
    st.switch_page("pages/2_Projects.py")
elif go == "lab":
    st.switch_page("pages/4_Lab.py")
elif go == "contact":
    st.switch_page("pages/3_Contact.py")

# =========================
# ASSETS
# =========================
ASSETS = Path(__file__).parent / "assets"
VIDEO_PATH = ASSETS / "Data.mp4"  # <- usa tu nuevo recorte
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

/* Evita scrolls raros del contenedor principal */
[data-testid="stAppViewContainer"] { overflow: hidden; }
</style>
""",
    unsafe_allow_html=True,
)

# =========================
# HERO + MENU CSS (dentro del iframe)
# =========================
css = """
<style>
* { box-sizing:border-box; }
html, body { margin:0; padding:0; background:#000; height:100%; }

/* HERO: deja margen izquierdo para la flecha de Streamlit */
.hero{
  position:relative;
  width: calc(100vw - 64px);
  height: 100vh;
  margin-left: 64px;
  overflow:hidden;
  background:#000;
}

/* VIDEO */
.hero video{
  position:absolute;
  inset:0;
  width:100%;
  height:100%;
  object-fit:cover;
  z-index:0;
}

/* overlay */
.overlay-dark{
  position:absolute;
  inset:0;
  background:rgba(0,0,0,.35);
  z-index:1;
  pointer-events:none;
}

/* topbar */
.topbar{
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

.brand{
  display:flex;
  align-items:center;
  gap:12px;
  font-weight:800;
  letter-spacing:1px;
  text-transform:uppercase;
}

.brand img{
  width:36px;
  height:36px;
  object-fit:contain;
  background:#fff;
  padding:6px;
  border-radius:10px;
}

/* center text */
.center{
  position:absolute;
  inset:0;
  z-index:4;
  display:flex;
  align-items:center;
  justify-content:center;
  text-align:center;
  color:#fff;
  padding:0 24px;
  font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
}
.center h1{
  font-size:clamp(2.4rem,5vw,4.4rem);
  font-weight:900;
  margin:0;
  text-shadow:0 10px 30px rgba(0,0,0,.6);
}

/* accents */
.accents{ position:absolute; inset:0; z-index:3; pointer-events:none; }
.line{ position:absolute; height:3px; background:#ff2a2a; opacity:.9; }
.l1{ top:92px; right:130px; width:120px; }
.l2{ top:122px; right:40px; width:240px; }
.l3{ bottom:70px; left:40px; width:220px; opacity:.55; }
.l4{ top:30%; left:55%; width:250px; transform:rotate(-55deg); opacity:.5; }

/* ===== MENU: details/summary (sin JS) ===== */
.menu{
  position:absolute;
  top:22px;
  right:28px;
  z-index:10000;
}

/* ocultar marker default */
.menu summary{ list-style:none; cursor:pointer; }
.menu summary::-webkit-details-marker{ display:none; }

/* burger button */
.burger{
  width:52px;
  height:52px;
  background:#ff2a2a;
  display:grid;
  place-items:center;
  box-shadow:0 10px 25px rgba(0,0,0,.25);
  border-radius:0;  /* cuadrado como te gusta */
  position: relative;
  z-index: 10001; /* 👈 siempre clickeable para cerrar */
}

.burger span{
  display:block;
  width:22px;
  height:2px;
  background:#fff;
  margin:3px 0;
  transition:transform .25s ease, opacity .25s ease;
}

/* animación a X cuando está abierto */
.menu[open] .burger span:nth-child(1){ transform:translateY(5px) rotate(45deg); }
.menu[open] .burger span:nth-child(2){ opacity:0; }
.menu[open] .burger span:nth-child(3){ transform:translateY(-5px) rotate(-45deg); }

/* drawer */
.drawer{
  position:fixed;
  top:0;
  right:0;
  width:min(380px,90vw);
  height:100vh;
  background:rgba(10,10,12,.92);
  backdrop-filter:blur(10px);
  border-left:1px solid rgba(255,255,255,.08);
  padding:90px 28px 28px;
  transform:translateX(110%);
  transition:transform .28s ease;
  z-index:9999;
}

/* abre drawer */
.menu[open] .drawer{ transform:translateX(0); }

/* links */
.drawer a{
  display:block;
  padding:16px;
  margin:10px 0;
  border:1px solid rgba(255,255,255,.12);
  border-radius:14px;
  color:#fff;
  text-decoration:none;
  font-weight:800;
  letter-spacing:.5px;
}

.drawer a:hover{
  background:rgba(255,42,42,.18);
  border-color:rgba(255,42,42,.7);
}

/* responsive */
@media (max-width:600px){
  .topbar{ padding:16px 16px; }
  .l1,.l2,.l3,.l4{ display:none; }
}
</style>
"""

logo_html = f"<img src='data:image/png;base64,{logo_b64}' alt='logo'>" if logo_b64 else ""

about_link = "?go=about"
projects_link = "?go=projects"
lab_link = "?go=lab"
contact_link = "?go=contact"

html = f"""
<!doctype html>
<html>
<head>{css}</head>
<body>
  <div class="hero">
    <video autoplay muted loop playsinline preload="auto">
      <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
    </video>

    <div class="overlay-dark"></div>

    <details class="menu">
      <summary class="burger" aria-label="Open menu">
        <span></span><span></span><span></span>
      </summary>

      <div class="drawer">
        <a href="{about_link}" target="_self" rel="noopener">About me</a>
        <a href="{projects_link}" target="_self" rel="noopener">Projects</a>
        <a href="{lab_link}" target="_self" rel="noopener">Lab</a>
        <a href="{contact_link}" target="_self" rel="noopener">Contact</a>
      </div>
    </details>

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
</body>
</html>
"""

# Render como componente HTML (interacción estable)
components.html(html, height=1100, scrolling=False)
