from pathlib import Path

import streamlit as st

from src.loaders import load_projects

st.set_page_config(page_title="Projects • Portfolio JRR", page_icon="🧪", layout="wide")

# --- Minimal UI cleanup ---
st.markdown(
    """
<style>
header[data-testid="stHeader"] {display:none;}
footer {visibility:hidden;}
.block-container { padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1180px; }
</style>
""",
    unsafe_allow_html=True,
)

# --- Theme (matches About) ---
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
.hr{ height:1px; background: var(--line); margin: 16px 0 22px 0; }

.card{
  border: 1px solid var(--line);
  background: linear-gradient(180deg, var(--card), rgba(0,0,0,.18));
  border-radius: 18px;
  padding: 16px 16px;
}
.meta{ color: rgba(255,255,255,.68); font-size: 12px; margin-top: 4px; }
.tags{ display:flex; gap:8px; flex-wrap:wrap; margin-top: 10px; }
.tag{
  padding: 6px 9px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: rgba(0,0,0,.18);
  color: rgba(255,255,255,.76);
  font-size: 12px;
}
.badge{
  display:inline-flex; align-items:center; gap:8px;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: rgba(255,255,255,.03);
  color: rgba(255,255,255,.80);
  font-size: 12px;
}
.links a{
  display:inline-block;
  padding: 8px 12px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: rgba(255,255,255,.04);
  color: rgba(255,255,255,.88) !important;
  text-decoration: none;
  margin-right: 8px;
  margin-top: 10px;
}
.links a:hover{ background: rgba(255,255,255,.07); }
.small{ color: rgba(255,255,255,.70); }
</style>
""",
    unsafe_allow_html=True,
)

ROOT = Path(__file__).parents[1]
DATA = ROOT / "data" / "projects.yaml"

projects = load_projects(DATA)

st.markdown(
    """
# Projects

### A curated index of systems, experiments, and applied work.
<div class="hr"></div>
""",
    unsafe_allow_html=True,
)

# --- Controls ---
c1, c2, c3 = st.columns([1.4, 0.9, 0.9], gap="large")
query = c1.text_input("Search", placeholder="Search by title, tags, stack, category…")
category_all = ["All"] + sorted({p["category"] for p in projects if p.get("category")})
category = c2.selectbox("Category", category_all, index=0)
status_all = ["All"] + sorted({p["status"] for p in projects if p.get("status")})
status = c3.selectbox("Status", status_all, index=0)

def match(p: dict) -> bool:
    if category != "All" and p.get("category") != category:
        return False
    if status != "All" and p.get("status") != status:
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
                " ".join(p.get("tags", [])),
                " ".join(p.get("stack", [])),
                p.get("impact", ""),
                p.get("details", ""),
            ]
        ).lower()
        return q in hay
    return True

filtered = [p for p in projects if match(p)]
st.caption(f"Showing {len(filtered)} / {len(projects)} projects")

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# --- Grid of cards ---
if not filtered:
    st.info("No projects match your filters yet. Add more entries in data/projects.yaml.")
else:
    cols = st.columns(2, gap="large")
    for i, p in enumerate(filtered):
        with cols[i % 2]:
            title = p.get("title", "")
            tagline = p.get("tagline", "")
            meta = f"{p.get('category','')} • {p.get('status','')} • {p.get('year','')}".strip(" •")
            impact = p.get("impact", "")
            tags = p.get("tags", [])
            stack = p.get("stack", [])
            links = p.get("links", {}) or {}
            highlights = p.get("highlights", [])
            details = p.get("details", "")

            st.markdown(
                f"""
<div class="card">
  <h3 style="margin:0;">{title}</h3>
  <div class="meta">{meta}</div>
  <p class="small" style="margin-top:10px; margin-bottom:0;">{tagline}</p>

  {"<div class='tags'>" + "".join([f"<span class='tag'>{t}</span>" for t in tags[:6]]) + "</div>" if tags else ""}
  {"<div class='meta' style='margin-top:10px;'>Stack: " + ", ".join(stack) + "</div>" if stack else ""}
  {"<div class='meta' style='margin-top:6px;'><b>Impact:</b> " + impact + "</div>" if impact else ""}
</div>
""",
                unsafe_allow_html=True,
            )

            with st.expander("Details", expanded=False):
                if highlights:
                    st.markdown("**Highlights**")
                    for h in highlights:
                        st.write(f"- {h}")
                if details:
                    st.markdown("**Notes**")
                    st.write(details)

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
