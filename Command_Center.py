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

logo_html = f"<img src='data:image/png;base64,{logo_b64}' alt='logo'/>" if logo_b64 else ""

# =========================
# ONE-PAGE HTML (NO JS)
# =========================
html = f"""
<style>
* {{ box-sizing:border-box; }}
html, body {{ background:#000; margin:0; padding:0; }}
/* permite scroll de pagina */
body {{ overflow-y:auto; }}

/* ===== HERO ===== */
.hero {{
  position: relative;
  width: calc(100vw - 64px);
  height: 100vh;
  margin-left: 64px;
  overflow: hidden;
  background: #000;
}}

/* Video */
.hero video {{
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 0;
}}

/* Overlay */
.overlay-dark {{
  position:absolute;
  inset:0;
  background:rgba(0,0,0,0.35);
  z-index:1;
  pointer-events:none;
}}

/* Topbar */
.topbar {{
  position:absolute;
  top:0; left:0; right:0;
  z-index:5;
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:22px 28px;
  color:#fff;
  font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
}}

.brand {{
  display:flex;
  align-items:center;
  gap:12px;
  font-weight:800;
  letter-spacing:1px;
  text-transform:uppercase;
}}

.brand img {{
  width:36px;
  height:36px;
  object-fit:contain;
  background:#fff;
  padding:6px;
  border-radius:10px;
  box-shadow:0 4px 12px rgba(0,0,0,0.25);
}}

/* Center text */
.center {{
  position:absolute;
  inset:0;
  z-index:4;
  display:flex;
  align-items:center;
  justify-content:center;
  text-align:center;
  color:#fff;
  padding:0 24px;
}}

.center h1 {{
  font-size:clamp(2.4rem,5vw,4.4rem);
  font-weight:900;
  margin:0;
  text-shadow:0 10px 30px rgba(0,0,0,0.6);
}}

/* accents */
.accents {{ position:absolute; inset:0; z-index:3; pointer-events:none; }}
.line {{ position:absolute; height:3px; background:#ff2a2a; opacity:.9; }}
.l1 {{ top:92px; right:130px; width:120px; }}
.l2 {{ top:122px; right:40px; width:240px; }}
.l3 {{ bottom:70px; left:40px; width:220px; opacity:.55; }}
.l4 {{ top:30%; left:55%; width:250px; transform:rotate(-55deg); opacity:.5; }}

/* ===== Burger + Drawer (checkbox hack) ===== */
#navToggle {{ display:none; }}

.burger {{
  width:52px;
  height:52px;
  background:#ff2a2a;
  display:grid;
  place-items:center;
  cursor:pointer;
  box-shadow:0 10px 25px rgba(0,0,0,.25);
}}

.burger span {{
  display:block;
  width:22px;
  height:2px;
  background:#fff;
  margin:3px 0;
  transition:.25s ease;
}}

#navToggle:checked + label.burger span:nth-child(1) {{ transform:translateY(5px) rotate(45deg); }}
#navToggle:checked + label.burger span:nth-child(2) {{ opacity:0; }}
#navToggle:checked + label.burger span:nth-child(3) {{ transform:translateY(-5px) rotate(-45deg); }}

/* Drawer fixed */
.drawer {{
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
  transition:transform .3s ease;
  z-index:9999;
}}

#navToggle:checked ~ .drawer {{ transform:translateX(0%); }}

.drawer a {{
  display:block;
  padding:16px;
  margin:10px 0;
  border:1px solid rgba(255,255,255,.12);
  border-radius:14px;
  color:#fff;
  text-decoration:none;
  font-weight:800;
  letter-spacing:.5px;
}}

.drawer a:hover {{
  background:rgba(255,42,42,.18);
  border-color:rgba(255,42,42,.7);
  transform:translateY(-1px);
  transition:.2s;
}}

/* ===== Cerrar drawer SIN JS al navegar a secciones =====
   Como el drawer está DESPUÉS de las secciones en el DOM,
   podemos ocultarlo cuando una sección es :target.
*/
#about:target ~ .drawer,
#projects:target ~ .drawer,
#lab:target ~ .drawer,
#contact:target ~ .drawer {{
  transform:translateX(110%) !important;
}}

/* ===== Sections ===== */
.section {{
  width: calc(100vw - 64px);
  margin-left: 64px;
  padding: 90px 28px;
  background: #0b0b0d;
  color: #fff;
  font-family: system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
  border-top: 1px solid rgba(255,255,255,0.06);
}}

.section h2 {{
  margin: 0 0 14px 0;
  font-size: 2rem;
}}

.section p {{
  margin: 0;
  opacity: 0.75;
  max-width: 900px;
  line-height: 1.6;
}}

@media (max-width:600px) {{
  .hero {{ width: 100vw; margin-left: 0; }}
  .section {{ width: 100vw; margin-left: 0; }}
}}
</style>

<div class="hero">
<video autoplay muted loop playsinline>
<source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
</video>

<div class="overlay-dark"></div>

<!-- Checkbox + burger (toggle) -->
<input id="navToggle" type="checkbox">
<label for="navToggle" class="burger" aria-label="Open menu" style="position:absolute; top:22px; right:28px; z-index:10000;">
<span></span><span></span><span></span>
</label>

<div class="topbar">
<div class="brand">
{logo_html}
<div>Portfolio JRR</div>
</div>
<div></div>
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

<!-- ===== SECTIONS (one-page) ===== -->
<div id="about" class="section">
<h2>About me</h2>
<p>Aquí va tu mezcla 50/50: CV profesional (reclutadores) + laboratorio técnico (proyectos, experimentos, mindset).</p>
</div>

<div id="projects" class="section">
<h2>Projects</h2>
<p>Aquí vamos a leer data/projects.yaml y mostrar industrias como bloques (cards). Al abrir una industria, listamos sus proyectos.</p>
</div>

<div id="lab" class="section">
<h2>Lab</h2>
<p>Esta sección es para tu “laboratorio”: notebooks, demos, prototipos, simulaciones, artículos técnicos, etc.</p>
</div>

<div id="contact" class="section">
<h2>Contact</h2>
<p>Email, LinkedIn, GitHub, y un mini formulario (si quieres) en la siguiente iteración.</p>
</div>

<!-- Drawer VA AL FINAL para poder cerrarlo con :target -->
<div class="drawer">
<a href="#about">About me</a>
<a href="#projects">Projects</a>
<a href="#lab">Lab</a>
<a href="#contact">Contact</a>
</div>
"""

st.markdown(html, unsafe_allow_html=True)
