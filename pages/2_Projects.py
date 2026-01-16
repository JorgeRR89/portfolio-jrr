import streamlit as st

st.set_page_config(page_title="Projects", page_icon="🛰️", layout="wide")

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
.muted{ color: rgba(255,255,255,0.70); }

/* ===== Featured Solutions Layout (like your reference image) ===== */
.solutions{
  display:grid;
  grid-template-columns: 1.45fr 1fr 1fr;
  gap: 16px;
  margin-top: 18px;
}

/* Left big card spans 2 rows */
.solutions .big{
  grid-row: span 2;
  border-radius: 22px;
  overflow:hidden;
  border: 1px solid rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.03);
  backdrop-filter: blur(10px);
  min-height: 520px;
  position: relative;
  transition: transform 180ms ease, border-color 180ms ease, background 180ms ease;
}
.solutions .big:hover{
  transform: translateY(-4px);
  border-color: rgba(0,180,255,0.40);
  background: rgba(0,180,255,0.06);
}

.cover{
  height: 320px;
  background:
    radial-gradient(circle at 20% 20%, rgba(0,180,255,0.35), rgba(0,0,0,0) 55%),
    radial-gradient(circle at 85% 10%, rgba(0,120,255,0.25), rgba(0,0,0,0) 60%),
    linear-gradient(180deg, rgba(255,255,255,0.06), rgba(0,0,0,0));
  border-bottom: 1px solid rgba(255,255,255,0.08);
}
.card-body{
  padding: 18px;
}
.title{
  font-size: 26px;
  font-weight: 900;
  margin: 0;
}
.desc{
  margin-top: 10px;
  font-size: 14px;
  line-height: 1.45;
  color: rgba(255,255,255,0.75);
}
.pill{
  display:inline-block;
  margin-top: 12px;
  font-size: 12px;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.14);
  background: rgba(0,0,0,0.25);
  color: rgba(255,255,255,0.80);
}

/* Small cards */
.solutions .small{
  border-radius: 22px;
  overflow:hidden;
  border: 1px solid rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.03);
  backdrop-filter: blur(10px);
  min-height: 252px;
  position: relative;
  transition: transform 180ms ease, border-color 180ms ease, background 180ms ease;
}
.solutions .small:hover{
  transform: translateY(-4px);
  border-color: rgba(0,180,255,0.40);
  background: rgba(0,180,255,0.06);
}

