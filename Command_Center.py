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
VIDEO_PATH = ASSETS / "coding1.mp4"
LOGO_PATH = ASSETS / "logo.png"


def b64_file(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")


video_b64 = b64_file(VIDEO_PATH) if VIDEO_PATH.exists() else ""
logo_b64 = b64_file(LOGO_PATH) if LOGO_PATH.exists() else ""

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

logo_html = f"<img class='nav-logo' src='data:image/png;base64,{logo_b64}'/>" if logo_b64 else ""

app_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />

<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;800&display=swap');

  :root {{
    --code-font: "JetBrains Mono", "Fira Code", "Source Code Pro", monospace;
  }}

  html, body {{
    margin: 0;
    padding: 0;
    height: 100%;
    overflow: hidden;
    background: #000;
    font-family: var(--code-font);
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

  /* wrapper para rotar sin romper el video */
  .video-tilt {{
    position: absolute;
    inset: -10%;
    transform: rotate(-2deg) scale(1.12);
    transform-origin: center;
    z-index: 1;
  }}

  .video-tilt video {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    filter: contrast(1.05) brightness(0.95);
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

  /* NAV */
  .nav-wrap {{
    position: fixed;
    top: 5%;
    right: 14.5%;
    left: auto;
    transform: translate(-4px, 150px);
    z-index: 999999;
    width: 260px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }}

  .nav-title {{
    font-family: var(--code-font);
    font-weight: 800;
    color: #eaf6ff;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    white-space: nowrap;
  }}

  .cursor {{
    display: inline-block;
    width: 10px;
    height: 18px;
    border-radius: 2px;
    background: rgba(143, 211, 255, 0.95);
    box-shadow: 0 0 10px rgba(0,160,255,.8);
    animation: blink 0.95s steps(1) infinite;
  }}

  @keyframes blink {{
    50% {{ opacity: 0; }}
  }}

  .nav-btn {{
    width: 260px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    height: 50px;
    padding: 0 22px;
    border-radius: 999px;

    font-family: var(--code-font);
    font-weight: 800;
    font-size: 15px;
    letter-spacing: 0.4px;

    color: #eaf6ff;
    cursor: pointer;

    background: linear-gradient(
      180deg,
      rgba(0,120,255,0.18),
      rgba(0,0,0,0.85)
    );

    border: 1px solid rgba(120,190,255,0.65);

    box-shadow:
      0 0 0 1px rgba(120,190,255,0.4),
      0 0 14px rgba(0,140,255,0.45),
      inset 0 0 18px rgba(0,120,255,0.25);

    backdrop-filter: blur(14px);
    transition: all .25s ease;
  }}

  .nav-btn:hover {{
    box-shadow:
      0 0 0 1px rgba(140,210,255,0.9),
      0 0 22px rgba(0,160,255,0.75),
      inset 0 0 22px rgba(0,140,255,0.35);
    transform: translateY(-1px) scale(1.02);
  }}

  .nav-logo {{
    width: 22px;
    height: 22px;
    border-radius: 7px;
  }}

  .nav-burger {{
    font-family: var(--code-font);
    font-weight: 900;
    font-size: 18px;
    color: #8fd3ff;
    text-shadow: 0 0 8px rgba(0,160,255,.8);
  }}

  .nav-menu {{
    display: none;
    margin-top: 14px;
    width: 260px;
    border-radius: 16px;
    padding: 12px;

    background: linear-gradient(
      180deg,
      rgba(8,14,22,0.95),
      rgba(0,0,0,0.85)
    );

    border: 1px solid rgba(120,190,255,0.35);

    box-shadow:
      0 0 24px rgba(0,120,255,0.35),
      inset 0 0 22px rgba(0,90,180,0.15);

    backdrop-filter: blur(18px);
  }}

  .nav-menu.open {{
    display: block;
  }}

  .nav-item {{
    display: block;
    width: 100%;
    padding: 13px 14px;
    margin: 10px 0;
    border-radius: 12px;

    font-family: var(--code-font);
    font-weight: 700;
    font-size: 14px;
    letter-spacing: 0.3px;
    text-align: center;

    color: #e9f4ff;
    text-decoration: none;

    background: linear-gradient(
      180deg,
      rgba(255,255,255,0.06),
      rgba(255,255,255,0.02)
    );

    border: 1px solid rgba(255,255,255,0.12);
    transition: all .2s ease;
  }}

  .nav-item:hover {{
    background: linear-gradient(
      180deg,
      rgba(0,140,255,0.25),
      rgba(0,60,140,0.18)
    );

    border-color: rgba(120,200,255,0.75);

    box-shadow:
      inset 0 0 18px rgba(0,120,255,0.35),
      0 0 16px rgba(0,140,255,0.55);

    transform: scale(1.03);
  }}
</style>
</head>

<body>
  <div class="hero">
    <div class="video-tilt">
      {"<video autoplay muted loop playsinline><source src='data:video/mp4;base64," + video_b64 + "' type='video/mp4'></video>" if video_b64 else ""}
    </div>
    <div class="overlay"></div>
  </div>

  <div class="nav-wrap">
    <button class="nav-btn" id="navBtn">
      {logo_html}
      <span class="nav-title">
        <span id="typedTitle"></span><span class="cursor"></span>
      </span>
      <span class="nav-burger">≡</span>
    </button>

    <div class="nav-menu" id="navMenu">
      <a class="nav-item" href="{about_url}">About me</a>
      <a class="nav-item" href="{projects_url}">Projects</a>
      <a class="nav-item" href="{contact_url}">Contact</a>
    </div>
  </div>

<script>
  // ---- MENU toggle ----
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

  // ---- TYPING effect ----
  const target = document.getElementById("typedTitle");
  const text = "Portfolio JRR";
  let i = 0;

  function type() {{
    if (i <= text.length) {{
      target.textContent = text.slice(0, i);
      i++;
      setTimeout(type, 65);
    }}
  }}
  type();
</script>

</body>
</html>
"""

components.html(app_html, height=900, scrolling=False)
