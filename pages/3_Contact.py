import base64
from pathlib import Path

import streamlit as st


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Contact • Portfolio JRR", page_icon="🛰️", layout="wide")


# =========================
# PATHS / ASSETS
# =========================
ROOT = Path(__file__).parent.parent  # /portfolio-jrr
ASSETS = ROOT / "assets"

LOGO_PATH = ASSETS / "wizard_FN.png"
RESUME_PATH = ASSETS / "Jorge_Reyes_CV.pdf"  # <-- asegúrate que exista en assets/


def b64_file(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8") if path.exists() else ""


logo_b64 = b64_file(LOGO_PATH)
resume_b64 = b64_file(RESUME_PATH)


# =========================
# CLEAN UI
# =========================
st.markdown(
    """
<style>
header[data-testid="stHeader"] {display:none;}
footer {visibility:hidden;}
.block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1080px; }
a { text-decoration: none; }
</style>
""",
    unsafe_allow_html=True,
)

# =========================
# THEME
# =========================
st.markdown(
    """
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
p, li, small { color: var(--fg2); }

.hr{ height:1px; background: var(--line); margin: 16px 0 22px 0; }

.topbar{
  display:flex; align-items:flex-start; justify-content:space-between;
  gap: 12px;
  padding: 6px 0 2px 0;
}

.brand{
  display:flex; align-items:center; gap:12px;
  color: rgba(255,255,255,.92);
  font-weight:700;
  letter-spacing:.3px;
  font-size: 14px;
}
.brand img{
  width: 34px; height: 34px;
  border-radius: 10px;
  object-fit: cover;
  box-shadow: 0 10px 28px rgba(0,0,0,.35);
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
  display:inline-flex; align-items:center; gap:10px;
  padding: 12px 16px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: rgba(255,255,255,.05);
  color: rgba(255,255,255,.92) !important;
  font-size: 14px;
}
.action a:hover{ background: rgba(255,255,255,.09); }

.tagwrap{ display:flex; gap:10px; flex-wrap:wrap; margin-top:10px; }
.tag{
  padding: 7px 10px;
  border-radius: 12px;
  border: 1px solid var(--line);
  background: rgba(0,0,0,.18);
  color: rgba(255,255,255,.78);
  font-size: 12px;
}

.icon{
  width: 16px; height: 16px; display:inline-block;
  border-radius: 4px;
  background: rgba(255,255,255,.14);
}
.icon svg{ width:16px; height:16px; display:block; }

ul.clean{ margin: 10px 0 0 18px; padding: 0; }
ul.clean li{ margin: 6px 0; }

@media (max-width: 780px){
  .topbar{ flex-direction: column; }
  .navbtns{ justify-content:flex-start; }
}
</style>
""",
    unsafe_allow_html=True,
)


# =========================
# ICONS (inline SVG, minimal)
# =========================
def svg_icon(kind: str) -> str:
    icons = {
        "resume": """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M7 3h7l3 3v15a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z" stroke="rgba(255,255,255,.82)" stroke-width="1.6"/>
  <path d="M14 3v4h4" stroke="rgba(255,255,255,.82)" stroke-width="1.6"/>
  <path d="M8 11h8M8 15h8M8 19h6" stroke="rgba(255,255,255,.70)" stroke-width="1.6" stroke-linecap="round"/>
</svg>
""",
        "linkedin": """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M6 9v12" stroke="rgba(255,255,255,.82)" stroke-width="1.8" stroke-linecap="round"/>
  <path d="M6 6.5a1.3 1.3 0 1 0 0-2.6a1.3 1.3 0 0 0 0 2.6z" fill="rgba(255,255,255,.82)"/>
  <path d="M10 21v-7.2c0-2.5 3.5-2.7 3.5 0V21" stroke="rgba(255,255,255,.82)" stroke-width="1.8" stroke-linecap="round"/>
  <path d="M17.5 13.2V21" stroke="rgba(255,255,255,.82)" stroke-width="1.8" stroke-linecap="round"/>
  <path d="M10 13.8V9h3.2" stroke="rgba(255,255,255,.70)" stroke-width="1.8" stroke-linecap="round"/>
</svg>
""",
        "github": """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M12 2.6c-5.2 0-9.4 4.2-9.4 9.4c0 4.1 2.7 7.6 6.4 8.8c.5.1.7-.2.7-.5v-1.7c-2.6.6-3.2-1.1-3.2-1.1c-.4-1.1-1-1.4-1-1.4c-.9-.6.1-.6.1-.6c1 .1 1.5 1 1.5 1c.9 1.5 2.4 1.1 3 .8c.1-.7.4-1.1.7-1.3c-2.1-.2-4.3-1-4.3-4.7c0-1 .4-1.8 1-2.4c-.1-.2-.4-1.2.1-2.4c0 0 .8-.3 2.5 1c.7-.2 1.5-.3 2.3-.3c.8 0 1.6.1 2.3.3c1.7-1.2 2.5-1 2.5-1c.5 1.2.2 2.2.1 2.4c.6.6 1 1.4 1 2.4c0 3.7-2.2 4.5-4.3 4.7c.4.3.7.9.7 1.8v2.7c0 .3.2.6.7.5c3.7-1.2 6.4-4.7 6.4-8.8c0-5.2-4.2-9.4-9.4-9.4z" fill="rgba(255,255,255,.82)"/>
</svg>
""",
        "email": """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M4 7h16v10a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V7z" stroke="rgba(255,255,255,.82)" stroke-width="1.6"/>
  <path d="M4.5 7.5l7.5 6l7.5-6" stroke="rgba(255,255,255,.70)" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
""",
        "calendar": """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M7 3v3M17 3v3" stroke="rgba(255,255,255,.82)" stroke-width="1.6" stroke-linecap="round"/>
  <path d="M4.5 7h15v13a2 2 0 0 1-2 2h-11a2 2 0 0 1-2-2V7z" stroke="rgba(255,255,255,.82)" stroke-width="1.6"/>
  <path d="M7 11h10M7 15h7" stroke="rgba(255,255,255,.70)" stroke-width="1.6" stroke-linecap="round"/>
</svg>
""",
    }
    return icons.get(kind, "")


def action_link(href: str, label: str, icon_kind: str, new_tab: bool = True, download: bool = False) -> str:
    icon = svg_icon(icon_kind)
    icon_html = f"<span class='icon'>{icon}</span>" if icon else ""
    target = "_blank" if new_tab else "_self"
    dl = "download" if download else ""
    return f"<a href='{href}' target='{target}' {dl}>{icon_html}{label}</a>"


# =========================
# HEADER / NAV
# =========================
brand_img = f"<img alt='logo' src='data:image/png;base64,{logo_b64}' />" if logo_b64 else ""

st.markdown(
    f"""
<div class="topbar">
  <div class="brand">
    {brand_img}
    <div>Portfolio JRR</div>
  </div>

  <div class="navbtns">
    <a href="./" target="_self">Home</a>
    <a href="./About_Me" target="_self">About</a>
    <a href="./Projects" target="_self">Projects</a>
    <a href="./Lab" target="_self">Lab</a>
  </div>
</div>

<div style="height:10px;"></div>

<div>
  <h1 style="margin:0;">Contact</h1>
  <div class="small">A simple interface to connect.</div>
</div>

<div class="hr"></div>
""",
    unsafe_allow_html=True,
)

# =========================
# HERO
# =========================
st.markdown(
    """
<div class="card">
  <h2 style="margin-top:0;">Let’s build something real.</h2>
  <p class="small">
    I’m interested in roles and collaborations where data, machine learning, and engineering
    intersect with real-world systems.
  </p>

  <div class="tagwrap">
    <span class="tag">Data science & machine learning</span>
    <span class="tag">Analytics & decision systems</span>
    <span class="tag">Automation & real-world constraints</span>
    <span class="tag">Simulation, forecasting, optimization</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# =========================
# GRID
# =========================
col1, col2 = st.columns([1.05, 1], gap="large")

with col1:
    # Resume & Profiles
    resume_link = (
        f"data:application/pdf;base64,{resume_b64}"
        if resume_b64
        else None
    )

    links = []
    if resume_link:
        links.append(action_link(resume_link, "Download Resume", "resume", new_tab=False, download=True))
    else:
        # Fallback visual: muestra advertencia si no existe el PDF
        st.warning("Resume PDF not found. Add it to assets/ as 'Jorge_Reyes_CV.pdf' (or update RESUME_PATH).")

    links.append(action_link("https://www.linkedin.com/in/jorge-reyes-data-science/", "LinkedIn", "linkedin", new_tab=True))
    links.append(action_link("https://github.com/JorgeRR89", "GitHub", "github", new_tab=True))

    st.markdown(
        f"""
<div class="card">
  <h3 style="margin-top:0;">Resume & Profiles</h3>
  <p class="small">Fast access for recruiters and collaborators.</p>
  <div class="action">
    {''.join(links)}
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    # Contact actions
    calendly_url = "https://calendly.com/reyesrod-jorge"

 st.markdown("""
<div class="card">
  <h3>Contact</h3>
  <p class="small">Open channel for opportunities, projects, or technical discussions.</p>

  <div class="action">

    <a href="mailto:reyesrod.jorge@gmail.com" target="_blank">
      Send Email
    </a>

    <a href="https://wa.me/525545230886?text=Hi%20Jorge%2C%20I%20saw%20your%20portfolio%20and%20I’d%20like%20to%20connect."
       target="_blank">
       WhatsApp
    </a>

    <a href="https://calendly.com/reyesrod-jorge" target="_blank">
      Schedule a call
    </a>

  </div>
</div>
""", unsafe_allow_html=True)



with col2:
    st.markdown(
        """
<div class="card">
  <h3 style="margin-top:0;">What I’m looking for</h3>

  <p class="small">
    Teams where intelligent systems are operational — where models touch processes, decisions,
    performance, and people.
  </p>

  <ul class="clean">
    <li>Applied machine learning and decision systems</li>
    <li>Data products and analytics platforms</li>
    <li>Simulation, forecasting, and optimization</li>
    <li>Automation and real-world engineering constraints</li>
  </ul>

  <p class="small" style="margin-top:12px;">
    If what you saw in Projects and Lab aligns with your work, I’d be glad to connect.
  </p>
</div>
""",
        unsafe_allow_html=True,
    )

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

st.markdown(
    """
<div class="small">
© Jorge Reyes — Portfolio JRR<br/>
Built as a system, not a static page.
</div>
""",
    unsafe_allow_html=True,
)