.small-top{
  height: 90px;
  background:
    radial-gradient(circle at 25% 25%, rgba(0,180,255,0.28), rgba(0,0,0,0) 60%),
    linear-gradient(180deg, rgba(255,255,255,0.05), rgba(0,0,0,0));
  border-bottom: 1px solid rgba(255,255,255,0.08);
}
.small-body{ padding: 14px 14px 10px 14px; }
.small-title{
  font-size: 16px;
  font-weight: 880;
  margin: 0;
}
.small-desc{
  margin-top: 8px;
  font-size: 13px;
  line-height: 1.35;
  color: rgba(255,255,255,0.72);
}
.icon{
  position:absolute;
  top: 56px;
  left: 14px;
  width: 44px;
  height: 44px;
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

/* Bottom row (3 cards) */
.more{
  display:grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-top: 16px;
}

/* Link styling */
a.cardlink{
  text-decoration:none !important;
  color: inherit !important;
  display:block;
}

/* Responsive */
@media (max-width: 1100px){
  .solutions{ grid-template-columns: 1fr; }
  .solutions .big{ grid-row: auto; }
  .more{ grid-template-columns: 1fr; }
}
</style>
""",
    unsafe_allow_html=True
)

st.markdown("# Projects")
st.markdown("<p class='muted'>Featured solutions by industry (case files • outcomes • demos).</p>", unsafe_allow_html=True)

# ====== DATA (your real pages) ======
cards = {
    "Bancos & Seguros": ("Risk • Analytics", "Riesgo, fraude, segmentación, churn y KPIs ejecutivos.", "🏦", "pages/2a_Bancos_Seguros.py"),
    "Energía": ("Ops • Optimization", "Optimización, confiabilidad, monitoreo y analítica operativa.", "⚡", "pages/2b_Energia.py"),
    "Entretenimiento": ("NLP • Recommenders", "Recomendación, engagement, sentiment y análisis de audiencia.", "🎬", "pages/3c_Entretenimiento.py"),
    "Manufactura": ("Quality • IoT", "Calidad, OEE, mantenimiento predictivo e IoT industrial.", "🏭", "pages/2d_Manufactactura.py" if False else "pages/2d_Manufactura.py"),
    "Marketing": ("Growth • BI", "Funnels, CAC/LTV, performance, atribución y experimentación.", "📈", "pages/2e_Marketing.py"),
    "Política": ("Signals • Scenarios", "Discurso, percepción pública, señales tempranas y escenarios.", "🏛️", "pages/2f_Politica.py"),
    "Transporte": ("Routing • Forecast", "Demanda, ruteo, costos y optimización logística.", "🚚", "pages/2g_Transporte.py"),
}

# ====== RENDER: Featured solutions (1 big + 4 small) ======
big = "Bancos & Seguros"
small_4 = ["Energía", "Entretenimiento", "Manufactura", "Marketing"]
bottom = ["Política", "Transporte"]  # we’ll add a 3rd placeholder so it looks symmetric

# Build one HTML block for the grid so it renders correctly
def card_html(name, is_big=False):
    tag, desc, icon, page = cards[name]
    if is_big:
        return f"""
<a class="cardlink" href="/{page.replace("pages/","").replace(".py","")}">
  <div class="big">
    <div class="cover"></div>
    <div class="icon">{icon}</div>
    <div class="card-body">
      <p class="title">{name}</p>
      <span class="pill">{tag}</span>
      <p class="desc">{desc}</p>
      <span class="pill">Open →</span>
    </div>
  </div>
</a>
"""
    return f"""
<a class="cardlink" href="/{page.replace("pages/","").replace(".py","")}">
  <div class="small">
    <div class="small-top"></div>
    <div class="icon">{icon}</div>
    <div class="small-body">
      <p class="small-title">{name}</p>
      <span class="pill">{tag}</span>
      <p class="small-desc">{desc}</p>
      <span class="pill">Open →</span>
    </div>
  </div>
</a>
"""

# IMPORTANT:
# Streamlit multipage uses URL routing like "/Projects" not "/pages/x.py".
# So instead we will show the cards layout in HTML and keep real navigation with st.page_link right below each card using columns.

# 1) Render the layout visuals
st.markdown(
    "<div class='solutions'>"
    + card_html(big, is_big=True)
    + "".join(card_html(n) for n in small_4)
    + "</div>",
    unsafe_allow_html=True
)

# 2) Real navigation (kept inside same page area, corporate)
st.markdown("### Open an industry")
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.page_link("pages/2a_Bancos_Seguros.py", label="Bancos & Seguros", icon="🏦")
    st.page_link("pages/2b_Energia.py", label="Energía", icon="⚡")
with c2:
    st.page_link("pages/2c_Entretenimiento.py", label="Entretenimiento", icon="🎬")
    st.page_link("pages/2d_Manufactura.py", label="Manufactura", icon="🏭")
with c3:
    st.page_link("pages/2e_Marketing.py", label="Marketing", icon="📈")
    st.page_link("pages/2f_Politica.py", label="Política", icon="🏛️")
with c4:
    st.page_link("pages/2g_Transporte.py", label="Transporte", icon="🚚")

# 3) Bottom row visuals (3-up)
st.markdown(
    "<div class='more'>"
    + card_html("Política")
    + card_html("Transporte")
    + """
<div class="small" style="opacity:.9">
  <div class="small-top"></div>
  <div class="icon">✨</div>
  <div class="small-body">
    <p class="small-title">More industries</p>
    <span class="pill">Coming soon</span>
    <p class="small-desc">Más verticales y case files se agregan pronto.</p>
  </div>
</div>
"""
    + "</div>",
    unsafe_allow_html=True
)
