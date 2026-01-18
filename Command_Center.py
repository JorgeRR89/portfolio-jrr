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
VIDEO_PATH = ASSETS / "data.mp4"
LOGO_PATH = ASSETS / "DS.png"


def b64_file(path: Path) -> str:
    return base64.encodebytes(path.read_bytes()).decode("utf-8")


video_b64 = b64_file(VIDEO_PATH) if VIDEO_PATH.exists() else ""
logo_b64 = b64_file(LOGO_PATH) if LOGO_PATH.exists() else ""

if not video_b64:
    st.error("No encuentro el video. Coloca tu archivo en: assets/data.mp4")
    st.stop()

# =========================
# GLOBAL CSS STREAMLIT
# =========================
st.markdown("""
<style>
html, body {height:100%; margin:0;}
header[data-testid="stHeader"] {display:none;}
footer {visibility:hidden;}
.block-container { padding:0 !important; max-width:100% !important; }
section.main > div { padding:0 !important; }
</style>
""", unsafe_allow_html=True)

# =========================
# HERO + MENU CSS
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
  z-index:6;
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

/* BURGER */
#menuToggle { display:none; }

.burger {
  position:absolute;
  top:22px;
  right:28px;
  width:52px;
  height:52px;
  background:#ff2a2a;
  display:grid;
  place-items:center;
  box-shadow:0 10px 25px rgba(0,0,0,.25);
  z-index:10001;
  cursor:pointer;
}

.burger span {
  display:block;
  width:22px;
  height:2px;
  background:#fff;
  margin:3px 0;
}

/* DRAWER */
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
  z-index:10000;
}

#menuToggle:checked ~ .drawer {
  transform:translateX(0%);
}

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
</style>
"""

logo_html = f"<img src='data:image/png;base64,{logo_b64}'>" if logo_b64 else ""

about_link = "?go=about"
projects_link = "?go=projects"
lab_link = "?go=lab"
contact_link = "?go=contact"

html = f"""
{css}
<div class="hero">

  <input type="checkbox" id="menuToggle"/>

  <label for="menuToggle" class="burger" aria-label="Open menu">
    <span></span><span></span><span></span>
  </label>

  <video autoplay muted loop playsinline>
    <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
  </video>

  <div class="overlay-dark"></div>

  <div class="drawer">
    <a href="{about_link}" target="_self">About me</a>
    <a href="{projects_link}" target="_self">Projects</a>
    <a href="{lab_link}" target="_self">Lab</a>
    <a href="{contact_link}" target="_self">Contact</a>
  </div>

  <div class="topbar">
    <div class="brand">
      {logo_html}
      <div>Portfolio JRR</div>
    </div>
  </div>

  <div class="center">
    <h1>Welcome to my lab</h1>
  </div>

</div>
"""

st.markdown(html, unsafe_allow_html=True)
