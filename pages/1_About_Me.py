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

# --- Header ---
st.markdown(
    """
# About

### I build data-driven systems and ship real-world solutions.
<div class="chips">
  <span class="chip">🧠 Data Science</span>
  <span class="chip">🤖 Machine Learning</span>
  <span class="chip">🛰️ Analytics & Automation</span>
  <span class="chip">⚙️ Engineering mindset</span>
</div>

<div class="hr"></div>
""",
    unsafe_allow_html=True,
)

# --- KPIs (edit to your truth) ---
st.markdown(
    """
<<div class="kpi">
  <div class="k"><b>10+ years</b><span>Industrial & oil/gas engineering</span></div>
  <div class="k"><b>1+ year</b><span>Applied data science & machine learning</span></div>
  <div class="k"><b>One profile</b><span>Where physical systems meet AI</span></div>
</div>

""",
    unsafe_allow_html=True,
)

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# --- Main two columns ---
col1, col2 = st.columns([1.35, 1], gap="large")

with col1:
    st.markdown(
        """
<div class="card">
  <h3>Who I am</h3>

  <p>
    I’m Jorge Reyes — an engineer working at the intersection of data science,
    machine learning, and real-world systems.
    I build analytical and intelligent tools that transform raw data into
    decision frameworks: dashboards, models, simulations, and automated pipelines
    designed to operate beyond the screen.
  </p>

  <p>
    My background blends engineering thinking with applied data science.
    I’m drawn to complex, imperfect environments — where information is incomplete,
    conditions change, and systems must be both technically sound and operationally viable.
  </p>

  <p>
    Beyond performance metrics, I’m especially interested in projects with real-world
    and social impact. Problems where technology can improve safety, efficiency,
    access, and quality of life.
    I care about building systems that influence reality, not just reports.
  </p>

  <h3>What drives my work</h3>
  <ul>
    <li>Designing data and ML systems meant to be used, not just analyzed.</li>
    <li>Bridging engineering constraints with analytical intelligence.</li>
    <li>Applying machine learning where it creates real leverage.</li>
    <li>Automation as a way to free people from manual and error-prone work.</li>
    <li>Clear thinking, clean structure, and explainable solutions.</li>
  </ul>
</div>

<div style="height:12px;"></div>

<div class="card">
  <h3>My Lab Philosophy</h3>

  <p>
    I treat my work as a laboratory — a space to experiment, simulate, design, and test systems
    before they exist in the real world.
  </p>

  <p>
    I’m not interested in building models in isolation.
    I’m interested in building decision engines, operational tools, and intelligent systems
    that can survive imperfect data, real constraints, and human use.
  </p>

  <p>My lab focuses on three principles:</p>

  <ul>
    <li><b>Systems over scripts.</b> I design architectures, not one-off analyses.</li>
    <li><b>Impact over novelty.</b> Technology must change something real to matter.</li>
    <li><b>Clarity over complexity.</b> Powerful systems should still be understandable.</li>
  </ul>

  <p>
    This space exists to explore applied machine learning, automation, simulation,
    and data-driven engineering — especially where they intersect with social and real-world impact.
  </p>
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
    <li>Building a portfolio that feels like a product.</li>
    <li>Sharpening ML + storytelling for interviews.</li>
    <li>Shipping projects end-to-end (data → insight → interface).</li>
  </ul>
</div>
""",
        unsafe_allow_html=True,
    )

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# --- Timeline / Experience (edit) ---
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
  <h3>Technical Instructor — Electricity / Automation</h3>
  <small><!-- TODO: dates --></small>
  <ul>
    <li>Taught hands-on classes on installations, PLCs, Arduino, and control systems.</li>
    <li>Designed competency-based evaluations and interactive learning materials.</li>
  </ul>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# --- CTAs ---
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
