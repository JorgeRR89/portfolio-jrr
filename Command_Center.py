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
VIDEO_PATH = ASSETS / "data-world.mp4"  # cambia aquí si tu video se llama distinto
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
</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------
# Hero video (full screen)
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
# UI Overlay styles
# ----------------------------
st.markdown(
    """
<style>
/* Top-left brand */
.ui-brand{
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
}
.ui-brand img{
  width: 22px;
  height: 22px;
  border-radius: 7px;
}

/* Burger top-right */
.ui-burger{
  position: fixed;
  top: 18px;
  right: 22px;
  z-index: 99999;
}
.ui-burger .stButton > button{
  width: 56px !important;
  height: 56px !important;
  border-radius: 16px !important;
  padding: 0 !important;
  border: 1px solid rgba(255,255,255,0.18) !important;
  background: rgba(0,0,0,0.50) !important;
  color: #fff !important;
  font-weight: 950 !important;
  font-size: 22px !important;
  backdrop-filter: blur(12px);
}
.ui-burger .stButton > button:hover{
  border-color: rgba(255,255,255,0.32) !important;
  background: rgba(0,0,0,0.72) !important;
}

/* Center CTA */
.ui-cta{
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 99999;
}
.ui-cta .stButton > button{
  border-radius: 999px !important;
  padding: 22px 40px !important;
  border: 1px solid rgba(255,255,255,0.25) !important;
  background: rgba(0,0,0,0.62) !important;
  color: #fff !important;
  font-weight: 950 !important;
  font-size: 18px !important;
  letter-spacing: 4.2px !important;
  text-transform: uppercase !important;
  backdrop-filter: blur(14px);
  box-shadow: 0 24px 90px rgba(0,0,0,0.65);
}
.ui-cta .stButton > button:hover{
  border-color: rgba(255,255,255,0.38) !important;
  background: rgba(0,0,0,0.78) !important;
  transform: translateY(-1px);
}

/* Dropdown menu panel */
.ui-menu{
  position: fixed;
  top: 84px;
  right: 22px;
  z-index: 99999;
  width: 220px;
  border-radius: 16px;
  padding: 10px;
  background: rgba(0,0,0,0.74);
  border: 1px solid rgba(255,255,255,0.14);
  backdrop-filter: blur(14px);
}
.ui-menu .stButton > button{
  width: 100%;
  border-radius: 12px !important;
  padding: 11px 12px !important;
  border: 1px solid rgba(255,255,255,0.14) !important;
  background: rgba(255,255,255,0.06) !important;
  color: #fff !important;
  font-weight: 780 !important;
}
.ui-menu .stButton > button:hover{
  border-color: rgba(255,255,255,0.30) !important;
  background: rgba(255,255,255,0.10) !important;
}

/* Prevent scroll bounce space */
html, body { overflow: hidden; }
</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------
# Brand (top-left)
# ----------------------------
brand_img = f"<img src='data:image/png;base64,{logo_b64}' />" if logo_b64 else ""
st.markdown(f"<div class='ui-brand'>{brand_img}Portfolio JRR</div>", unsafe_allow_html=True)

# ----------------------------
# Center CTA
# ----------------------------
st.markdown("<div class='ui-cta'>", unsafe_allow_html=True)
if st.button("WELCOME TO MY LAB", key="cc_cta"):
    st.switch_page("pages/1_Industries.py")
st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# Burger + menu
# ----------------------------
st.markdown("<div class='ui-burger'>", unsafe_allow_html=True)
if st.button("≡", key="cc_burger"):
    st.session_state["cc_menu_open"] = not st.session_state.get("cc_menu_open", False)
st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.get("cc_menu_open", False):
    st.markdown("<div class='ui-menu'>", unsafe_allow_html=True)

    if st.button("About", key="cc_about"):
        st.session_state["cc_menu_open"] = False
        st.switch_page("pages/3_About_Me.py")

    if st.button("Projects", key="cc_projects"):
        st.session_state["cc_menu_open"] = False
        st.switch_page("pages/4_Projects.py")

    if st.button("Contact", key="cc_contact"):
        st.session_state["cc_menu_open"] = False
        st.switch_page("pages/5_Contact.py")

    st.markdown("</div>", unsafe_allow_html=True)
