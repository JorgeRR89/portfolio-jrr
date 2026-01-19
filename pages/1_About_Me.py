import streamlit as st

st.set_page_config(page_title="About • Portfolio JRR", page_icon="🛰️", layout="wide")

# --- Minimal UI cleanup (matches Home) ---
helps = """
<style>
header[data-testid="stHeader"] {display:none;}
footer {visibility:hidden;}
.block-container { padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1080px; }
a { text-decoration: none; }
</style>
"""
st.markdown(helps, unsafe_allow_html=True)

# --- Subtle background / typography (antigravity-ish, lightweight) ---
theme = """
<style>
:root{
  --fg: rgba(255,255,255,.92);
  --fg2: rgba(255,255,255,.72);
  --line: rgba(255,255,255,.10);
  --card: rgba(255,255,255,.04);
  --card2: rgba(0,0,0,.25);
}
html, body, [data-testid="stAppViewContainer"]{
  background: radial-gradient(900px 520px at 50% 0%, rgba(255,255,255,.05), rgba(0,0,0,.98)) !important;
  color: var(--fg) !important;
}
h1,h2,h3{ letter-spacing: -0.03em; }
small, p, li { color: var(--fg2); }
.hr{
  height:1px; background: var(--line); margin: 18px 0 26px 0;
}
.chips{
  display:flex; gap:10px; flex-wrap: wrap; margin-top: 10px;
}
.chip{
  display:inline-flex; align-items:center; gap:8px;
  padding: 8px 12px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: rgba(255,255,255,.03);
  color: rgba(255,255,255,.82);
  font-size: 12px;
}
.card{
  border: 1px solid var(--line);
  background: linear-gradient(180deg, var(--card), rgba(0,0,0,.18));
  border-radius: 18px;
  padding: 18px 18px;
}
.card h3{ margin-top: 0; }
.tagwrap{ display:flex; gap:10px; flex-wrap:wrap; }
.tag{
  padding: 7px 10px;
  border-radius: 12px;
  border: 1px solid var(--line);
  background: rgba(0,0,0,.18);
  color: rgba(255,255,255,.78);
  font-size: 12px;
}
.cta{
  display:flex; gap:10px; flex-wrap:wrap; margin-top: 14px;
}
.cta a{
  display:inline-block;
  padding: 10px 14px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: rgba(255,255,255,.04);
  color: rgba(255,255,255,.88) !important;
}
.cta a:hover{ background: rgba(255,255,255,.07); }
.kpi{
  display:grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}
.kpi .k{
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 14px 14px;
  background: rgba(255,255,255,.03);
}
.kpi .k b{ font-size: 18px; color: rgba(255,255,255,.92); }
.kpi .k span{ display:block; margin-top: 2px; font-size: 12px; color: rgba(255,255,255,.68); }
@media (max-width: 780px){
  .kpi{ grid-template-columns: 1fr; }
}
</style>
"""
st.markdown(theme, unsafe_allow_html=True)

# --- Content ---
st.markdown(
    """
# About

### I build data-driven systems and ship real-world solutions.
<div class="chips">
  <span class="chip">🧠 Data Science</span>
  <span class="chip">🛰️ Analytics & Automation</span>
  <span class="chip">⚙️ Engineering mindset</span>
</div>

<div class="hr"></div>
""",
    unsafe_allow_html=True,
)

# KPIs (edit to your truth)
st.markdown(
    """
<div class="kpi">
  <div class="k"><b>TODO</b><span>Years across engineering + analytics</span></div>
  <div class="k"><b>TODO</b><span>Dashboards / models shipped</span></div>
  <div class="k"><b>TODO</b><span>Domains: e-commerce, industrial, sports analytics</span></div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

col1, col2 = st.columns([1.35, 1], gap="large")

with col1:
    st.markdown(
        """
<div class="card">
  <h3>Who I am</h3>
  <p>
    <!-- TODO: escribe 4–6 líneas con tu narrativa -->
    I’m Jorge Reyes — an engineer who transitioned into data science and analytics.
    I like turning messy data into decision systems: dashboards, pipelines, forecasts,
    simulations, and automation that improve outcomes.
  </p>

  <p>
    <!-- TODO: ajusta a tu realidad -->
    My work spans e-commerce performance, industrial engineering projects,
    and sports simulation workflows — always with a focus on clarity, speed, and measurable impact.
  </p>

  <h3>What I optimize for</h3>
  <ul>
    <li>Clean, reproducible analysis (Python/SQL) and readable results.</li>
    <li>Practical ML when it truly adds value (not for decoration).</li>
    <li>Automation to remove manual work and reduce errors.</li>
    <li>Strong communication: explain complex systems simply.</li>
  </ul>
</div>
""",
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
<div class="card">
  <h3>Core stack</h3>
  <div class="tagwrap">
    <span class="tag">Python</span>
    <span class="tag">SQL</span>
    <span class="tag">pandas</span>
    <span class="tag">scikit-learn</span>
    <span class="tag">Power BI</span>
    <span class="tag">Streamlit</span>
    <span class="tag">Git/GitHub</span>
  </div>

  <div style="height:12px;"></div>

  <h3>Now</h3>
  <ul>
    <li><!-- TODO --> Building a portfolio that feels like a product.</li>
    <li><!-- TODO --> Sharpening ML + storytelling for interviews.</li>
    <li><!-- TODO --> Shipping projects end-to-end (data → insight → interface).</li>
  </ul>
</div>
""",
        unsafe_allow_html=True,
    )

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# Timeline / Experience (edit)
st.markdown("### Timeline", unsafe_allow_html=True)
st.markdown(
    """
<div class="card">
  <h3>Account Manager / Data Analyst — Virtual Integration Warehouse (Contract)</h3>
  <small>Apr 2023 — Nov 2025</small>
  <ul>
    <li>Built predictive models and interactive dashboards to analyze sales, customers, and product performance.</li>
    <li>Automated SQL + pandas workflows, reducing manual analysis time by ~60%.</li>
    <li>Designed Monte Carlo simulations and classification models for demand and strategy.</li>
    <li>Optimized e-commerce decisions across Mercado Libre and Amazon.</li>
  </ul>
</div>

<div style="height:12px;"></div>

<div class="card">
  <h3><!-- TODO: role/title --> Technical Instructor — Electricity / Automation</h3>
  <small><!-- TODO: dates --></small>
  <ul>
    <li><!-- TODO --> Taught hands-on classes on installations, PLCs, Arduino, and control systems.</li>
    <li><!-- TODO --> Designed competency-based evaluations and interactive learning materials.</li>
  </ul>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# CTAs
st.markdown(
    """
### Want the projects?
<div class="cta">
  <a href="./Projects" target="_self">→ Explore Projects</a>
  <a href="./Contact" target="_self">→ Contact</a>
  <a href="./Lab" target="_self">→ Enter the Lab</a>
</div>
""",
    unsafe_allow_html=True,
)

