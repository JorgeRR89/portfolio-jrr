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
# Overlay UI styles
# ----------------------------
st.markdown(
    """
<style>
/* ====== SINGLE TOP-LEFT BUTTON: "Portfolio JRR ≡" ======
   Target the popover trigger by aria-label = the popover label.
   We'll label the popover exactly "Portfolio JRR".
/* ====== Portfolio JRR ≡  (single top button) ====== */

button[aria-label="Portfolio JRR"]{
  position: fixed !important;

  /* 🔽 AJUSTA ESTE VALOR si lo quieres más arriba o más abajo */
  top: 86px !important;      

  left: 22px !important;
  z-index: 100001 !important;

  height: 46px !important;
  padding: 0 16px !important;
  border-radius: 999px !important;

  border: 1px solid rgba(255,255,255,0.16) !important;
  background: rgba(0,0,0,0.55) !important;

  color: #fff !important;
  font-weight: 850 !important;
  letter-spacing: 0.3px !important;
  font-size: 15px !important;

  backdrop-filter: blur(14px);
}

/* ❌ Oculta flecha nativa del popover */
button[aria-label="Portfolio JRR"] svg{
  display: none !important;
}

/* 🍔 Burger icon */
button[aria-label="Portfolio JRR"]::after{
  content: "  ≡";
  color: #fff;
  font-size: 20px;
  font-weight: 950;
  letter-spacing: 2px;
}

/* Hover */
button[aria-label="Portfolio JRR"]:hover{
  border-color: rgba(255,255,255,0.32) !important;
  background: rgba(0,0,0,0.72) !important;
}


/* Add ≡ on the right inside the same button */
button[aria-label="Portfolio JRR"]::after{
  content: "  ≡";
  color: #fff;
  font-size: 18px;
  font-weight: 950;
}

/* Optional: logo inside the button (we'll inject via background if you want later) */
/* Hover */
button[aria-label="Portfolio JRR"]:hover{
  border-color: rgba(255,255,255,0.28) !important;
  background: rgba(0,0,0,0.58) !important;
}

/* Popover panel buttons (About/Projects/Contact) */
div[data-testid="stPopoverBody"] .stButton > button{
  width: 220px;
  border-radius: 12px !important;
  padding: 11px 12px !important;
  border: 1px solid rgba(255,255,255,0.14) !important;
  background: rgba(0,0,0,0.74) !important;
  color: #fff !important;
  font-weight: 780 !important;
  text-align: left !important;
}
div[data-testid="stPopoverBody"] .stButton > button:hover{
  border-color: rgba(255,255,255,0.30) !important;
  background: rgba(0,0,0,0.84) !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------
# SINGLE MENU: the brand itself is the menu trigger
# ----------------------------
with st.popover("Portfolio JRR"):
    if st.button("About me", key="cc_about"):
        st.switch_page("pages/3_About_Me.py")

    if st.button("Projects", key="cc_projects"):
        st.switch_page("pages/4_Projects.py")

    if st.button("Contact", key="cc_contact"):
        st.switch_page("pages/5_Contact.py")

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

