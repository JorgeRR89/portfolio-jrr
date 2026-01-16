import streamlit as st

st.set_page_config(
    page_title="Projects",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ====== CSS (look tipo "featured solutions", dark) ======
st.markdown(
    """
<style>
/* Layout */
.block-container{
  padding-top: 48px !important;
  padding-left: 56px !important;
  padding-right: 56px !important;
  max-width: 1400px !important;
}
h1, h2, h3, p { color: #fff; }
.small-muted { color: rgba(255,255,255,0.65); }

/* Grid of cards */
.grid{
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 18px;
  margin-top: 22px;
}

/* Card */
.card{
  grid-column: span 4;
  border-radius: 18px;
  padding: 18px 18px 16px 18px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.10);
  backdrop-filter: blur(10px);
  transition: transform 180ms ease, border-color 180ms ease, background 180ms ease;
  min-height: 140px;
}
.card:hover{
  transform: translateY(-3px);
  border-color: rgba(0,180,255,0.35);
  background: rgba(0,180,255,0.06);
}

/* Card header */
.card-top{
  display:flex;
  align-items:flex-start;
  justify-content:space-between;
  gap: 12px;
}
.card-title{
  font-size: 18px;
  font-weight: 850;
  letter-spacing: 0.2px;
  margin: 0;
}
.card-desc{
  margin: 10px 0 0 0;
  color: rgba(255,255,255,0.72);
  font-size: 14px;
  line-height: 1.35;
}

/* Tag */
.tag{
  font-size: 12px;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.14);
  background: rgba(0,0,0,0.25);
  color: rgba(255,255,255,0.78);
  white-space: nowrap;
}

/* Button */
.card-btn .stButton>button{
  width: 100%;
  border-radius: 14px !important;
  padding: 10px 12px !important;
  border: 1px solid rgba(255,255,255,0.12) !important;
  background: rgba(255,255,255,0.06) !important;
  color: #fff !important;
  font-weight: 780 !important;
}
.card-btn .stButton>button:hover{
  border-color: rgba(0,180,255,0.35) !important;
  background: rgba(0,180,255,0.10) !important;
}

/* Responsive */
@media (max-width: 1100px){
  .card{ grid-column: span 6; }
}
@media (max-width: 700px){
  .block-container{ padding-left: 18px !important; padding-right: 18px !important; }
  .card{ grid-column: span 12; }
}
</style>
""",
    unsafe_allow_html=True,
)

# ====== Header ======
st.markdown("<h1>Projects</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='small-muted'>Browse by industry. Each block will contain case files, outcomes, links and demos.</p>",
    unsafe_allow_html=True
)

# ====== Industries (edita esto) ======
INDUSTRIES = [
    {
        "name": "Data & AI",
        "tag": "ML • Analytics",
        "desc": "Modeling, forecasting, NLP, dashboards and decision systems.",
        "page": "pages/4a_Data_AI.py",   # opcional (si luego creas subpáginas)
    },
    {
        "name": "Oil & Gas / Pipelines",
        "tag": "Engineering",
        "desc": "Risk, operations analytics, pigging programs, technical delivery.",
        "page": "pages/4b_Oil_Gas.py",
    },
    {
        "name": "Industrial Automation",
        "tag": "PLC • Control",
        "desc": "Controls, instrumentation, automation design and troubleshooting.",
        "page": "pages/4c_Automation.py",
    },
    {
        "name": "E-commerce Analytics",
        "tag": "BI • Growth",
        "desc": "Profitability, demand, pricing, inventory and marketplace ops.",
        "page": "pages/4d_Ecommerce.py",
    },
    {
        "name": "Sports Analytics (NFL)",
        "tag": "Simulation",
        "desc": "Monte Carlo game scripts, props strategy and market reading.",
        "page": "pages/4e_Sports.py",
    },
    {
        "name": "Education / Teaching",
        "tag": "Curriculum",
        "desc": "Technical lesson planning, labs and learning materials.",
        "page": "pages/4f_Education.py",
    },
]

# ====== Grid ======
st.markdown("<div class='grid'>", unsafe_allow_html=True)

for i, item in enumerate(INDUSTRIES):
    st.markdown(
        f"""
        <div class="card">
          <div class="card-top">
            <h3 class="card-title">{item["name"]}</h3>
            <span class="tag">{item["tag"]}</span>
          </div>
          <p class="card-desc">{item["desc"]}</p>
        """,
        unsafe_allow_html=True
    )

    # Botón (si la subpágina aún no existe, puedes comentar esta parte)
    st.markdown("<div class='card-btn'>", unsafe_allow_html=True)
    if st.button("Open", key=f"open_{i}"):
        # Si todavía no has creado esas páginas, comenta esta línea.
        st.switch_page(item["page"])
    st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

