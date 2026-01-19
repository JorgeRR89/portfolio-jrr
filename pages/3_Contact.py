import streamlit as st

st.set_page_config(page_title="Contact • Portfolio JRR", page_icon="📡", layout="wide")

# --- Minimal UI cleanup ---
st.markdown("""
<style>
header[data-testid="stHeader"] {display:none;}
footer {visibility:hidden;}
.block-container { padding-top: 1.8rem; padding-bottom: 3rem; max-width: 1080px; }
a { text-decoration: none; }
</style>
""", unsafe_allow_html=True)

# --- Theme (same system as About/Projects/Lab) ---
st.markdown("""
<style>
:root{
  --fg: rgba(255,255,255,.92);
  --fg2: rgba(255,255,255,.72);
  --line: rgba(255,255,255,.10);
  --card: rgba(255,255,255,.04);
}
html, body, [data-testid="stAppViewContainer"]{
  background: radial-gradient(900px 520px at 50% 0%, rgba(255,255,255,.05), rgba(0,0,0,.98)) !important;
  color: var(--fg) !important;
}
h1,h2,h3{ letter-spacing: -0.03em; }
.hr{ height:1px; background: var(--line); margin: 16px 0 22px 0; }

.topbar{
  display:flex; align-items:flex-start; justify-content:space-between;
  gap: 12px;
  padding: 8px 0 2px 0;
}
.navbtns{ display:flex; gap:10px; flex-wrap:wrap; justify-content:flex-end; }
.navbtns a{
  display:inline-block;
  padding: 9px 12px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: rgba(255,255,255,.04);
  color: rgba(255,255,255,.88) !important;
  text-decoration:none;
  font-size: 13px;
}
.navbtns a:hover{ background: rgba(255,255,255,.07); }

.card{
  border: 1px solid var(--line);
  background: linear-gradient(180deg, var(--card), rgba(0,0,0,.18));
  border-radius: 18px;
  padding: 18px 18px;
}
.small{ color: rgba(255,255,255,.72); }

.action{
  display:flex; gap:12px; flex-wrap:wrap; margin-top: 10px;
}
.action a{
  display:inline-flex; align-items:center; gap:8px;
  padding: 12px 16px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: rgba(255,255,255,.05);
  color: rgba(255,255,255,.92) !important;
  font-size: 14px;
}
.action a:hover{ background: rgba(255,255,255,.09); }

.tagwrap{ display:flex; gap:10px; flex-wrap:wrap; margin-top:8px; }
.tag{
  padding: 7px 10px;
  border-radius: 12px;
  border: 1px solid var(--line);
  background: rgba(0,0,0,.18);
  color: rgba(255,255,255,.78);
  font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

# --- Top bar ---
st.markdown("""
<div class="topbar">
  <div>
    <h1 style="margin:0;">Contact</h1>
    <div class="small">Command interface — connect, collaborate, or deploy.</div>
  </div>
  <div class="navbtns">
    <a href="./" target="_self">← Home</a>
    <a href="./About_Me" target="_self">About</a>
    <a href="./Projects" target="_self">Projects</a>
    <a href="./Lab" target="_self">Lab</a>
  </div>
</div>

<div class="hr"></div>
""", unsafe_allow_html=True)

# --- HERO ---
st.markdown("""
<div class="card">
  <h2>Let’s build something real.</h2>
  <p class="small">
    I’m interested in roles and collaborations where data, machine learning and engineering
    intersect with real-world systems — industrial, analytical, autonomous, or impact-driven.
  </p>

  <div class="tagwrap">
    <span class="tag">🧠 Data Science & ML</span>
    <span class="tag">⚙️ Engineering systems</span>
    <span class="tag">📈 Decision platforms</span>
    <span class="tag">🌍 Social & operational impact</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# --- GRID ---
col1, col2 = st.columns([1.05, 1], gap="large")

with col1:
    st.markdown("""
<div class="card">
  <h3>Resume & Profiles</h3>
  <p class="small">Fast access for recruiters and collaborators.</p>

  <div class="action">
    <a href="https://YOUR_LINK_TO_RESUME.pdf" target="_blank">📄 Download Resume</a>
    <a href="https://www.linkedin.com/in/YOURUSERNAME" target="_blank">💼 LinkedIn</a>
    <a href="https://github.com/YOURUSERNAME" target="_blank">🧩 GitHub</a>
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    st.markdown("""
<div class="card">
  <h3>Contact</h3>
  <p class="small">Open channel for opportunities, projects, or technical discussions.</p>

  <div class="action">
    <a href="mailto:YOURMAIL@domain.com">✉️ Email</a>
    <a href="https://calendly.com/YOURLINK" target="_blank">📅 Schedule a call</a>
  </div>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div class="card">
  <h3>Direction</h3>

  <p class="small">
    I’m particularly interested in environments where intelligent systems are not theoretical,
    but operational — where models touch processes, decisions, safety, performance, and people.
  </p>

  <ul class="small">
    <li>Applied machine learning and decision systems</li>
    <li>Industrial, automation, and operations-driven AI</li>
    <li>Simulation, forecasting, and optimization platforms</li>
    <li>Data products with measurable real-world impact</li>
  </ul>

  <p class="small">
    If what you saw in the Lab and Projects aligns with your work,
    I’d be glad to connect.
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

st.markdown("""
<div class="small">
© Jorge Reyes — Portfolio Lab  
This interface is intentionally built as a system, not a static page.
</div>
""", unsafe_allow_html=True)
