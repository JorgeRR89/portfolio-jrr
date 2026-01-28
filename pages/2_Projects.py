from pathlib import Path
import streamlit as st

from src.loaders import load_projects

# =========================
# Page config
# =========================
st.set_page_config(page_title="Projects • Portfolio JRR", page_icon="🧪", layout="wide")

# =========================
# Paths
# =========================
ROOT = Path(__file__).parents[1]  # /portfolio-jrr
DATA = ROOT / "data" / "projects.yaml"

# =========================
# Minimal UI cleanup
# =========================
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

# =========================
# Theme
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
.hr{ height:1px; background: var(--line); margin: 14px 0 22px 0; }

.topbar{
  display:flex; align-items:flex-start; justify-content:space-between;
  gap: 12px;
  padding: 10px 0 2px 0;
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
  border: 1px solid rgba(255,255,255,.22);
  background: linear-gradient(180deg, rgba(255,255,255,.08), rgba(0,0,0,.20));
  border-radius: 18px;
  padding: 16px 16px;
  box-shadow: 0 0 0 1px rgba(255,255,255,.04), 0 18px 40px rgba(0,0,0,.45);
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

.modehint{
  color: rgba(255,255,255,.66);
  font-size: 12px;
  margin-top: 6px;
}

/* Cover image styling */
.cover{
  border-radius: 16px;
  border: 1px solid rgba(255,255,255,.10);
  overflow: hidden;
  margin-bottom: 10px;
}
</style>
""",
    unsafe_allow_html=True,
)

# =========================
# Helpers
# =========================
def slugify(s: str) -> str:
    s = (s or "").strip().lower()
    keep = []
    for ch in s:
        keep.append(ch if ch.isalnum() else "-")
    out = "".join(keep)
    while "--" in out:
        out = out.replace("--", "-")
    return out.strip("-")


def project_pid(p: dict) -> str:
    pid = p.get("id")
    if pid:
        return str(pid).strip()
    return slugify(p.get("title", "project"))


def lab_link(pid: str) -> str:
    return f"/Lab?project={pid}"


def safe_list(x):
    return x if isinstance(x, list) else ([] if x is None else [str(x)])


def render_cover(p: dict):
    cover = (p or {}).get("cover", "")
    if not cover:
        return
    img_path = ROOT / cover
    if img_path.exists():
        # wrapper for consistent rounded border
        st.markdown("<div class='cover'>", unsafe_allow_html=True)
        st.image(str(img_path), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


# =========================
# Load projects
# =========================
projects = load_projects(DATA)

# Normalize for UI safety
norm = []
for p in projects:
    p = dict(p or {})
    p["skills"] = safe_list(p.get("skills"))
    p["tools"] = safe_list(p.get("tools"))
    p["outcomes"] = safe_list(p.get("outcomes"))
    p["links"] = p.get("links") or {}
    p["pid"] = project_pid(p)
    norm.append(p)

projects = norm

# =========================
# Top bar
# =========================
st.markdown(
    """
<div class="topbar">
  <div>
    <h1 style="margin:0;">Projects</h1>
    <div class="small">Recruiter-friendly highlights with optional Lab demos.</div>
  </div>
  <div class="navbtns">
    <a href="/" target="_self">Home</a>
    <a href="/About_Me" target="_self">About</a>
    <a href="/Contact" target="_self">Contact</a>
  </div>
</div>
<div class="hr"></div>
""",
    unsafe_allow_html=True,
)

# =========================
# Filters
# =========================
c1, c2, c3, c4, c5, c6 = st.columns([1.35, 1.05, 1.0, 0.85, 0.9, 0.9], gap="large")
query = c1.text_input("Search", placeholder="Title, skills, tools, outcomes…")

industry_all = ["All"] + sorted({p.get("industry", "") for p in projects if p.get("industry")})
industry = c2.selectbox("Industry", industry_all, index=0)

type_all = ["All"] + sorted({p.get("type", "") for p in projects if p.get("type")})
ptype = c3.selectbox("Type", type_all, index=0)

status_all = ["All"] + sorted({p.get("status", "") for p in projects if p.get("status")})
status = c4.selectbox("Status", status_all, index=0)

impact_all = ["All"] + sorted({p.get("impact_type", "") for p in projects if p.get("impact_type")})
impact_type = c5.selectbox("Impact", impact_all, index=0)

resume_mode = c6.toggle("Resume Mode", value=True)

st.markdown(
    f"<div class='modehint'>{'Resume Mode ON → fast scan view.' if resume_mode else 'Resume Mode OFF → full recruiter view (problem → approach → results).'} </div>",
    unsafe_allow_html=True,
)

def match(p: dict) -> bool:
    if industry != "All" and p.get("industry") != industry:
        return False
    if ptype != "All" and p.get("type") != ptype:
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
                p.get("industry", ""),
                p.get("type", ""),
                p.get("status", ""),
                p.get("year", ""),
                p.get("impact_type", ""),
                " ".join(p.get("skills", [])),
                " ".join(p.get("tools", [])),
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

# =========================
# Spotlight
# =========================
spot = next((p for p in filtered if p.get("spotlight")), None)
if spot:
    render_cover(spot)

    meta = f"{spot.get('industry','')} • {spot.get('type','')} • {spot.get('status','')} • {spot.get('year','')}".strip(" •")
    impact = spot.get("impact_type", "")
    tools = spot.get("tools", [])
    skills = spot.get("skills", [])
    outcomes = spot.get("outcomes", [])
    links = spot.get("links", {}) or {}

    st.markdown(
        f"""
<div class="spotlight">
  <div class="badge">Spotlight • {meta}</div>
  <h2 style="margin:10px 0 0 0;">{spot.get("title","")}</h2>
  <p class="small" style="margin-top:10px;">{spot.get("tagline","")}</p>

  <div class="pills">
    {f"<span class='pill'>Impact: {impact}</span>" if impact else ""}
    {f"<span class='pill'>Tools: {', '.join(tools[:5])}</span>" if tools else ""}
    {f"<span class='pill'>Skills: {', '.join(skills[:3])}</span>" if skills else ""}
  </div>

  {"<div class='meta' style='margin-top:10px;'>• " + outcomes[0] + "</div>" if outcomes else ""}
</div>
""",
        unsafe_allow_html=True,
    )

    btns = [("Open in Lab", lab_link(spot["pid"]))]

    if links.get("github"):
        btns.append(("GitHub", links["github"]))
    if links.get("colab"):
        btns.append(("Colab", links["colab"]))
    if links.get("demo"):
        btns.append(("Demo", links["demo"]))
    if links.get("report"):
        btns.append(("Report", links["report"]))

    html_btns = ["<div class='links'>"]
    for label, url in btns:
        target = "_self" if label == "Open in Lab" else "_blank"
        html_btns.append(f"<a href='{url}' target='{target}'>{label} ↗</a>")
    html_btns.append("</div>")
    st.markdown("".join(html_btns), unsafe_allow_html=True)


    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# =========================
# Cards
# =========================
cards = [p for p in filtered if p is not spot]

if not cards and not spot:
    st.info("No projects match your filters yet. Add entries in data/projects.yaml.")
else:
    cols = st.columns(2, gap="large")
    for i, p in enumerate(cards):
        with cols[i % 2]:
            render_cover(p)

            meta = f"{p.get('industry','')} • {p.get('type','')} • {p.get('status','')} • {p.get('year','')}".strip(" •")
            impact = p.get("impact_type", "")
            tools = p.get("tools", [])
            skills = p.get("skills", [])
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
    {f"<span class='pill'>Tools: {', '.join(tools[:5])}</span>" if tools else ""}
    {f"<span class='pill'>Skills: {', '.join(skills[:3])}</span>" if skills else ""}
  </div>

  {"<div class='meta' style='margin-top:10px;'>" + "• " + outcomes[0] + "</div>" if (outcomes and resume_mode) else ""}
  {"<div class='meta' style='margin-top:10px;'><b>Key outcomes</b><br>" + "<br>".join([f"• {x}" for x in outcomes[:3]]) + "</div>" if (outcomes and (not resume_mode)) else ""}
</div>
""",
                unsafe_allow_html=True,
            )

            btns = [("Open in Lab", lab_link(p["pid"]))]

            if links.get("github"):
                btns.append(("GitHub", links["github"]))
            if links.get("colab"):
                btns.append(("Colab", links["colab"]))
            if links.get("demo"):
                btns.append(("Demo", links["demo"]))
            if links.get("report"):
                btns.append(("Report", links["report"]))

            html_btns = ["<div class='links'>"]
            for label, url in btns:
                target = "_self" if label == "Open in Lab" else "_blank"
                html_btns.append(f"<a href='{url}' target='{target}'>{label} ↗</a>")
            html_btns.append("</div>")
            st.markdown("".join(html_btns), unsafe_allow_html=True)

            if not resume_mode:
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

# =========================
# Bottom navigation
# =========================
st.markdown(
    """
<div class="hr"></div>
<div class="navbtns">
  <a href="/" target="_self">Back to Home</a>
  <a href="/About_Me" target="_self">About</a>
  <a href="/Contact" target="_self">Contact</a>
</div>
""",
    unsafe_allow_html=True,
)
