import base64
from pathlib import Path
from urllib.parse import urlencode

import streamlit as st
import streamlit.components.v1 as components

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="Portfolio JRR",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------
# Paths
# ----------------------------
ASSETS = Path(__file__).parent / "assets"
VIDEO_PATH = ASSETS / "data-world.mp4"
LOGO_PATH = ASSETS / "logo.png"  # opcional

def b64_file(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")

video_b64 = b64_file(VIDEO_PATH) if VIDEO_PATH.exists() else ""
logo_b64 = b64_file(LOGO_PATH) if LOGO_PATH.exists() else ""

# ----------------------------
# Clean Streamlit chrome
# ----------------------------
st.markdown(
    """
<style>
header[data-testid="stHeader"] {display:none;}
footer {visibility:hidden;}
.block-container { padding: 0 !important; max-width: 100% !important; }
section.main > div { padding: 0 !important; }
div[data-testid="stVerticalBlock"] { gap: 0rem; }
</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------
# Routing via query params (stable navigation)
# ----------------------------
params = st.query_params
page = params.get("page", "")

if page == "about":
    st.switch_page("pages/3_About_Me.py")
elif page == "projects":
    st.switch_page("pages/4_Projects.py")
elif page == "contact":
    st.switch_page("pages/5_Contact.py")

# ----------------------------
# Topbar HTML (Portfolio JRR ≡ + burger dropdown)
# ----------------------------
top_px = 72  # <-- AJUSTA AQUÍ: lo baja/sube a la altura del video

logo_html = f"<img class='nav-logo' src='data:image/png;base64,{logo_b64}'/>" if logo_b64 else ""

# Links (query params)
about_url = "?" + urlencode({"page": "about"})
projects_url = "?" + urlencode({"page": "projects"})
contact_url = "?" + urlencode({"page": "contact"})

nav_html = f"""
<div class="nav-wrap">
  <button class="nav-btn" id="navBtn" aria-label="Portfolio JRR">
    {logo_html}
    <span class="nav-title">Portfolio JRR</span>
    <span class="nav-burger">≡</span>
  </button>

  <div class="nav-menu" id="navMenu" role="menu">
    <a class="nav-item" href="{about_url}">About me</a>
    <a class="nav-item" href="{projects_url}">Projects</a>
    <a class="nav-item" href="{contact_url}">Contact</a>
  </div>
</div>

<style>
  .nav-wrap {{
    position: fixed;
    top: {top_px}px;
    left: 22px;
    z-index: 999999;
    user-select: none;
  }}

  .nav-btn {{
    display: inline-flex;
    align-items: center;
    gap: 10px;
    height: 46px;
    padding: 0 14px;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.16);
    background: rgba(0,0,0,0.55);
    backdrop-filter: blur(14px);
    cursor: pointer;
  }}

  .nav-logo {{
    width: 22px;
    height: 22px;
    border-radius: 7px;
  }}

  .nav-title {{
    color: #fff;
    font-weight: 850;
    letter-spacing: 0.3px;
    font-size: 15px;
  }}

  .nav-burger {{
    color: #fff;
    font-weight: 950;
    font-size: 20px;
    letter-spacing: 2px;
    padding-left: 2px;
  }}

  .nav-btn:hover {{
    border-color: rgba(255,255,255,0.32);
    background: rgba(0,0,0,0.72);
  }}

  .nav-menu {{
    display: none;
    margin-top: 10px;
    width: 240px;
    border-radius: 16px;
    padding: 10px;
    background: rgba(0,0,0,0.74);
    border: 1px solid rgba(255,255,255,0.14);
    backdrop-filter: blur(14px);
  }}

  .nav-menu.open {{
    display: block;
  }}

  .nav-item {{
    display: block;
    width: 100%;
    padding: 11px 12px;
    margin: 8px 0;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.14);
    background: rgba(255,255,255,0.06);
    color: #fff;
    font-weight: 780;
    text-decoration: none;
    text-align: left;
  }}

  .nav-item:hover {{
    border-color: rgba(255,255,255,0.30);
    background: rgba(255,255,255,0.10);
  }}
</style>

<script>
  const btn = document.getElementById("navBtn");
  const menu = document.getElementById("navMenu");

  function toggleMenu(e) {{
    e.preventDefault();
    e.stopPropagation();
    menu.classList.toggle("open");
  }}

  function closeMenu() {{
    menu.classList.remove("open");
  }}

  btn.addEventListener("click", toggleMenu);
  document.addEventListener("click", closeMenu);
  document.addEventListener("keydown", (e) => {{
    if (e.key === "Escape") closeMenu();
  }});
</script>
"""

components.html(nav_html, height=180, scrolling=False)

# ----------------------------
# Hero video fullscreen
# ----------------------------
hero_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<style>
  html, body {{
    margin: 0;
    padding: 0;
    background: transparent;
    height: 100%;
    overflow: hidden;
  }}
  .hero {{
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100vh;
    background: #000;
    overflow: hidden;
  }}
  video {{
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }}
  .overlay {{
    position: absolute;
    inset: 0;
    background:
      radial-gradient(ellipse at center,
        rgba(0,0,0,0.25),
        rgba(0,0,0,0.70) 55%,
        rgba(0,0,0,0.92) 100%);
  }}
</style>
</head>
<body>
  <div class="hero">
    {"<video autoplay muted loop playsinline><source src='data:video/mp4;base64," + video_b64 + "' type='video/mp4'></video>" if video_b64 else ""}
    <div class="overlay"></div>
  </div>
</body>
</html>
"""
components.html(hero_html, height=900, scrolling=False)
