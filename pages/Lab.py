# pages/Lab.py
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional
import html as _html

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

from src.loaders import load_projects


# =========================
# Page config
# =========================
st.set_page_config(page_title="Lab • Portfolio JRR", page_icon="🧪", layout="wide")


# =========================
# Minimalist styles
# =========================
st.markdown(
    """
<style>
header[data-testid="stHeader"] {display:none;}
footer {visibility:hidden;}
.block-container { padding-top: 1.2rem; padding-bottom: 3rem; max-width: 1180px; }
a { text-decoration: none; }

:root{
  --fg: rgba(255,255,255,.92);
  --fg2: rgba(255,255,255,.70);
  --line: rgba(255,255,255,.10);
  --card: rgba(255,255,255,.04);
  --card2: rgba(0,0,0,.18);
  --ok: rgba(120,255,180,.95);
  --warn: rgba(255,210,120,.95);
  --err: rgba(255,120,140,.95);
}

html, body, [data-testid="stAppViewContainer"]{
  background: radial-gradient(1000px 620px at 50% 0%, rgba(255,255,255,.05), rgba(0,0,0,.98)) !important;
  color: var(--fg) !important;
}

h1,h2,h3{ letter-spacing: -0.03em; }
small, p, li { color: var(--fg2); }

.hr{ height:1px; background: var(--line); margin: 14px 0 18px 0; }

.topbar{
  display:flex; align-items:flex-start; justify-content:space-between;
  gap: 12px;
  padding: 6px 0 6px 0;
}
.navbtns{ display:flex; gap:10px; flex-wrap:wrap; justify-content:flex-end; }
.navbtns a{
  display:inline-block;
  padding: 9px 12px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: rgba(255,255,255,.04);
  color: rgba(255,255,255,.88) !important;
  font-size: 13px;
}
.navbtns a:hover{ background: rgba(255,255,255,.08); }

.card{
  border: 1px solid var(--line);
  background: linear-gradient(180deg, var(--card), rgba(0,0,0,.16));
  border-radius: 18px;
  padding: 16px 16px;
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

.pills{ display:flex; gap:8px; flex-wrap:wrap; margin-top: 10px; }
.pill{
  padding: 6px 9px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: rgba(0,0,0,.18);
  color: rgba(255,255,255,.78);
  font-size: 12px;
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

.bigcta{
  display:inline-flex; align-items:center; gap:10px;
  padding: 10px 14px;
  border-radius: 14px;
  border: 1px solid rgba(255,255,255,.14);
  background: linear-gradient(180deg, rgba(255,255,255,.06), rgba(0,0,0,.10));
  color: rgba(255,255,255,.92);
  font-size: 14px;
}

.console{
  border: 1px solid var(--line);
  border-radius: 16px;
  background: rgba(0,0,0,.35);
  padding: 14px 14px;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  font-size: 12px;
  color: rgba(255,255,255,.82);
  overflow: auto;
  max-height: 240px;
}
.badge-ok{ color: var(--ok); }
.badge-warn{ color: var(--warn); }
.badge-err{ color: var(--err); }

.kv3{
  display:grid;
  grid-template-columns: repeat(3, minmax(0,1fr));
  gap: 12px;
  margin-top: 10px;
}
@media (max-width: 980px){
  .kv3{ grid-template-columns: 1fr; }
}
.kv3 .box{
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 12px 12px;
  background: rgba(255,255,255,.03);
}
.kv3 .box b{
  display:block;
  color: rgba(255,255,255,.90);
  margin-bottom: 6px;
}
</style>
""",
    unsafe_allow_html=True,
)


# =========================
# Helpers
# =========================
def _safe_list(x: Any) -> List[str]:
    return x if isinstance(x, list) else []


def _log_append(msg: str):
    st.session_state.setdefault("lab_log", [])
    st.session_state["lab_log"].append(msg)
    st.session_state["lab_log"] = st.session_state["lab_log"][-140:]


