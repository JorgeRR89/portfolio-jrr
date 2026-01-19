from pathlib import Path
import streamlit as st

from src.loaders import load_projects

st.set_page_config(page_title="Projects • Portfolio JRR", page_icon="🧪", layout="wide")

# ---- Minimal UI cleanup ----
st.markdown(
    """
<style>
header[data-testid="stHeader"] {display:none;}
footer {visibility:hidden;}
.block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1180px; }
</style>
""",
    unsafe_allow_html=True,
)

# ---- Theme (matches About) ----
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
.hr{ height:1px; background: var(--line); margin: 14px 0 22px 0; }

.topbar{
  display:flex; align-items:center; justify-content:space-between;
  gap: 12px;
  padding: 10px 0 2px 0;
}
.navbtns{ display:flex; gap:10px; flex-wrap:wrap; }
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
  padding: 16px 16px;
}
.meta{ color: rgba(255,255,255,.68); font-size: 12px; margin-top: 4px; }
.small{ color: rgba(255,255,255,.72); }

.pills{ display:flex; gap:8px; flex-wrap:wrap; margin-top: 10px; }
.pill{
  padding: 6px 9px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: rgba(0,0,0,.18);
  color: rgba(255,255,255,.78);
  font-size: 12px;
}

.badge{
  display:inline-flex; align-items:center; gap:8px;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: rgba(255,255,255,.03);
  color: rgba(255,255,255,.84);
  font-size: 12px;
}

.spotlight{
  border: 1px solid rgba(255,255,255,.14);
  background: linear-gradient(180deg, rgba(255,255,255,.06), rgba(0,0,0,.18));
  border-radius: 22px;
  padding: 18px 18px;
}

.links a{
  display:inline-block;
  padding: 8px 12px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: rgba(255,255,255,.04);
  color: rgba(255,255,255,.88) !important;
  text-decoration:none;
  margin-right: 8px;
  margin-top: 10px;
  font-size: 13px;
}
.links a:hover{ background: rgba(255,255,255,.07); }

.kv{
  margin-top: 10px;
  display:grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}
@media (max-width: 900px){
  .kv{ grid-template-columns: 1fr; }
}
.kv .box{
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 12px 12px;
  background: rgba(255,255,255,.03);
}
.kv .box b{ color: rgba(255,255,255,.88); }
</style>
""",
    unsafe_allow_html=True,
)

ROOT = Path(__file__).parents[1]
DATA = ROOT / "data" / "projects.yaml"
projects = load_projects(DATA)

# ---- Top bar with "Back to Home" ----
st.markdown(
    """
<div class="topbar">
  <div>
    <h1 style="margin:0;">Projects</h1>
    <div class="small">Recruiter-friendly highlights: problem → approach → outcomes.</div>
  </div>
  <div class="navbtns">
    <a href="./" target="_self">← Home</a>
    <a href="./About_Me" target="_self">About</a>
    <a href="./Contact" target="_self">Contact</a>
  </div>
</div>
<div class="hr"></div>
""",
    unsafe_allow_html=True,
)

# ---- Controls ----
c1, c2, c3, c4 = st.columns([1.6, 0.9, 0.9, 0.9], gap="large")
query = c1.text_input("Search", placeholder="Title, tags, stack, outcomes…")

cat_all = ["All"] + sorted({p["category"] for p in projects if p.get("category")})
category = c2.selectbox("Category", cat_all, index=0)

status_all = ["All"] + sorted({p["status"] for p in projects if p.get("status")})
status = c3.selectbox("Status", status_all, index=0)

impact_all = ["All"] + sorted({p["impact_type"] for p in projects if p.get("impact_type")})
impact_type = c4.selectbox("Impact", impact_all, index=0)

def match(p: dict) -> bool:
    if category != "All" and p.get("category") != category:
        return False
    if status != "All" and p.get("status") != status:
        return False
    if impact_type != "All" and p.get("impact_type") != impact_type:
        return False
    if query.strip():
        q = query.lower().strip()
        hay = " ".join(
            [
                p.get("title", ""),
                p.get("tagline", ""),
                p.get("category", ""),
                p.get("status", ""),
                p.get("year", ""),
                p.get("impact_type", ""),
                " ".join(p.get("tags", [])),
                " ".join(p.get("stack", [])),
                " ".join(p.get("outcomes", [])),
                p.get("problem", ""),
                p.get("approach", ""),
                p.get("results", ""),
                p.get("details", ""),
            ]
        ).lower()
        return q in hay
    return True

filtered = [p for p in projects if match(p)]
st.caption(f"Showing {len(filtered)} / {len(projects)} projects")

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# ---- Spotlight (first matching spotlight project) ----
spot = next((p for p in filtered if p.get("spotlight")), None)
if spot:
    st.markdown(
        f"""
