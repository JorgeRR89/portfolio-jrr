import base64
from pathlib import Path
from urllib.parse import urlencode

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Portfolio JRR",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ASSETS = Path(__file__).parent / "assets"
VIDEO_PATH = ASSETS / "data-flow.mp4"
LOGO_PATH = ASSETS / "logo.png"
GIF_PATH = ASSETS / "idea.gif"



def b64_file(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")

video_b64 = b64_file(VIDEO_PATH) if VIDEO_PATH.exists() else ""
logo_b64 = b64_file(LOGO_PATH) if LOGO_PATH.exists() else ""
gif_b64 = b64_file(GIF_PATH) if GIF_PATH.exists() else ""

# limpia chrome
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

# routing
page = st.query_params.get("page", "")
if page == "about":
    st.switch_page("pages/1_About_Me.py")
elif page == "projects":
    st.switch_page("pages/2_Projects.py")
elif page == "contact":
    st.switch_page("pages/3_Contact.py")

# urls
about_url = "?" + urlencode({"page": "about"})
projects_url = "?" + urlencode({"page": "projects"})
contact_url = "?" + urlencode({"page": "contact"})

top_px = 25
logo_html = f"<img class='nav-logo' src='data:image/png;base64,{logo_b64}'/>" if logo_b64 else ""

app_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<style>
  html, body {{
    margin: 0;
    padding: 0;
    height: 100%;
    overflow: hidden;
    background: #000;
  }}

  /* VIDEO + overlay */
  .hero {{
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    background: #000;
    z-index: 1;
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
    z-index: 2;
    background: radial-gradient(ellipse at center,
      rgba(0,0,0,0.25),
      rgba(0,0,0,0.70) 55%,
      rgba(0,0,0,0.92) 100%);
  }}
  
/* FOCO IDEA */
.idea-focus {{
  position: fixed;
  top: 40%;
  right: 12%;
  transform: translateY(-50%);
  width: 220px;
  opacity: 0.92;
  z-index: 8000;
  pointer-events: none;

  filter: drop-shadow(0 0 25px rgba(0,180,255,0.75))
          drop-shadow(0 0 60px rgba(0,120,255,0.35));
}}
  /* NAV */
  .nav-wrap {{
    position: fixed;
    top: 40%;
    right: 11%;
    left: auto;
    transform: translateY(110px);
    z-index: 999999;   /* arriba del video */
   
  }}

  .nav-btn {{
    display: inline-flex;
    align-items: center;
    gap: 10px;
    height: 46px;
    padding: 0 14px;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.18);
    background: rgba(0,0,0,0.55);
    backdrop-filter: blur(14px);
    cursor: pointer;
    color: #fff;
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
  }}

  .nav-item:hover {{
    border-color: rgba(255,255,255,0.30);
    background: rgba(255,255,255,0.10);
  }}


  
</style>
</head>
<body>

  <div class="hero">
    {"<video autoplay muted loop playsinline><source src='data:video/mp4;base64," + video_b64 + "' type='video/mp4'></video>" if video_b64 else ""}
    <div class="overlay"></div>
   {"<img class='idea-focus' src='data:image/gif;base64," + gif_b64 + "'/>" if gif_b64 else ""}
 
  </div>

  <div class="nav-wrap">
    <button class="nav-btn" id="navBtn">
      {logo_html}
      <span class="nav-title">Portfolio JRR</span>
      <span class="nav-burger">≡</span>
    </button>

    <div class="nav-menu" id="navMenu">
      <a class="nav-item" href="{about_url}">About me</a>
      <a class="nav-item" href="{projects_url}">Projects</a>
      <a class="nav-item" href="{contact_url}">Contact</a>
    </div>
  </div>

<script>
  const btn = document.getElementById("navBtn");
  const menu = document.getElementById("navMenu");

  btn.addEventListener("click", (e) => {{
    e.preventDefault();
    e.stopPropagation();
    menu.classList.toggle("open");
  }});

  document.addEventListener("click", () => {{
    menu.classList.remove("open");
  }});

  document.addEventListener("keydown", (e) => {{
    if (e.key === "Escape") menu.classList.remove("open");
  }});
</script>

</body>
</html>
"""

# ⚠️ SOLO ESTE components.html debe existir
components.html(app_html, height=900, scrolling=False)

