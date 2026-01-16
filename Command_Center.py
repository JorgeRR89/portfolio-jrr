import base64
from pathlib import Path

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
VIDEO_PATH = ASSETS / "data-world.mp4"  # cambia el nombre si tu video es otro
LOGO_PATH = ASSETS / "logo.png"           # opcional

# ----------------------------
# Helpers
# ----------------------------
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
/* remove Streamlit padding so it feels like a website */
.block-container { padding: 0 !important; max-width: 100% !important; }
section.main > div { padding: 0 !important; }
/* avoid gaps */
div[data-testid="stVerticalBlock"] { gap: 0rem; }
</style>
""",
    unsafe_allow_html=True,
)

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

# ----------------------------
# Brand (top-left)
# ----------------------------
brand_img = f"<img src='data:image/png;base64,{logo_b64}' />" if logo_b64 else ""
st.markdown(
    f"""
<style>
.ui-brand{{
  position: fixed;
  top: 18px;
  left: 22px;
  z-index: 99999;
  display:flex;
  align-items:center;
  gap:10px;
  padding: 10px 14px;
  border-radius: 999px;
  background: rgba(0,0,0,0.40);
  border: 1px solid rgba(255,255,255,0.14);
  color: #fff;
  font-weight: 850;
  letter-spacing: 0.2px;
  backdrop-filter: blur(12px);
}}
.ui-brand img{{
  width: 22px;
  height: 22px;
  border-radius: 7px;
}}
</style>
<div class="ui-brand">{brand_img}Portfolio JRR</div>
""",
    unsafe_allow_html=True,
)