<div class="spotlight">
  <div class="badge">✨ Spotlight • {spot.get("category","")} • {spot.get("status","")} • {spot.get("year","")}</div>
  <h2 style="margin:10px 0 0 0;">{spot.get("title","")}</h2>
  <p class="small" style="margin-top:10px;">{spot.get("tagline","")}</p>

  <div class="pills">
    {f"<span class='pill'>Impact: {spot.get('impact_type','')}</span>" if spot.get('impact_type') else ""}
    {f"<span class='pill'>Stack: {', '.join(spot.get('stack', [])[:5])}</span>" if spot.get('stack') else ""}
  </div>

  <div class="kv">
    <div class="box"><b>Problem</b><div class="small">{spot.get("problem","")}</div></div>
    <div class="box"><b>Approach</b><div class="small">{spot.get("approach","")}</div></div>
    <div class="box"><b>Outcomes</b><div class="small">{"<br>".join([f"• {x}" for x in spot.get("outcomes", [])[:4]])}</div></div>
    <div class="box"><b>Results</b><div class="small">{spot.get("results","")}</div></div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# ---- Card grid (without duplicating spotlight) ----
cards = [p for p in filtered if p is not spot]

if not cards and not spot:
    st.info("No projects match your filters yet. Add entries in data/projects.yaml.")
else:
    cols = st.columns(2, gap="large")
    for i, p in enumerate(cards):
        with cols[i % 2]:
            meta = f"{p.get('category','')} • {p.get('status','')} • {p.get('year','')}".strip(" •")
            impact = p.get("impact_type", "")
            stack = p.get("stack", [])
            tags = p.get("tags", [])
            outcomes = p.get("outcomes", [])
            links = p.get("links", {}) or {}

            st.markdown(
                f"""
<div class="card">
  <div class="badge">{meta}</div>
  <h3 style="margin:10px 0 0 0;">{p.get("title","")}</h3>
  <p class="small" style="margin-top:8px; margin-bottom:0;">{p.get("tagline","")}</p>

  <div class="pills">
    {f"<span class='pill'>Impact: {impact}</span>" if impact else ""}
    {f"<span class='pill'>Stack: {', '.join(stack[:4])}</span>" if stack else ""}
  </div>

  {"<div class='meta' style='margin-top:10px;'><b>Key outcomes</b><br>" + "<br>".join([f"• {x}" for x in outcomes[:3]]) + "</div>" if outcomes else ""}
</div>
""",
                unsafe_allow_html=True,
            )

            with st.expander("Recruiter view (problem → approach → results)", expanded=False):
                if p.get("problem"):
                    st.markdown("**Problem**")
                    st.write(p["problem"])
                if p.get("approach"):
                    st.markdown("**Approach**")
                    st.write(p["approach"])
                if p.get("results"):
                    st.markdown("**Results**")
                    st.write(p["results"])
                if p.get("details"):
                    st.markdown("**Notes**")
                    st.write(p["details"])

                # Links as pill buttons (only if present)
                btns = []
                if links.get("github"):
                    btns.append(("GitHub", links["github"]))
                if links.get("demo"):
                    btns.append(("Demo", links["demo"]))
                if links.get("report"):
                    btns.append(("Report", links["report"]))

                if btns:
                    st.markdown("<div class='links'>", unsafe_allow_html=True)
                    for label, url in btns:
                        st.markdown(f"<a href='{url}' target='_blank'>{label} ↗</a>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

# ---- Bottom navigation (extra obvious exit) ----
st.markdown(
    """
<div class="hr"></div>
<div class="navbtns">
  <a href="./" target="_self">← Back to Home</a>
  <a href="./About_Me" target="_self">About</a>
  <a href="./Contact" target="_self">Contact</a>
</div>
""",
    unsafe_allow_html=True,
)
