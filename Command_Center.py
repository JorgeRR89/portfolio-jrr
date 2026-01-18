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
# (importante: no bloquear scroll)
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
# HERO + SECTIONS CSS
# =========================
css = """
<style>
* { box-sizing:border-box; }

/* IMPORTANTE: permitir scroll en la página */
html, body { background:#000; overflow-x:hidden; overflow-y:auto; }

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
  padding: 0 24px;
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

/* ===== BURGER MENU (details) ===== */
.menu {
  position:absolute;
  top:22px;
  right:28px;
  z-index:10000;
}

.menu summary { list-style:none; cursor:pointer; }
.menu summary::-webkit-details-marker { display:none; }

.burger {
  width:52px;
  height:52px;
  background:#ff2a2a;
  display:grid;
  place-items:center;
  box-shadow:0 10px 25px rgba(0,0,0,.25);
}

.burger span {
  display:block;
  width:22px;
  height:2px;
  background:#fff;
  margin:3px 0;
}

/* Drawer */
.drawer {
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
}

.menu[open] .drawer { transform:translateX(0%); }

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
}

.drawer a:hover {
  background:rgba(255,42,42,.18);
  border-color:rgba(255,42,42,.7);
}

/* Sections */
.section {
  width: calc(100vw - 64px);
  margin-left: 64px;
  padding: 72px 36px;
  font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
  color: rgba(255,255,255,0.92);
  background: #070709;
  border-top: 1px solid rgba(255,255,255,0.06);
}

.section h2 {
  margin: 0 0 14px 0;
  font-size: 2rem;
  letter-spacing: .2px;
}

.section p {
  margin: 0 0 14px 0;
  line-height: 1.7;
  font-size: 1.05rem;
  max-width: 980px;
  color: rgba(255,255,255,0.82);
}

.badges {
  display:flex;
  flex-wrap:wrap;
  gap:10px;
  margin-top: 18px;
}

.badge {
  border: 1px solid rgba(255,255,255,0.14);
  border-radius: 999px;
  padding: 8px 12px;
  font-weight: 700;
  font-size: .92rem;
  color: rgba(255,255,255,0.86);
}

.grid2 {
  display:grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
  margin-top: 18px;
  max-width: 980px;
}

.card {
  border: 1px solid rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.04);
  border-radius: 18px;
  padding: 18px 18px;
}

.card h3 { margin: 0 0 10px 0; }
.card ul { margin: 0; padding-left: 18px; color: rgba(255,255,255,0.82); }

@media (max-width: 900px) {
  .grid2 { grid-template-columns: 1fr; }
}
</style>
"""

logo_html = f"<img src='data:image/png;base64,{logo_b64}'>" if logo_b64 else ""

# =========================
# HTML (Hero + Sections)
# =========================
html = f"""
{css}

<div class="hero" id="home">

  <video autoplay muted loop playsinline>
    <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
  </video>

  <div class="overlay-dark"></div>

  <details class="menu">
    <summary class="burger" aria-label="Open menu">
      <span></span><span></span><span></span>
    </summary>

    <div class="drawer">
      <a href="#about" target="_self" rel="noopener">About me</a>
      <a href="#projects" target="_self" rel="noopener">Projects</a>
      <a href="#lab" target="_self" rel="noopener">Lab</a>
      <a href="#contact" target="_self" rel="noopener">Contact</a>
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

<!-- ===================== ABOUT ===================== -->
<div class="section" id="about">
  <h2>About me</h2>
  <p><b>Jorge Reyes — Engineer · Data Scientist · Technical Architect</b></p>

  <p>
    Construyo soluciones donde convergen <b>ingeniería, datos y sistemas complejos</b>.
    Mi trabajo se mueve entre la ejecución técnica real y el análisis profundo de cómo funcionan
    los sistemas — técnicos, industriales y sociales.
  </p>

  <p>
    Este portafolio es dos cosas al mismo tiempo: un <b>CV profesional</b> para reclutadores y un <b>laboratorio técnico</b>
    donde documento experimentos, modelos, simulaciones y aprendizaje aplicado.
  </p>

  <div class="badges">
    <div class="badge">Python</div>
    <div class="badge">Data Science</div>
    <div class="badge">Simulación / Monte Carlo</div>
    <div class="badge">Power BI</div>
    <div class="badge">Sistemas complejos</div>
  </div>

  <div class="grid2">
    <div class="card">
      <h3>Professional profile</h3>
      <p>
        Me especializo en convertir complejidad en estructura: modelar el sistema,
        entender sus dinámicas y proponer mejoras medibles con datos.
      </p>
      <ul>
        <li>Análisis, preparación y modelado de datos</li>
        <li>Dashboards y métricas accionables</li>
        <li>Optimización, simulación y escenarios</li>
        <li>Arquitectura y documentación técnica</li>
      </ul>
    </div>

    <div class="card">
      <h3>Social & political analysis (evidence-driven)</h3>
      <p>
        Además de lo técnico, desarrollo proyectos para <b>entender y mejorar sistemas sociales</b>:
        políticas públicas, regulación, incentivos y comportamiento colectivo.
        No desde ideología, sino desde <b>análisis estructural basado en evidencia</b>.
      </p>
      <ul>
        <li>Evaluación de impacto social y acceso a oportunidades</li>
        <li>Comportamiento electoral y opinión pública (patrones / sesgos)</li>
        <li>Modelos de incentivos: por qué las reglas crean resultados</li>
        <li>Simulación de escenarios y “policy trade-offs”</li>
      </ul>
    </div>
  </div>
</div>

<!-- ===================== PROJECTS (placeholder) ===================== -->
<div class="section" id="projects">
  <h2>Projects</h2>
  <p>
    Aquí irá el “hub” por industria (tarjetas por sector) leído desde <code>data/projects.yaml</code>.
    En el siguiente paso lo conectamos al YAML.
  </p>
</div>

<!-- ===================== LAB (placeholder) ===================== -->
<div class="section" id="lab">
  <h2>Lab</h2>
  <p>
    Aquí van experimentos técnicos, notebooks, prototipos, simulaciones y pruebas.
    (Podemos leerlos desde otro YAML o desde el mismo por tipo = lab.)
  </p>
</div>

<!-- ===================== CONTACT (placeholder) ===================== -->
<div class="section" id="contact">
  <h2>Contact</h2>
  <p>
    Correo · LinkedIn · GitHub (lo ponemos después)
  </p>
</div>
"""

st.markdown(html, unsafe_allow_html=True)
