import streamlit as st

st.set_page_config(
    page_title="Projects",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================
# Corporate CSS
# =========================
st.markdown(
    """
<style>
.block-container{
  padding-top: 46px !important;
  padding-left: 56px !important;
  padding-right: 56px !important;
  max-width: 1500px !important;
}
h1, p { color: #fff; }
.muted { color: rgba(255,255,255,0.70); }

/* ====== Featured layout ====== */
.featured-grid{
  display:grid;
  grid-template-columns: 1.3fr 1fr;
  gap: 18px;
  margin-top: 22px;
}

/* Left big card */
.big-card{
  border-radius: 22px;
  overflow:hidden;
  border: 1px solid rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.03);
  backdrop-filter: blur(10px);
  min-height: 420px;
  position: relative;
  transition: transform 180ms ease, border-color 180ms ease, background 180ms ease;
}
.big-card:hover{
  transform: translateY(-4px);
  border-color: rgba(0,180,255,0.35);
  background: rgba(0,180,255,0.06);
}
.big-cover{
  height: 220px;
  background:
    radial-gradient(circle at 20% 20%, rgba(0,180,255,0.35), rgba(0,0,0,0) 55%),
    radial-gradient(circle at 80% 10%, rgba(0,120,255,0.25), rgba(0,0,0,0) 60%),
    linear-gradient(180deg, rgba(255,255,255,0.06), rgba(0,0,0,0));
  border-bottom: 1px solid rgba(255,255,255,0.08);
}
.big-content{ padding: 18px 18px 16px 18px; }
.big-title{ font-size: 22px; font-weight: 900; margin: 0; letter-spacing: 0.2px; }
.big-desc{ margin-top: 10px; font-size: 14px; line-height: 1.45; color: rgba(255,255,255,0.72); }
.pill{
  display:inline-block;
  margin-top: 12px;
  font-size: 12px;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.14);
  background: rgba(0,0,0,0.25);
  color: rgba(255,255,255,0.78);
}

/* Right 2x2 small cards */
.right-grid{
  display:grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}
.small-card{
  border-radius: 22px;
  overflow:hidden;
  border: 1px solid rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.03);
  backdrop-filter: blur(10px);
  min-height: 201px;
  position: relative;
  transition: transform 180ms ease, border-color 180ms ease, background 180ms ease;
}
.small-card:hover{
  transform: translateY(-4px);
  border-color: rgba(0,180,255,0.35);
  background: rgba(0,180,255,0.06);
}
.small-top{
  height: 78px;
  background:
    radial-gradient(circle at 25% 25%, rgba(0,180,255,0.28), rgba(0,0,0,0) 60%),
    linear-gradient(180deg, rgba(255,255,255,0.05), rgba(0,0,0,0));
  border-bottom: 1px solid rgba(255,255,255,0.08);
}
.small-content{ padding: 14px 14px 10px 14px; }
.small-title-row{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:10px;
}
.small-title{ font-size: 16px; font-weight: 880; margin: 0; }
.small-desc{ margin-top: 8px; font-size: 13px; line-height: 1.35; color: rgba(255,255,255,0.70); }
.icon{
  position:absolute;
  top: 54px;
  left: 14px;
  width: 42px;
  height: 42px;
  border-radius: 14px;
  background: rgba(0,0,0,0.40);
  border: 1px solid rgba(255,255,255,0.12);
  display:flex;
  align-items:center;
  justify-content:center;
  font-size: 20px;
  color:#fff;
  backdrop-filter: blur(10px);
}

/* Button */
.btn .stButton > button{
  width: 100%;
  border-radius: 14px !important;
  padding: 10px 12px !important;
  border: 1px solid rgba(255,255,255,0.12) !important;
  background: rgba(255,255,255,0.06) !important;
  color: #fff !important;
  font-weight: 780 !important;
}
.btn .stButton > button:hover{
  border-color: rgba(0,180,255,0.35) !important;
  background: rgba(0,180,255,0.10) !important;
}

/* Second row (3 cards) */
.second-row{
  display:grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
  margin-top: 18px;
}

/* Responsive */
@media (max-width: 1100px){
  .featured-grid{ grid-template-columns: 1fr; }
  .second-row{ grid-template-columns: 1fr; }
}
@media (max-width: 700px){
  .block-container{ padding-left: 18px !important; padding-right: 18px !important; }
  .right-grid{ grid-template-columns: 1fr; }
  .second-row{ grid-template-columns: 1fr; }
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown("# Projects")
st.markdown(
    "<p class='muted'>Industries / Case files (outcomes • links • demos). Select one to explore.</p>",
    unsafe_allow_html=True
)

# =========================
# Data (your real files)
# =========================
items = [
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
        "page": "pages/2c_Entretenimiento.py",
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

# =========================
# Featured section
# (1 big left + 4 right)
# =========================
featured_left = items[0]           # Bancos & Seguros (puedes cambiar)
right_four = items[1:5]           # Energía, Entretenimiento, Manufactura, Marketing
bottom_three = items[5:]          # Política, Transporte (y si falta 1, lo llenamos abajo)

st.markdown("<div class='featured-grid'>", unsafe_allow_html=True)

# Left big card (HTML) + button (streamlit)
st.markdown(
    f"""
    <div class="big-card">
      <div class="big-cover"></div>
      <div class="icon">{featured_left["icon"]}</div>
      <div class="big-content">
        <p class="big-title">{featured_left["name"]}</p>
        <span class="pill">{featured_left["tag"]}</span>
        <p class="big-desc">{featured_left["desc"]}</p>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
# Put a button aligned right under big card
colL, colR = st.columns([1, 1])
with colL:
    st.markdown("<div class='btn'>", unsafe_allow_html=True)
    if st.button("Open", key="open_left"):
        st.switch_page(featured_left["page"])
    st.markdown("</div>", unsafe_allow_html=True)

# Right grid container
st.markdown("<div class='right-grid'>", unsafe_allow_html=True)
for i, it in enumerate(right_four):
    st.markdown(
        f"""
        <div class="small-card">
          <div class="small-top"></div>
          <div class="icon">{it["icon"]}</div>
          <div class="small-content">
            <div class="small-title-row">
              <p class="small-title">{it["name"]}</p>
              <span class="pill">{it["tag"]}</span>
            </div>
            <p class="small-desc">{it["desc"]}</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div class='btn'>", unsafe_allow_html=True)
    if st.button("Open", key=f"open_right_{i}"):
        st.switch_page(it["page"])
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # close right-grid
st.markdown("</div>", unsafe_allow_html=True)  # close featured-grid

# =========================
# Second row (remaining)
# =========================
st.markdown("<div class='second-row'>", unsafe_allow_html=True)

# In case only 2 remain, we can add a placeholder card so layout stays symmetric
remaining = bottom_three
while len(remaining) < 3:
    remaining = remaining + [{
        "name": "Coming soon",
        "tag": "More • Industries",
        "desc": "Más industrias y case files se agregan pronto.",
        "icon": "✨",
        "page": None,
    }]

for j, it in enumerate(remaining[:3]):
    st.markdown(
        f"""
        <div class="small-card">
          <div class="small-top"></div>
          <div class="icon">{it["icon"]}</div>
          <div class="small-content">
            <div class="small-title-row">
              <p class="small-title">{it["name"]}</p>
              <span class="pill">{it["tag"]}</span>
            </div>
            <p class="small-desc">{it["desc"]}</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div class='btn'>", unsafe_allow_html=True)
    if it.get("page"):
        if st.button("Open", key=f"open_bottom_{j}"):
            st.switch_page(it["page"])
    else:
        st.button("Soon", key=f"soon_{j}", disabled=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


