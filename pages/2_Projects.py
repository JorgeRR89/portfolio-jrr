import streamlit as st

st.set_page_config(
    page_title="Projects",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------
# ROUTING via query params (click cards -> go=subpage)
# ----------------------------
go = st.query_params.get("go", "")
ROUTES = {
    "bancos": "pages/2a_Bancos_Seguros.py",
    "energia": "pages/2b_Energia.py",
    "entretenimiento": "pages/2c_Entretenimiento.py",
    "manufactura": "pages/2d_Manufactura.py",
    "marketing": "pages/2e_Marketing.py",
    "politica": "pages/2f_Politica.py",
    "transporte": "pages/2g_Transporte.py",
}

if go in ROUTES:
    st.query_params.clear()
    st.switch_page(ROUTES[go])

# ----------------------------
# Styles (single-grid 4x2)
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
  max-width: 1500px !important;
}

h1{ color:#fff; margin-bottom: 8px; }
.subtitle{ color: rgba(255,255,255,0.70); margin-top: 0; }

/* ===== 4 x 2 grid (ALL SAME SIZE) ===== */
.industry-grid{
  display:grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
  margin-top: 26px;
}

/* Card */
.industry-card{
  position: relative;
  height: 260px;
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
  color: #fff;
  backdrop-filter: blur(10px);
  z-index: 2;
}

.industry-body{ padding: 16px; }
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
}
.industry-open{
  position:absolute;
  bottom:14px;
  right:16px;
  font-size:12px;
  opacity:.85;
  color: rgba(255,255,255,0.78);
}

/* Make whole card clickable */
.cardlink{
  position:absolute;
  inset:0;
  z-index: 1;
  text-decoration:none !important;
  color: transparent !important;
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
    "<p class='subtitle'>8 industry blocks • same size • 4 columns × 2 rows.</p>",
    unsafe_allow_html=True,
)

# ----------------------------
# DATA (8 blocks)
# ----------------------------
cards = [
    # name, tag, desc, icon, go_key
    ("Bancos & Seguros", "Risk • Analytics", "Riesgo, fraude, segmentación, churn y KPIs.", "🏦", "bancos"),
    ("Energía", "Ops • Optimization", "Confiabilidad, mantenimiento, optimización.", "⚡", "energia"),
    ("Entretenimiento", "NLP • Recommenders", "Audiencias, recomendación, sentimiento.", "🎬", "entretenimiento"),
    ("Manufactura", "Quality • IoT", "OEE, calidad, defectos, predicción.", "🏭", "manufactura"),
    ("Marketing", "Growth • BI", "Funnels, CAC/LTV, performance, testing.", "📈", "marketing"),
    ("Política", "Signals • Scenarios", "Narrativa, percepción, escenarios.", "🏛️", "politica"),
    ("Transporte", "Routing • Forecast", "Ruteo, demanda, costos, logística.", "🚚", "transporte"),
    ("Coming soon", "New Lab", "Más industrias y case files en construcción.", "✨", ""),  # no click
]

# ----------------------------
# RENDER: SINGLE HTML BLOCK (this is the key)
# ----------------------------
html = ["<div class='industry-grid'>"]

for name, tag, desc, icon, key in cards:
    link = f"?go={key}" if key else "#"
    open_text = "Open →" if key else "Coming soon"

    html.append(f"""
    <div class="industry-card">
      {"<a class='cardlink' href='" + link + "'></a>" if key else ""}
      <div class="industry-top"></div>
      <div class="industry-icon">{icon}</div>
      <div class="industry-body">
        <p class="industry-title">{name}</p>
        <span class="industry-tag">{tag}</span>
        <p class="industry-desc">{desc}</p>
        <div class="industry-open">{open_text}</div>
      </div>
    </div>
    """)

html.append("</div>")

st.markdown("".join(html), unsafe_allow_html=True)