def _render_log():
    lines = st.session_state.get("lab_log", [])
    if not lines:
        lines = ["[system] ready."]

    safe_lines = []
    for line in lines:
        escaped = _html.escape(str(line))
        escaped = escaped.replace("&lt;span class=&#x27;badge-ok&#x27;&gt;", "<span class='badge-ok'>")
        escaped = escaped.replace("&lt;span class=&#x27;badge-warn&#x27;&gt;", "<span class='badge-warn'>")
        escaped = escaped.replace("&lt;span class=&#x27;badge-err&#x27;&gt;", "<span class='badge-err'>")
        escaped = escaped.replace("&lt;/span&gt;", "</span>")
        safe_lines.append(escaped)

    st.markdown("<div class='console'>" + "<br/>".join(safe_lines) + "</div>", unsafe_allow_html=True)


def _find_project(projects_list: List[Dict[str, Any]], pid: Optional[str]):
    if not pid:
        return None
    pid = str(pid).strip()
    for p in projects_list:
        if str(p.get("id", "")).strip() == pid:
            return p
    return None


def _abs_page(path: str) -> str:
    """
    Streamlit multipage on Community Cloud works reliably with absolute paths:
    '/', '/Projects', '/About_Me', '/Contact'
    """
    return path


# =========================
# Load YAML + query param
# =========================
ROOT = Path(__file__).parents[1]
YAML_PATH = ROOT / "data" / "projects.yaml"
projects = load_projects(YAML_PATH)

pid = st.query_params.get("project")
selected = _find_project(projects, pid)


# =========================
# Topbar (always)
# =========================
st.markdown(
    f"""
<div class="topbar">
  <div>
    <h1 style="margin:0;">Lab</h1>
    <div class="badge">From chaos to simplicity • recruiter-friendly proof</div>
  </div>
  <div class="navbtns">
    <a href="{_abs_page('/')}" target="_self">Home</a>
    <a href="{_abs_page('/About_Me')}" target="_self">About</a>
    <a href="{_abs_page('/Projects')}" target="_self">Projects</a>
    <a href="{_abs_page('/Contact')}" target="_self">Contact</a>
  </div>
</div>
<div class="hr"></div>
""",
    unsafe_allow_html=True,
)


# =========================
# If no project selected
# =========================
if not selected:
    if pid:
        st.warning(f"Project not found for project={pid}. Open from Projects → Open in Lab.")
    else:
        st.info("Open a project from **Projects → Open in Lab** to see its interactive demo.")
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    with st.expander("Output (optional)", expanded=False):
        _render_log()
    st.stop()


# =========================
# Project card
# =========================
title = selected.get("title", "Project")
tagline = selected.get("tagline", "")

industry = selected.get("industry", "")
ptype = selected.get("type", "")
impact = selected.get("impact_type", "")
tools = _safe_list(selected.get("tools"))
skills = _safe_list(selected.get("skills"))
links = selected.get("links", {}) if isinstance(selected.get("links", {}), dict) else {}
lab = selected.get("lab", {}) if isinstance(selected.get("lab", {}), dict) else {}

# Optional narrative fields (recommended)
chaos_txt = lab.get("chaos", "") or ""
simp_txt = lab.get("simplification", "") or ""
res_txt = lab.get("result", "") or ""

demo_asset = lab.get("demo_asset", "") or ""
mode = lab.get("mode", "") or ""


st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown(f"## {title}")
if tagline:
    st.caption(tagline)

pills = []
if industry:
    pills.append(f"<span class='pill'>Industry: {industry}</span>")
if ptype:
    pills.append(f"<span class='pill'>Type: {ptype}</span>")
if impact:
    pills.append(f"<span class='pill'>Impact: {impact}</span>")
if tools:
    pills.append(f"<span class='pill'>Tools: {', '.join(tools[:6])}</span>")
if skills:
    pills.append(f"<span class='pill'>Skills: {', '.join(skills[:4])}</span>")

if pills:
    st.markdown("<div class='pills'>" + "".join(pills) + "</div>", unsafe_allow_html=True)

btns = []
if links.get("github"):
    btns.append(("GitHub", links["github"]))
if links.get("colab"):
    btns.append(("Colab", links["colab"]))
if links.get("report"):
    btns.append(("Report", links["report"]))

