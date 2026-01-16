import streamlit as st

st.set_page_config(
    page_title="Projects",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ====== CSS ======
st.markdown(
    """
<style>
.block-container{
  padding-top: 46px !important;
  padding-left: 56px !important;
  padding-right: 56px !important;
  max-width: 1400px !important;
}
h1, p { color: #fff; }
.muted { color: rgba(255,255,255,0.70); }

/* Grid */
.grid{
  display:grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 18px;
  margin-top: 22px;
}

/* Card */
.card{
  grid-column: span 4;
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.03);
  backdrop-filter: blur(10px);
  transition: transform 180ms ease, border-color 180ms ease, background 180ms ease;
  min-height: 220px;
  position: relative;
}
.card:hover{
  transform: translateY(-4px);
  border-color: rgba(0,180,255,0.35);
  background: rgba(0,180,255,0.06);
}

/* Top visual area (fake cover) */
.cover{
  height: 92px;
  background: radial-gradient(circle at 20% 20%, rgba(0,180,255,0.35), rgba(0,0,0,0) 55%),
              radial-gradient(circle at 80% 10%, rgba(0,120,255,0.25), rgba(0,0,0,0) 60%),
              linear-gradient(180deg, rgba(255,255,255,0.06), rgba(0,0,0,0));
  border-bottom: 1px solid rgba(255,255,255,0.08);
}

/* Content */
.content{
  padding: 14px 16px 14px 16px;
}
.title-row{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap: 10px;
}
.title{
  font-size: 18px;
  font-weight: 850;
  margin: 0;
  letter-spacing: 0.2px;
}
.tag{
  font-size: 12px;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.14);
  background: rgba(0,0,0,0.25);
  color: rgba(255,255,255,0.78);
  white-space: nowrap;
}
.desc{
  margin-top: 10px;
  color: rgba(255,255,255,0.72);
  font-size: 14px;
  line-height: 1.35;
}

/* Icon bubble */
.icon{
  position:absolute;
  top: 58px;
  left: 16px;
  width: 44px;
  height: 44px;
  border-radius: 14px;
  background: rgba(0,0,0,0.40);
  border: 1px solid rgba(255,255,255,0.12);
  display:flex;
  align-items:center;
  justify-content:center;
  font-size: 20px;
  color: #fff;
  backdrop-filter: blur(10px);
}

/* Button */
.card-btn .stButton > button{
  width: 100%;
  border-radius: 14px !important;
  padding: 10px 12px !important;
  border: 1px solid rgba(255,255,255,0.12) !important;
  background: rgba(255,255,255,0.06) !important;
  color: #fff !important;
  font-weight: 780 !important;
}
.card-btn .stButton > button:hover{
  border-color: rgba(0,180,255,0.35) !important;
  background: rgba(0,180,255,0.10) !important;
}

/* Responsive */
@media (max-width: 1100px){ .card{ grid-column: span 6; } }
@media (max-width: 700px){
  .block-container{ padding-left: 18px !important; padding-right: 18px !important; }
  .card{ grid-column: span 12; }
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown("# Projects")
st.markdown("<p class='muted'>Select an industry to explore case files, outcomes, links and demos.</p>", unsafe_allow_html=True)

# ====== IMPORTANT: update to YOUR real filenames ======
INDUSTRIES = [
    {
        "name": "Bancos & Seguros",
        "tag": "Risk • Analytics",
        "desc": "Riesgo, fraude, segmentación, churn y KPIs ejecutivos.",
        "icon": "🏦",
        "page": "pages/2a_Bancos_Seguros.py",
    },
    {
        "name": "Energía",
        "tag": "Ops • Optimization",
        "desc": "Optimización, confiabilidad, monitoreo y analítica operativa.",
        "icon": "⚡",
        "page": "pages/2b_Energia.py",
    },
    {
        "name": "Entretenimiento",
        "tag": "NLP • Recommenders",
        "desc": "Recomendación, engagement, sentiment y análisis de audiencia.",
        "icon": "🎬",
        "page": "pages/2c_Entretenimiento.py",  # <- según tu screenshot
    },
    {
        "name": "Manufactura",
        "tag": "Quality • IoT",
        "desc": "Calidad, OEE, mantenimiento predictivo e IoT industrial.",
        "icon": "🏭",
        "page": "pages/2d_Manufactura.py",
    },
    {
        "name": "Marketing",
        "tag": "Growth • BI",
        "desc": "Funnels, CAC/LTV, performance, atribución y experimentación.",
        "icon": "📈",
        "page": "pages/2e_Marketing.py",
    },
    {
        "name": "Política",
        "tag": "Signals • Scenarios",
        "desc": "Discurso, percepción pública, señales tempranas y escenarios.",
        "icon": "🏛️",
        "page": "pages/2f_Politica.py",
    },
    {
        "name": "Transporte",
        "tag": "Routing • Forecast",
        "desc": "Demanda, ruteo, costos y optimización logística.",
        "icon": "🚚",
        "page": "pages/2g_Transporte.py",
    },
]

st.markdown("<div class='grid'>", unsafe_allow_html=True)

for i, it in enumerate(INDUSTRIES):
    st.markdown(
        f"""
        <div class="card">
          <div class="cover"></div>
          <div class="icon">{it["icon"]}</div>
          <div class="content">
            <div class="title-row">
              <p class="title">{it["name"]}</p>
              <span class="tag">{it["tag"]}</span>
            </div>
            <p class="desc">{it["desc"]}</p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='card-btn'>", unsafe_allow_html=True)
    if st.button("Open", key=f"open_{i}"):
        st.switch_page(it["page"])
    st.markdown("</div></div></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

