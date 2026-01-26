# pages/Lab.py
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional
import html as _html
import io

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
# Minimalist premium styles
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
  --fg3: rgba(255,255,255,.56);
  --line: rgba(255,255,255,.10);
  --line2: rgba(255,255,255,.14);

  --glass: rgba(255,255,255,.045);
  --glass2: rgba(255,255,255,.06);

  --ok: rgba(120,255,180,.95);
  --warn: rgba(255,210,120,.95);
  --err: rgba(255,120,140,.95);
}

html, body, [data-testid="stAppViewContainer"]{
  background:
    radial-gradient(1100px 680px at 50% 0%, rgba(255,255,255,.06), rgba(0,0,0,.98)) !important;
  color: var(--fg) !important;
}

h1,h2,h3{ letter-spacing: -0.04em; }
p, li, small { color: var(--fg2); }

.hr{ height:1px; background: var(--line); margin: 16px 0 18px 0; }

.topbar{
  display:flex; align-items:flex-start; justify-content:space-between;
  gap: 12px;
  padding: 6px 0 6px 0;
}

.brandline{
  display:flex; flex-direction:column; gap:6px;
}
.brandline h1{
  margin:0;
  font-size: 34px;
  line-height: 1.05;
}
.subbadge{
  display:inline-flex; align-items:center; gap:10px;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: rgba(255,255,255,.03);
  color: rgba(255,255,255,.82);
  font-size: 12px;
}

.navbtns{ display:flex; gap:10px; flex-wrap:wrap; justify-content:flex-end; }
.navbtns a{
  display:inline-block;
  padding: 9px 12px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: rgba(255,255,255,.035);
  color: rgba(255,255,255,.88) !important;
  font-size: 13px;
  transition: transform .12s ease, background .12s ease, border-color .12s ease;
}
.navbtns a:hover{
  background: rgba(255,255,255,.075);
  border-color: var(--line2);
  transform: translateY(-1px);
}

.card{
  border: 1px solid var(--line);
  background: linear-gradient(180deg, var(--glass2), rgba(0,0,0,.20));
  border-radius: 18px;
  padding: 16px 16px;
  box-shadow: 0 10px 28px rgba(0,0,0,.35);
}

.card h2{
  margin: 0 0 2px 0;
  font-size: 22px;
}
.card .tagline{
  margin: 6px 0 0 0;
  color: var(--fg2);
  font-size: 14px;
  line-height: 1.35;
}

.pills{ display:flex; gap:8px; flex-wrap:wrap; margin-top: 10px; }
.pill{
  padding: 6px 9px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: rgba(0,0,0,.16);
  color: rgba(255,255,255,.78);
  font-size: 12px;
}

.links{
  margin-top: 10px;
}
.links a{
  display:inline-flex;
  align-items:center;
  gap:8px;
  padding: 8px 12px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: rgba(255,255,255,.04);
  color: rgba(255,255,255,.90) !important;
  margin-right: 8px;
  margin-top: 8px;
  font-size: 13px;
  transition: transform .12s ease, background .12s ease, border-color .12s ease;
}
.links a:hover{
  background: rgba(255,255,255,.08);
  border-color: var(--line2);
  transform: translateY(-1px);
}

.captionmono{
  color: var(--fg3);
  font-size: 12px;
  margin-top: 8px;
}

.sectiontitle{
  font-size: 16px;
  color: rgba(255,255,255,.90);
  margin: 0 0 10px 0;
}

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
  font-size: 13px;
}
.kv3 .box div{
  color: var(--fg2);
  font-size: 13px;
  line-height: 1.45;
}

.ctaHint{
  color: var(--fg3);
  font-size: 12px;
  margin-top: 6px;
}

/* Console */
.console{
  border: 1px solid var(--line);
  border-radius: 16px;
  background: rgba(0,0,0,.35);
  padding: 14px 14px;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  font-size: 12px;
  color: rgba(255,255,255,.82);
  overflow: auto;
  max-height: 220px;
}
.badge-ok{ color: var(--ok); }
.badge-warn{ color: var(--warn); }
.badge-err{ color: var(--err); }