if btns:
    html_btns = ["<div class='links'>"]
    for label, url in btns:
        html_btns.append(f"<a href='{url}' target='_blank'>{label} ↗</a>")
    html_btns.append("</div>")
    st.markdown("".join(html_btns), unsafe_allow_html=True)

# small dataset badge
if demo_asset:
    st.caption(f"Demo dataset: `{demo_asset}`")
else:
    st.caption("Demo dataset: (not configured yet)")

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

_log_append(f"<span class='badge-ok'>[project]</span> loaded: {selected.get('id','')}")


# =========================
# From chaos to simplicity (always visible)
# =========================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("### From chaos to simplicity")

# If YAML doesn't have the texts yet, show placeholders so you remember to fill them.
c1 = chaos_txt if chaos_txt else "Describe the messy reality (noise, constraints, seasonality, ambiguity)."
c2 = simp_txt if simp_txt else "Describe the simplification (features, model, evaluation, decision framing)."
c3 = res_txt if res_txt else "Describe the result (baseline improvement, stability, operational value)."

st.markdown(
    f"""
<div class="kv3">
  <div class="box"><b>The chaos</b><div>{c1}</div></div>
  <div class="box"><b>The simplification</b><div>{c2}</div></div>
  <div class="box"><b>The result</b><div>{c3}</div></div>
</div>
""",
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div class='hr'></div>", unsafe_allow_html=True)


# =========================
# Keep it simple (main CTA)
# =========================
st.markdown("### ▶️ Keep it simple")

# One single action. Everything else renders after click.
keep = st.button("Keep it simple", type="primary")

# Persist the run state so refresh doesn't wipe the view immediately
if keep:
    st.session_state["kis_ran"] = True
    _log_append("<span class='badge-ok'>[run]</span> keep it simple clicked.")

ran = bool(st.session_state.get("kis_ran", False))

if not ran:
    st.caption("Click **Keep it simple** to run the project demo (dataset + one proof-of-work view).")
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
else:
    # =========================
    # Load demo dataset (project-specific)
    # =========================
    df = None
    if demo_asset:
        demo_path = ROOT / demo_asset
        if demo_path.exists():
            try:
                df = pd.read_csv(demo_path)
                _log_append(f"<span class='badge-ok'>[data]</span> loaded demo: {demo_asset} ({len(df):,} rows)")
            except Exception as e:
                _log_append(f"<span class='badge-err'>[error]</span> failed reading demo_asset: {e}")
        else:
            _log_append(f"<span class='badge-warn'>[warn]</span> demo_asset not found: {demo_asset}")
    else:
        _log_append("<span class='badge-warn'>[warn]</span> no demo_asset configured in projects.yaml")

    if df is None:
        st.error("Demo dataset could not be loaded. Check `lab.demo_asset` path in projects.yaml.")
    else:
        # =========================
        # Proof of work (minimal placeholder)
        # Next step: swap this with Taxi-specific time-series demo.
        # =========================
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### Proof of work")
        st.caption("Minimal demo loaded. Next: project-specific chart + baseline vs model metric.")
        st.dataframe(df.head(12), use_container_width=True, height=280)

        # Simple chart: first numeric column over index (placeholder)
        num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
        if num_cols:
            y = num_cols[0]
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.plot(df[y].values[:200])
            ax.set_title(f"Quick view: {y}")
            st.pyplot(fig, clear_figure=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    # =========================
    # How I built it (optional)
    # =========================
    with st.expander("How I built it (optional)", expanded=False):
        if selected.get("approach"):
            st.markdown("**Approach**")
            st.write(selected.get("approach"))
        if selected.get("problem"):
            st.markdown("**Problem**")
            st.write(selected.get("problem"))
        if selected.get("results"):
            st.markdown("**Results**")
            st.write(selected.get("results"))
        if selected.get("details"):
            st.markdown("**Notes**")
            st.write(selected.get("details"))
        if not any(selected.get(k) for k in ["approach", "problem", "results", "details"]):
            st.caption("Add problem/approach/results/details in projects.yaml to enrich this section.")


# =========================
# Output log (optional)
# =========================
with st.expander("Output (optional)", expanded=False):
    _render_log()
