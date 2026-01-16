import streamlit as st

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="Projects",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------
# Styles (Corporate 4x2 grid, equal cards)
# ----------------------------
st.markdown(
    """
<style>
header[data-testid="stHeader"] {display:none;}
footer {visibility:hidden;}
.block-container{
  padding-top: 46px !important;
  padding-left: 56px !important;
  padding-right: 56px !important;
  max-width: 1400px !important;
}

/* Titles */
h1{ color:#fff; margin-bottom: 8px; }
.subtitle{
  color: rgba(255,255,255,0.70);
  margin-top: 0;
}

/* ===== INDUSTRY GRID 4 x 2 ===== */
.industry-grid{
  display:grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
  margin-top: 26px;
}

.industry-card{
  position: relative;
  height: 260px;                 /* ✅ all same size */
  border-radius: 22px;
  border: 1px solid rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.035);
  backdrop-filter: blur(10px);
  overflow:hidden;
  transition: transform .2s ease, border-color .2s ease, background .2s ease;
}

.industry-card:hover{
  transform: translateY(-6px);
  border-color: rgba(0,180,255,0.45);
  background: rgba(0,180,255,0.08);
}

.industry-top{
  height: 92px;
  background:
    radial-gradient(circle at 25% 25%, rgba(0,180,255,0.28), rgba(0,0,0,0) 60%),
    radial-gradient(circle at 85% 10%, rgba(0,120,255,0.18), rgba(0,0,0,0) 55%),
    linear-gradient(180deg, rgba(255,255,255,0.05), rgba(0,0,0,0));
  border-bottom: 1px solid rgba(255,255,255,0.08);
}

.industry-icon{
  position:absolute;
  top: 54px;
  left: 16px;
  width: 46px;
  height: 46px;
  border-radius: 14px;
  background: rgba(0,0,0,0.45);
  border: 1px solid rgba(255,255,255,0.12);
  display:flex;
  align-items:center;
  justify-content:center;
  font-size: 22px;
  backdrop-filter: blur(10px);
}

.industry-body{
  padding: 16px;
}

.industry-title{
  margin:0;
  font-size:17px;
  font-weight:900;
  color:white;
}

.industry-tag{
  display:inline-block;
  margin-top:8px;
  font-size:12px;
  padding:6px 10px;
  border-radius:999px;
  border:1px solid rgba(255,255,255,0.14);
  background: rgba(0,0,0,0.28);
  color: rgba(255,255,255,0.8);
}

.industry-desc{
  margin-top:10px;
  font-size:13px;
  line-height:1.35;
  color: rgba(255,255,255,0.72);
  max-width: 95%;
}

.industry-open{
  position:absolute;
  bottom:14px;
  right:16px;
  font-size:12px;
  opacity:.85;
  color: rgba(255,255,255,0.78);
}

/* Make the entire card clickable via hidden link */
.card-link{
  position:absolute;
  inset:0;
  z-index: 2;
  text-decoration:none;
  color: transparent;
}

/* Responsive */
@media (max-width: 1200px){
  .industry-grid{ grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 650px){
  .block-container{ padding-left: 18px !important; padding-right: 18px !important; }
  .industry-grid{ grid-template-columns: 1fr; }
}
</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------
# Header
# ----------------------------
st.markdown("# Projects")
st.markdown(
    "<p class='subtitle'>Explore my work by industry. Case files, outcomes, links and demos will live inside each section.</p>",
    unsafe_allow_html=True,
)

# ----------------------------
# Data (your pages)
# NOTE: Entretenimiento is 3c_Entretenimiento.py per your repo screenshot.
# ----------------------------
industries = [
    {
        "name": "Bancos & Seguros",
        "tag": "Risk • Analytics",
        "desc": "Riesgo, fraude, segmentación, churn y dashboards ejecutivos.",
        "icon": "🏦",
        "page": "pages/2a_Bancos_Seguros.py",
    },
    {
        "name": "Energía",
        "tag": "Ops • Optimization",
        "desc": "Confiabilidad, mantenimiento, optimización y analítica operativa.",
        "icon": "⚡",
        "page": "pages/2b_Energia.py",
    },
    {
        "name": "Entretenimiento",
        "tag": "NLP • Recommenders",
        "desc": "Recomendación, engagement, sentiment y análisis de audiencia.",
        "icon": "🎬",
        "page": "pages/2c_Entretenimiento.py",
    },
    {
        "name": "Manufactura",
        "tag": "Quality • IoT",
        "desc": "OEE, calidad, procesos, mantenimiento predictivo e IoT industrial.",
        "icon": "🏭",
        "page": "pages/2d_Manufactura.py",
    },
    {
        "name": "Marketing",
        "tag": "Growth • BI",
        "desc": "Funnels, CAC/LTV, performance marketing y experimentación.",
        "icon": "📈",
        "page": "pages/2e_Marketing.py",
    },
    {
        "name": "Política",
        "tag": "Signals • Scenarios",
        "desc": "Señales, narrativa, percepción pública y escenarios.",
        "icon": "🏛️",
        "page": "pages/2f_Politica.py",
    },
    {
        "name": "Transporte",
        "tag": "Routing • Forecast",
        "desc": "Ruteo, demanda, costos y optimización logística.",
        "icon": "🚚",
        "page": "pages/2g_Transporte.py",
    },
    {
        "name": "Coming soon",
        "tag": "New Lab",
        "desc": "Nuevas industrias y casos en construcción.",
        "icon": "✨",
        "page": None,  # no navigation
    },
]

# ----------------------------
# Grid render (cards)
# We use HTML for the card UI + a Streamlit button overlay per-card for navigation.
# ----------------------------
st.markdown("<div class='industry-grid'>", unsafe_allow_html=True)

for i, it in enumerate(industries):
    # Card shell
    st.markdown(
        f"""
        <div class="industry-card">
          <div class="industry-top"></div>
          <div class="industry-icon">{it["icon"]}</div>
          <div class="industry-body">
            <p class="industry-title">{it["name"]}</p>
            <span class="industry-tag">{it["tag"]}</span>
            <p class="industry-desc">{it["desc"]}</p>
            <div class="industry-open">{'Open →' if it["page"] else 'Coming soon'}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Navigation: invisible-ish button per card (works reliably with Streamlit)
    # We place it right after the card; Streamlit will render below,
    # but visually the card is already corporate. Click via button under each card if you prefer.
    # If you want true "click anywhere", we can do JS routing next.
    if it["page"]:
        # compact button below each card (optional). Comment out if you don't want it.
        if st.button(f"Open {it['name']}", key=f"open_{i}"):
            st.switch_page(it["page"])
    else:
        st.button("Coming soon", key=f"soon_{i}", disabled=True)

st.markdown("</div>", unsafe_allow_html=True)

