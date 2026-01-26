from __future__ import annotations

from pathlib import Path
import html as _html

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, Ridge

from src.loaders import load_projects


# =========================
# Page config
# =========================
st.set_page_config(page_title="Lab • Portfolio JRR", page_icon="🧪", layout="wide")


# =========================
# Paths
# =========================
ROOT = Path(__file__).parents[1]
YAML_PATH = ROOT / "data" / "projects.yaml"


# =========================
# Styles
# =========================
st.markdown(
    """
<style>
header[data-testid="stHeader"] {display:none;}
footer {visibility:hidden;}
.block-container { padding-top: 1.4rem; padding-bottom: 3rem; max-width: 1180px; }
a { text-decoration: none; }

:root{
  --fg: rgba(255,255,255,.92);
  --fg2: rgba(255,255,255,.72);
  --line: rgba(255,255255,.10);
  --card: rgba(255,255,255,.04);
  --ok: rgba(120,255,180,.95);
  --warn: rgba(255,210,120,.95);
  --err: rgba(255,120,140,.95);
}

html, body, [data-testid="stAppViewContainer"]{
  background: radial-gradient(1000px 620px at 50% 0%, rgba(255,255,255,.05), rgba(0,0,0,.98)) !important;
  color: var(--fg) !important;
}

.card{
  border: 1px solid var(--line);
  background: linear-gradient(180deg, var(--card), rgba(0,0,0,.16));
  border-radius: 18px;
  padding: 16px 16px;
  margin-bottom:12px;
}

.pill{
  display:inline-flex; align-items:center; gap:8px;
  padding: 7px 12px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: rgba(255,255,255,.03);
  color: rgba(255,255,255,.85);
  font-size: 12px;
}

.console{
  border: 1px solid var(--line);
  border-radius: 16px;
  background: rgba(0,0,0,.35);
  padding: 14px;
  font-family: ui-monospace, monospace;
  font-size: 12px;
  color: rgba(255,255,255,.82);
  overflow: auto;
  max-height: 260px;
}

.badge-ok{ color: var(--ok); }
.badge-warn{ color: var(--warn); }
.badge-err{ color: var(--err); }
</style>
""",
    unsafe_allow_html=True,
)


# =========================
# Utils
# =========================
def _log(msg: str):
    st.session_state.setdefault("lab_log", [])
    st.session_state["lab_log"].append(msg)
    st.session_state["lab_log"] = st.session_state["lab_log"][-150:]


def _render_log():
    lines = st.session_state.get("lab_log", []) or ["[system] ready."]
    safe = []
    for l in lines:
        e = _html.escape(str(l))
        e = e.replace("&lt;span class=&#x27;badge-ok&#x27;&gt;", "<span class='badge-ok'>")
        e = e.replace("&lt;span class=&#x27;badge-warn&#x27;&gt;", "<span class='badge-warn'>")
        e = e.replace("&lt;span class=&#x27;badge-err&#x27;&gt;", "<span class='badge-err'>")
        e = e.replace("&lt;/span&gt;", "</span>")
        safe.append(e)
    st.markdown("<div class='console'>" + "<br/>".join(safe) + "</div>", unsafe_allow_html=True)


def _numeric_cols(df):
    return [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]


def _cat_cols(df):
    return [c for c in df.columns if df[c].dtype == "object"]


# =========================
# Load projects + query
# =========================
projects = load_projects(YAML_PATH)
query_project = st.query_params.get("project")

selected = None
if query_project:
    for p in projects:
        if str(p.get("id","")).strip() == str(query_project).strip():
            selected = p
            break

if selected:
    _log(f"<span class='badge-ok'>[project]</span> loaded: {selected.get('id')}")
else:
    if query_project:
        _log(f"<span class='badge-warn'>[warn]</span> project not found: {query_project}")


def has_demo(p):
    if not p: return False
    demo = (p.get("lab", {}) or {}).get("demo_asset")
    if not demo: return False
    return (ROOT / demo).exists()


# =========================
# Top bar
# =========================
st.markdown("## 🧪 Lab — Project Sandbox")
st.markdown("---")


# =========================
# Project card + pill
# =========================
if selected:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"### {selected.get('title')}")
    st.caption(selected.get("tagline",""))

    meta = []
    for k in ["industry","type","impact_type","status","year"]:
        if selected.get(k):
            meta.append(f"<span class='pill'>{k.replace('_',' ').title()}: {selected[k]}</span>")

    st.markdown(" ".join(meta), unsafe_allow_html=True)

    if has_demo(selected):
        st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
        st.markdown("<span class='pill'>🧪 Project demo available</span>", unsafe_allow_html=True)

        if st.button("🧪 Open Project Demo"):
            st.session_state["data_mode"] = "project_demo"
            _log("<span class='badge-ok'>[ui]</span> switched to Project demo")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("Open a project from Projects → Open in Lab")


# =========================
# Data mode
# =========================
st.session_state.setdefault("data_mode", "demo")

# auto-load demo when coming from Projects
if selected and has_demo(selected) and "auto_loaded" not in st.session_state:
    st.session_state["data_mode"] = "project_demo"
    st.session_state["auto_loaded"] = True


# =========================
# Load data
# =========================
df = None
mode = st.session_state["data_mode"]

if mode == "project_demo" and selected and has_demo(selected):
    asset = selected["lab"]["demo_asset"]
    df = pd.read_csv(ROOT / asset)
    _log(f"<span class='badge-ok'>[data]</span> loaded project demo: {asset}")

elif mode == "demo":
    rng = np.random.default_rng(7)
    df = pd.DataFrame({
        "date": pd.date_range("2025-01-01", periods=400, freq="D"),
        "demand": rng.poisson(120, 400),
        "price": rng.normal(45, 6, 400),
        "marketing": rng.normal(1800, 300, 400)
    })
    _log("[data] demo dataset loaded")

elif mode == "upload":
    up = st.file_uploader("Upload CSV", type="csv")
    if up:
        df = pd.read_csv(up)
        _log(f"<span class='badge-ok'>[data]</span> loaded CSV: {up.name}")
    else:
        st.stop()


# =========================
# Data explorer
# =========================
st.markdown("## Data Explorer")
st.dataframe(df.head(40), use_container_width=True)
st.markdown("---")


# =========================
# Quick model
# =========================
st.markdown("## 🧪 Quick experiment")

targets = ["(none)"] + list(df.columns)
t = st.selectbox("Target column", targets)

if st.button("Run quick model") and t != "(none)":
    X = df.drop(columns=[t])
    y = df[t]
    num = _numeric_cols(X)
    cat = _cat_cols(X)

    pre = ColumnTransformer([
        ("num", Pipeline([("imp", SimpleImputer(strategy="median"))]), num),
        ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                          ("ohe", OneHotEncoder(handle_unknown="ignore"))]), cat)
    ])

    model = LogisticRegression(max_iter=1000) if y.nunique() < 20 else Ridge()
    pipe = Pipeline([("pre", pre), ("model", model)])

    Xtr,Xte,ytr,yte = train_test_split(X,y,test_size=0.25,random_state=42)
    pipe.fit(Xtr,ytr)
    pred = pipe.predict(Xte)

    if y.nunique() < 20:
        st.success(f"Accuracy: {accuracy_score(yte, np.round(pred)):.3f}")
    else:
        st.success(f"RMSE: {np.sqrt(mean_squared_error(yte,pred)):.2f}")


# =========================
# Console
# =========================
st.markdown("## Output log")
_render_log()