/* DataScience-ish pre box (info/head) */
.dsbox{
  border: 1px solid var(--line);
  border-radius: 14px;
  background: rgba(0,0,0,.28);
  padding: 12px 12px;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  font-size: 12px;
  color: rgba(255,255,255,.84);
  overflow: auto;
  max-height: 220px;
}

/* Make Streamlit primary button look more premium */
div.stButton > button[kind="primary"]{
  border-radius: 14px !important;
  border: 1px solid rgba(255,255,255,.16) !important;
  background: linear-gradient(180deg, rgba(255,255,255,.10), rgba(255,255,255,.04)) !important;
  color: rgba(255,255,255,.92) !important;
  padding: 10px 14px !important;
  font-weight: 700 !important;
}
div.stButton > button[kind="primary"]:hover{
  border-color: rgba(255,255,255,.24) !important;
  background: linear-gradient(180deg, rgba(255,255,255,.14), rgba(255,255,255,.06)) !important;
  transform: translateY(-1px);
}

/* Slightly reduce plot padding */
div[data-testid="stPlotlyChart"], div[data-testid="stImage"], div[data-testid="stPyplot"]{
  margin-top: 0.2rem;
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


def _capture_df_info(df: pd.DataFrame) -> str:
    buf = io.StringIO()
    df.info(buf=buf)
    return buf.getvalue()


def _expected_answer_text(p: Dict[str, Any], df: pd.DataFrame) -> str:
    """
    Recruiter-friendly 2–3 lines, grounded in YAML if present.
    If YAML has problem/approach/results, use them; else provide a safe default.
    """
    problem = (p.get("problem") or "").strip()
    approach = (p.get("approach") or "").strip()
    results = (p.get("results") or "").strip()

    # fallback (minimal + DS tone)
    if not (problem or approach or results):
        rows, cols = df.shape
        return (
            "Built a reproducible forecasting workflow to turn noisy ride demand into a usable planning signal. "
            f"Loaded a clean modeling table ({rows:,} rows × {cols} cols), then validated performance with time-aware evaluation. "
            "Outcome: a simple, operational view to forecast short-horizon demand and support staffing/capacity decisions."
        )

    # keep it short + scannable
    parts = []
    if problem:
        parts.append(f"**Problem:** {problem}")
    if approach:
        parts.append(f"**How:** {approach}")
    if results:
        parts.append(f"**Result:** {results}")
    return "\n".join(parts)


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
    """
<div class="topbar">
  <div class="brandline">
    <h1>Lab</h1>
    <div class="subbadge">From chaos to simplicity • recruiter-friendly proof</div>
  </div>
  <div class="navbtns">
    <a href="/" target="_self">Home</a>
    <a href="/About_Me" target="_self">About</a>
    <a href="/Projects" target="_self">Projects</a>
    <a href="/Contact" target="_self">Contact</a>
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

chaos_txt = lab.get("chaos", "") or ""
simp_txt = lab.get("simplification", "") or ""
res_txt = lab.get("result", "") or ""

demo_asset = lab.get("demo_asset", "") or ""

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown(f"<h2>{_html.escape(title)}</h2>", unsafe_allow_html=True)
if tagline:
    st.markdown(f"<div class='tagline'>{_html.escape(tagline)}</div>", unsafe_allow_html=True)

pills = []
if industry:
    pills.append(f"<span class='pill'>Industry: {_html.escape(industry)}</span>")
if ptype:
    pills.append(f"<span class='pill'>Type: {_html.escape(ptype)}</span>")
if impact:
    pills.append(f"<span class='pill'>Impact: {_html.escape(impact)}</span>")
if tools:
    pills.append(f"<span class='pill'>Tools: {_html.escape(', '.join(tools[:6]))}</span>")
if skills:
    pills.append(f"<span class='pill'>Skills: {_html.escape(', '.join(skills[:4]))}</span>")

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

if demo_asset:
    st.markdown(f"<div class='captionmono'>Demo dataset: <code>{_html.escape(demo_asset)}</code></div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='captionmono'>Demo dataset: (not configured yet)</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

_log_append(f"<span class='badge-ok'>[project]</span> loaded: {selected.get('id','')}")


# =========================
# From chaos to simplicity (always visible)
# =========================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='sectiontitle'>From chaos to simplicity</div>", unsafe_allow_html=True)

c1 = chaos_txt if chaos_txt else "Messy demand: seasonality, spikes, noise, and operational constraints."
c2 = simp_txt if simp_txt else "Feature engineering + model baselines + time-aware evaluation."
c3 = res_txt if res_txt else "A stable short-horizon forecast signal for planning decisions."

st.markdown(
    f"""
<div class="kv3">
  <div class="box"><b>The chaos</b><div>{_html.escape(c1)}</div></div>
  <div class="box"><b>The simplification</b><div>{_html.escape(c2)}</div></div>
  <div class="box"><b>The result</b><div>{_html.escape(c3)}</div></div>
</div>
""",
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div class='hr'></div>", unsafe_allow_html=True)


# =========================
# Keep it simple (main CTA)
# =========================
st.markdown("<div class='sectiontitle'>▶️ Keep it simple</div>", unsafe_allow_html=True)
keep = st.button("Keep it simple", type="primary")

if keep:
    st.session_state["kis_ran"] = True
    _log_append("<span class='badge-ok'>[run]</span> keep it simple clicked.")

ran = bool(st.session_state.get("kis_ran", False))

if not ran:
    st.markdown("<div class='ctaHint'>One click → load demo → show a tiny DS proof (head + info + small chart).</div>", unsafe_allow_html=True)
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
        # Minimal Proof of Work (head + info + small chart)
        # =========================
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='sectiontitle'>Proof of work</div>", unsafe_allow_html=True)

        # 1) df.head(5)
        st.markdown("<div class='captionmono'>df.head(5)</div>", unsafe_allow_html=True)
        st.dataframe(df.head(5), use_container_width=True, height=150)

        # 2) df.info() captured output (looks like terminal)
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        st.markdown("<div class='captionmono'>df.info()</div>", unsafe_allow_html=True)
        info_txt = _capture_df_info(df)
        st.markdown(f"<div class='dsbox'>{_html.escape(info_txt).replace('\\n','<br/>')}</div>", unsafe_allow_html=True)

        # 3) tiny chart (just visual)
        num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
        if num_cols:
            y = num_cols[0]
            st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
            st.markdown("<div class='captionmono'>tiny visual (example)</div>", unsafe_allow_html=True)

            fig = plt.figure(figsize=(5.8, 2.0))  # smaller
            ax = fig.add_subplot(111)
            vals = df[y].values[:200]
            ax.plot(vals)
            ax.set_title(f"{y}", fontsize=10)
            ax.tick_params(axis="both", labelsize=8)
            ax.set_xlabel("")
            ax.set_ylabel("")
            fig.tight_layout(pad=0.6)
            st.pyplot(fig, clear_figure=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # =========================
        # Expected answer (recruiter response)
        # =========================
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='sectiontitle'>What this model solved</div>", unsafe_allow_html=True)
        st.write(_expected_answer_text(selected, df))
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    with st.expander("How I built it (optional)", expanded=False):
        shown = False
        for key, label in [("problem", "Problem"), ("approach", "Approach"), ("results", "Results"), ("details", "Notes")]:
            val = (selected.get(key) or "").strip()
            if val:
                st.markdown(f"**{label}**")
                st.write(val)
                shown = True
        if not shown:
            st.caption("Add problem/approach/results/details in projects.yaml to enrich this section.")


with st.expander("Output (optional)", expanded=False):
    _render_log()
