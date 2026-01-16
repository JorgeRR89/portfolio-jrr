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
/* Brand top-left */
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

/* --- FIX REAL: pin the popover trigger (burger) top-right --- */
div[data-testid="stPopover"] > button{
  position: fixed !important;
  top: 18px !important;
  right: 22px !important;
  left: auto !important;          /* clave: anula cualquier left */
  z-index: 100001 !important;     /* arriba del brand */

  width: 56px !important;
  height: 56px !important;
  border-radius: 16px !important;
  padding: 0 !important;

  border: 1px solid rgba(255,255,255,0.18) !important;
  background: rgba(0,0,0,0.50) !important;

  font-size: 0 !important;        /* oculta el texto del botón */
  color: transparent !important;
  backdrop-filter: blur(12px);
}

/* Trigger del popover (solo el botón que abre el menú) */
div[data-testid="stPopover"] > button{
  position: fixed !important;
  top: 18px !important;
  right: 22px !important;
  left: auto !important;
  z-index: 100001 !important;

  width: 56px !important;
  height: 56px !important;
  border-radius: 16px !important;
  padding: 0 !important;

  border: 1px solid rgba(255,255,255,0.18) !important;
  background: rgba(0,0,0,0.50) !important;

  font-size: 0 !important;        /* oculta "MENU" */
  color: transparent !important;
  backdrop-filter: blur(12px);
}

/* Icono ≡ SOLO en el trigger */
div[data-testid="stPopover"] > button::before{
  content: "≡";
  color: #fff;
  font-size: 22px;
  font-weight: 950;
}

/* Hover trigger */
div[data-testid="stPopover"] > button:hover{
  border-color: rgba(255,255,255,0.32) !important;
  background: rgba(0,0,0,0.72) !important;
}

/* Estilos para los botones dentro del panel del popover (NO fixed) */
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




/* icono ≡ via pseudo-element */
button[aria-label="MENU"]::before{
  content: "≡";
  color: #fff;
  font-size: 22px;
  font-weight: 950;
}

/* Hover */
button[aria-label="MENU"]:hover{
  border-color: rgba(255,255,255,0.32) !important;
  background: rgba(0,0,0,0.72) !important;
}

/* Estilo de botones dentro del popover */
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
# Brand (top-left)
# ----------------------------
brand_img = f"<img src='data:image/png;base64,{logo_b64}' />" if logo_b64 else ""
st.markdown(f"<div class='ui-brand'>{brand_img}Portfolio JRR</div>", unsafe_allow_html=True)

# ----------------------------
# Burger menu (top-right) using popover
# ----------------------------
with st.popover("MENU"):  # el texto se oculta por CSS y se muestra ≡
    if st.button("About me", key="cc_about"):
        st.switch_page("pages/3_About_Me.py")

    if st.button("Projects", key="cc_projects"):
        st.switch_page("pages/4_Projects.py")

    if st.button("Contact", key="cc_contact"):
        st.switch_page("pages/5_Contact.py")

# ----------------------------
# Hero video fullscreen (va al final; overlay sigue encima)
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
