import streamlit as st
from pathlib import Path
import base64

st.set_page_config(
    page_title="Portfolio JRR",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ASSETS = Path(__file__).parent / "assets"
VIDEO_PATH = ASSETS / "mundo-red-datos.mp4"   # <-- aquí va tu video final
BG_IMG_PATH = ASSETS / "nodes_bg.png" # <-- opcional: imagen estática de nodos
LOGO_PATH = ASSETS / "logo.png"       # <-- opcional: logo mini

# ----------------- CSS -----------------
st.markdown("""
<style>
header[data-testid="stHeader"] {display:none;}
footer {visibility:hidden;}
.block-container{padding-top:28px !important;}

:root{
  --bg:#000;
  --card:#ffffff;
  --text:#0b0f14;
  --muted:#5b6675;
  --border:rgba(0,0,0,0.10);
  --shadow: 0 18px 70px rgba(0,0,0,0.55);
}

/* Full-screen hero wrapper */
.hero-wrap{
  position: relative;
  width: 100%;
  min-height: 86vh;
  border-radius: 26px;
  overflow: hidden;
  background: var(--bg);
  border: 1px solid rgba(255,255,255,0.08);
}

/* Background video */
.hero-wrap video{
  position:absolute;
  inset:0;
  width:100%;
  height:100%;
  object-fit:cover;
  opacity:0.70;
  filter: contrast(1.05) saturate(0.9);
}

/* Background image fallback */
.hero-bg-img{
  position:absolute;
  inset:0;
  width:100%;
  height:100%;
  object-fit:cover;
  opacity:0.65;
}

/* Dark overlay to make center card pop */
.hero-overlay{
  position:absolute;
  inset:0;
  background: radial-gradient(ellipse at 50% 35%,
    rgba(0,0,0,0.15),
    rgba(0,0,0,0.78) 55%,
    rgba(0,0,0,0.92) 100%);
}

/* Center card */
.command-card{
  position:absolute;
  top:50%;
  left:50%;
  transform: translate(-50%, -52%);
  width: min(1100px, 92%);
  background: var(--card);
  border-radius: 26px;
  box-shadow: var(--shadow);
  border: 1px solid var(--border);
  padding: 26px 28px 26px 28px;
}

/* Card top bar */
.card-top{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:12px;
  padding-bottom: 10px;
}
.brand{
  display:flex;
  align-items:center;
  gap:10px;
  font-weight: 750;
  color: var(--text);
}
.brand img{
  width: 26px; height: 26px; border-radius: 8px;
}
.nav{
  display:flex; gap:18px; align-items:center;
  color: var(--muted);
  font-weight: 600;
  font-size: 14px;
}
.burger{
  width: 38px; height: 38px;
  border-radius: 999px;
  display:flex; align-items:center; justify-content:center;
  border: 1px solid rgba(0,0,0,0.10);
  color: var(--text);
}

/* Card body */
.card-body{
  padding: 34px 12px 8px 12px;
  display:flex;
  flex-direction: column;
  align-items: center;
  text-align:center;
}
.kicker{
  letter-spacing: 2.6px;
  font-size: 12px;
  color: var(--muted);
  font-weight: 700;
}
.h1{
  margin-top: 10px;
  font-size: 56px;
  line-height: 1.02;
  font-weight: 850;
  color: var(--text);
}
.sub{
  margin-top: 14px;
  max-width: 760px;
  font-size: 17px;
  line-height: 1.45;
  color: rgba(11,15,20,0.80);
}
.cta{
  margin-top: 22px;
  display:flex;
  gap:12px;
  justify-content:center;
  flex-wrap: wrap;
}
.pill{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  padding: 11px 16px;
  border-radius: 999px;
  border: 1px solid rgba(0,0,0,0.12);
  font-weight: 700;
  color: var(--text);
  background: rgba(0,0,0,0.02);
}
.pill.primary{
  background: #0B0F14;
  color: #fff;
  border-color: #0B0F14;
}

/* Footer hint inside card */
.card-foot{
  margin-top: 26px;
  padding-top: 14px;
  border-top: 1px solid rgba(0,0,0,0.08);
  display:flex;
  justify-content:space-between;
  color: rgba(11,15,20,0.55);
  font-size: 12px;
  font-weight: 600;
}

/* Industries section */
.section-title{
  margin-top: 18px;
  font-size: 18px;
  font-weight: 780;
}
</style>
""", unsafe_allow_html=True)

# ----------------- Helpers -----------------
def _b64_file(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")

# ----------------- HERO -----------------
st.markdown('<div class="hero-wrap">', unsafe_allow_html=True)

# Background: video if exists, else image if exists, else nothing
if VIDEO_PATH.exists():
    b64 = _b64_file(VIDEO_PATH)
    st.markdown(
        f"""
        <video autoplay muted loop playsinline>
          <source src="data:video/mp4;base64,{b64}" type="video/mp4">
        </video>
        """,
        unsafe_allow_html=True,
    )
elif BG_IMG_PATH.exists():
    # If you upload assets/nodes_bg.png it will be shown as fallback
    b64img = _b64_file(BG_IMG_PATH)
    st.markdown(
        f'<img class="hero-bg-img" src="data:image/png;base64,{b64img}" />',
        unsafe_allow_html=True,
    )

st.markdown('<div class="hero-overlay"></div>', unsafe_allow_html=True)

# Brand logo inside card (optional)
logo_html = ""
if LOGO_PATH.exists():
    b64logo = _b64_file(LOGO_PATH)
    logo_html = f'<img src="data:image/png;base64,{b64logo}" />'

# Command Card HTML
st.markdown(
    f"""
<div class="command-card">
  <div class="card-top">
    <div class="brand">
      {logo_html}
      <span>Portfolio JRR</span>
    </div>
    <div class="nav">
      <span>About</span>
      <span>Projects</span>
      <span>Contact</span>
      <div class="burger">☰</div>
    </div>
  </div>

  <div class="card-body">
    <div class="kicker">COMMAND CENTER</div>
    <div class="h1">WELCOME TO MY LAB</div>
    <div class="sub">
      Engineering futuristic intelligence systems — predictive models, simulation engines, and decision frameworks
      across critical industries.
    </div>

    <div class="cta">
      <span class="pill primary">Enter the Lab</span>
      <span class="pill">Open Simulation Lab</span>
    </div>

    <div class="card-foot">
      <span>Intelligence • Engineering • Systems</span>
      <span>Scroll ↓</span>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)

# ----------------- UNDER HERO: industries preview + real buttons -----------------
st.write("")  # spacing

# Real navigation buttons (Streamlit actions)
b1, b2, b3 = st.columns([0.22, 0.22, 0.56])
with b1:
    if st.button("Enter the Lab", use_container_width=True):
        # We'll create pages later; for now keep it on the home or route to Industries
        try:
            st.switch_page("pages/1_Industries.py")
        except Exception:
            st.warning("Industries page not created yet.")
with b2:
    if st.button("Open Simulation Lab", use_container_width=True):
        try:
            st.switch_page("pages/2_Simulation_Lab.py")
        except Exception:
            st.warning("Simulation Lab page not created yet.")

st.markdown('<div class="section-title">Strategic Domains</div>', unsafe_allow_html=True)
st.caption("Organized like IBM Solutions — projects grouped by industry.")

industries = [
    ("Finance • Banking • Insurance", "Risk modeling, anomaly detection, forecasting, decision engines."),
    ("Sports Analytics", "Simulation, scenario testing, performance & market signals."),
    ("Energy", "Demand forecasting, operational optimization, anomaly detection."),
    ("Manufacturing", "Quality analytics, predictive maintenance, process optimization."),
    ("Healthcare", "Risk prediction, operational intelligence, pattern detection."),
    ("Transportation & Logistics", "Route optimization, ETA forecasting, supply-chain intelligence."),
    ("Politics & Public Systems", "Sentiment, information signals, scenario modeling."),
    ("Marketing & Growth", "Segmentation, uplift/propensity, attribution, demand intelligence."),
]

cols = st.columns(4)
for i, (name, desc) in enumerate(industries):
    with cols[i % 4]:
        st.markdown(
            f"""
            <div style="
              border:1px solid rgba(255,255,255,0.10);
              border-radius:16px;
              padding:14px 14px 12px 14px;
              background: rgba(255,255,255,0.03);
              min-height: 92px;">
              <div style="font-weight:760; margin-bottom:6px;">{name}</div>
              <div style="opacity:0.82; font-size:12.5px; line-height:1.35;">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
