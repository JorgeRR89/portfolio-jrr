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
# ROUTING (query param -> switch_page)
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
# PATHS
# =========================
ASSETS = Path(__file__).parent / "assets"
VIDEO_PATH = ASSETS / "data.mp4"
LOGO_PATH = ASSETS / "DS.png"

if not VIDEO_PATH.exists():
    st.error("No encuentro el video. Colócalo en: assets/data.mp4")
    st.stop()

# =========================
# GLOBAL CSS (full screen)
# =========================
st.markdown("""
<style>
html, body {height:100%; margin:0;}
header[data-testid="stHeader"] {display:none;}
footer {visibility:hidden;}
.block-container { padding:0 !important; max-width:100% !important; }
section.main > div { padding:0 !important; }

/* Hacemos que el contenedor del video sea full screen */
div[data-testid="stVideo"] video {
  width: calc(100vw - 64px) !important;
  height: 100vh !important;
  object-fit: cover !important;
  margin-left: 64px !important;
  border-radius: 0 !important;
}

/* Quitamos padding raro alrededor de st.video */
div[data-testid="stVideo"] {
  margin: 0 !important;
  padding: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# VIDEO (servido por Streamlit, NO base64)
# =========================
st.video(str(VIDEO_PATH), autoplay=True, loop=True, muted=True)

# =========================
# OVERLAY + MENU HTML (ligero)
# =========================
logo_html = ""
if LOGO_PATH.exists():
    import base64
    logo_b64 = base64.b64encode(LOGO_PATH.read_bytes()).decode("utf-8")
    logo_html = f"<img src='data:image/png;base64,{logo_b64}'>"

css = """
<style>
/* Capa overlay encima del video */
.hero-overlay{
  position: fixed;
  top: 0; left: 0;
  width: 100vw;
  height: 100vh;
  pointer-events: none;
  z-index: 50;
}

/* Oscurecer */
.overlay-dark{
  position:absolute;
  inset:0;
  background: rgba(0,0,0,0.35);
}

/* Topbar */
.topbar{
  position:absolute;
  top:0; left:64px; right:0;
  display:flex;
  justify-content:space-between;
  align-items:center;
  padding:22px 28px;
  color:#fff;
  font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
  pointer-events:auto;
  z-index: 60;
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
  background:#fff;
  padding:6px;
  border-radius:10px;
}

/* Center text */
.center{
  position:absolute;
  inset:0;
  display:flex;
  justify-content:center;
  align-items:center;
  text-align:center;
  color:#fff;
  pointer-events:none;
}
.center h1{
  font-size:clamp(2.4rem,5vw,4.4rem);
  font-weight:900;
  margin:0;
  text-shadow:0 10px 30px rgba(0,0,0,0.6);
}

/* Burger + drawer */
#menuToggle{display:none;}
.burger{
  width:52px; height:52px;
  background:#ff2a2a;
  display:grid; place-items:center;
  box-shadow:0 10px 25px rgba(0,0,0,.25);
  cursor:pointer;
}
.burger span{
  display:block;
  width:22px; height:2px;
  background:#fff;
  margin:3px 0;
}
.drawer{
  position:fixed;
  top:0; right:0;
  width:min(380px,90vw);
  height:100vh;
  background:rgba(10,10,12,.92);
  backdrop-filter: blur(10px);
  border-left:1px solid rgba(255,255,255,.08);
  padding:90px 28px 28px;
  transform:translateX(110%);
  transition:transform .3s ease;
  z-index: 70;
  pointer-events:auto;
}
#menuToggle:checked ~ .drawer{transform:translateX(0%);}
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
</style>
"""

about_link = "?go=about"
projects_link = "?go=projects"
lab_link = "?go=lab"
contact_link = "?go=contact"

html = f"""
{css}
<div class="hero-overlay">
  <div class="overlay-dark"></div>

  <div class="topbar">
    <div class="brand">{logo_html}<div>Portfolio JRR</div></div>

    <input type="checkbox" id="menuToggle"/>
    <label for="menuToggle" class="burger" aria-label="Open menu">
      <span></span><span></span><span></span>
    </label>

    <div class="drawer">
      <a href="{about_link}" target="_self">About me</a>
      <a href="{projects_link}" target="_self">Projects</a>
      <a href="{lab_link}" target="_self">Lab</a>
      <a href="{contact_link}" target="_self">Contact</a>
    </div>
  </div>

  <div class="center">
    <h1>Welcome to my lab</h1>
  </div>
</div>
"""

st.markdown(html, unsafe_allow_html=True)
