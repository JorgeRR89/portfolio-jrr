from __future__ import annotations

from pathlib import Path
from io import StringIO
import textwrap

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import yaml

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


# =========================
# Page config
# =========================
st.set_page_config(page_title="Lab • Portfolio JRR", page_icon="🧪", layout="wide")


# =========================
# Premium minimal styles
# =========================
st.markdown(
    """
<style>
header[data-testid="stHeader"] {display:none;}
footer {visibility:hidden;}
.block-container { padding-top: 1.6rem; padding-bottom: 3.2rem; max-width: 1100px; }

:root{
  --fg: rgba(255,255,255,.92);
  --fg2: rgba(255,255,255,.70);
  --line: rgba(255,255,255,.10);
  --card: rgba(255,255,255,.04);
  --card2: rgba(255,255,255,.06);
  --shadow: rgba(0,0,0,.35);
  --accent: rgba(255, 80, 90, .95);
}

html, body, [data-testid="stAppViewContainer"]{
  background:
    radial-gradient(900px 520px at 50% 0%, rgba(255,255,255,.06), rgba(0,0,0,.98)) !important;
  color: var(--fg) !important;
}

h1,h2,h3{ letter-spacing:-0.03em; }
p, li, small { color: var(--fg2); }
a { text-decoration: none !important; }

.hr{ height:1px; background: var(--line); margin: 16px 0 22px 0; }

.topbar{
  display:flex; align-items:flex-start; justify-content:space-between;
  gap: 12px;
  padding: 8px 0 8px 0;
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

.hero{
  border: 1px solid rgba(255,255,255,.12);
  background: linear-gradient(180deg, rgba(255,255,255,.06), rgba(0,0,0,.22));
  border-radius: 22px;
  padding: 20px 20px;
  box-shadow: 0 20px 60px var(--shadow);
}
.subtitle{
  color: rgba(255,255,255,.70);
  margin-top: 6px;
  font-size: 14px;
  line-height: 1.4;
}
.micro{
  margin-top: 10px;
  display:inline-flex;
  align-items:center;
  gap: 8px;
  padding: 7px 10px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: rgba(0,0,0,.25);
  font-size: 12px;
  color: rgba(255,255,255,.78);
}

.card{
  border: 1px solid var(--line);
  background: linear-gradient(180deg, var(--card), rgba(0,0,0,.18));
  border-radius: 18px;
  padding: 16px 16px;
  box-shadow: 0 18px 50px var(--shadow);
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

.kpi{
  display:grid;
  grid-template-columns: repeat(4, minmax(0,1fr));
  gap: 10px;
}
.kpi .k{
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 12px 12px;
  background: rgba(255,255,255,.03);
}
.kpi .k b{ font-size: 16px; color: rgba(255,255,255,.92); }
.kpi .k span{ display:block; margin-top: 2px; font-size: 12px; color: rgba(255,255,255,.68); }
@media (max-width: 920px){
  .kpi{ grid-template-columns: 1fr 1fr; }
}
@media (max-width: 640px){
  .kpi{ grid-template-columns: 1fr; }
}

.dsbox{
  border: 1px solid rgba(255,255,255,.10);
  border-radius: 16px;
  background: rgba(0,0,0,.35);
  padding: 14px 14px;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono","Courier New", monospace;
  font-size: 12px;
  color: rgba(255,255,255,.84);
  overflow:auto;
  max-height: 310px;
}
.dslabel{
  font-size: 12px;
  color: rgba(255,255,255,.62);
  margin-bottom: 8px;
}

.resultok{
  border: 1px solid rgba(120,255,180,.25);
  background: linear-gradient(180deg, rgba(120,255,180,.08), rgba(0,0,0,.20));
}
.resultwarn{
  border: 1px solid rgba(255,210,120,.25);
  background: linear-gradient(180deg, rgba(255,210,120,.08), rgba(0,0,0,.20));
}

.smallhint{ color: rgba(255,255,255,.60); font-size: 12px; }

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

/* Make primary button feel premium */
div[data-testid="stButton"] button[kind="primary"]{
  background: var(--accent) !important;
  border: 1px solid rgba(255,255,255,.12) !important;
  border-radius: 14px !important;
  padding: 10px 14px !important;
  box-shadow: 0 14px 40px rgba(0,0,0,.35) !important;
}
div[data-testid="stButton"] button[kind="primary"]:hover{
  filter: brightness(1.02);
}

/* Secondary buttons */
div[data-testid="stButton"] button[kind="secondary"]{
  border-radius: 999px !important;
  border: 1px solid var(--line) !important;
  background: rgba(255,255,255,.04) !important;
}

</style>
""",
    unsafe_allow_html=True,
)


# =========================
# YAML loading (direct, robust)
# =========================
def load_yaml_dict(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data if isinstance(data, dict) else {}


def load_projects_raw(path: Path) -> list[dict]:
    data = load_yaml_dict(path)
    projects = data.get("projects", [])
    return projects if isinstance(projects, list) else []


def find_project(projects: list[dict], pid: str | None) -> dict | None:
    if not pid:
        return None
    pid = str(pid).strip()
    for p in projects:
        if str(p.get("id", "")).strip() == pid:
            return p
    return None


# =========================
# Time-series demo helpers
# =========================
def infer_datetime_col(df: pd.DataFrame) -> str | None:
    # Prefer common names
    candidates = ["datetime", "date", "timestamp", "time"]
    cols = [c for c in df.columns]
    for name in candidates:
        for c in cols:
            if name in str(c).lower():
                try:
                    pd.to_datetime(df[c], errors="raise")
                    return c
                except Exception:
                    pass
    # fallback: try any col
    for c in cols:
        try:
            pd.to_datetime(df[c], errors="raise")
            return c
        except Exception:
            continue
    return None


def infer_target_col(df: pd.DataFrame) -> str | None:
    # Your typical taxi dataset uses num_orders
    preferred = ["num_orders", "demand", "demand_units", "target"]
    for c in preferred:
        if c in df.columns:
            return c
    # fallback: first numeric column
    num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    return num_cols[0] if num_cols else None


def make_features(ts: pd.Series, max_lag: int = 24, roll: int = 24) -> pd.DataFrame:
    """
    ts: hourly series
    returns dataframe with calendar + lag + rolling features + target y
    """
    df = pd.DataFrame({"y": ts})
    idx = df.index

    df["year"] = idx.year
    df["month"] = idx.month
    df["day"] = idx.day
    df["hour"] = idx.hour
    df["dayofweek"] = idx.dayofweek

    for lag in range(1, max_lag + 1):
        df[f"lag_{lag}"] = df["y"].shift(lag)

    df[f"rolling_mean_{roll}"] = df["y"].shift(1).rolling(roll).mean()
    df = df.dropna()
    return df


def time_split(df: pd.DataFrame, train_frac: float = 0.9):
    cut = int(len(df) * train_frac)
    train = df.iloc[:cut]
    test = df.iloc[cut:]
    return train, test


def rmse(y_true, y_pred) -> float:
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))


def to_info_text(df: pd.DataFrame) -> str:
    buf = StringIO()
    df.info(buf=buf)
    return buf.getvalue()


def small_series_plot(ts: pd.Series, title: str = "Hourly demand (sample view)"):
    fig = plt.figure(figsize=(7.2, 2.4), dpi=140)
    ax = fig.add_subplot(111)
    ax.plot(ts.index, ts.values)
    ax.set_title(title, fontsize=10)
    ax.tick_params(axis="x", labelrotation=0)
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    return fig


# =========================
# Paths + query param
# =========================
ROOT = Path(__file__).parents[1]
YAML_PATH = ROOT / "data" / "projects.yaml"
projects = load_projects_raw(YAML_PATH)

project_q = st.query_params.get("project")
selected = find_project(projects, project_q)


# =========================
# Top bar (navigation)
# =========================
st.markdown(
    """
<div class="topbar">
  <div style="max-width: 720px;">
    <h1 style="margin:0;">Lab</h1>
    <div class="subtitle">Recruiter-friendly demos: small proof, clear outcome, optional deep dive.</div>
  </div>
  <div class="navbtns">
    <a href="./" target="_self">← Home</a>
    <a href="./About_Me" target="_self">About</a>
    <a href="./Projects" target="_self">Projects</a>
    <a href="./Contact" target="_self">Contact</a>
  </div>
</div>
<div class="hr"></div>
""",
    unsafe_allow_html=True,
)


# =========================
# If no project selected: keep it simple
# =========================
if not selected:
    st.markdown(
        """
<div class="hero">
  <h2 style="margin:0;">From chaos to simplicity.</h2>
  <div class="subtitle">
    Open this Lab from <b>Projects → Open in Lab</b> to load a project demo dataset and run a minimal proof-of-work.
  </div>
  <div class="micro">Tip: the URL should look like <code>?project=taxi_demand</code></div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.stop()


# =========================
# Project hero
# =========================
title = selected.get("title", "Project Lab")
tagline = selected.get("tagline", "")
industry = selected.get("industry", "")
ptype = selected.get("type", "")
impact_type = selected.get("impact_type", "")
year = selected.get("year", "")
status = selected.get("status", "")
links = selected.get("links", {}) or {}
tools = selected.get("tools", []) if isinstance(selected.get("tools"), list) else []
skills = selected.get("skills", []) if isinstance(selected.get("skills"), list) else []

st.markdown(
    f"""
<div class="hero">
  <div style="display:flex; justify-content:space-between; gap: 14px; flex-wrap:wrap;">
    <div style="min-width: 280px; flex: 1;">
      <h2 style="margin:0;">{title}</h2>
      <div class="subtitle">{tagline}</div>
      <div class="micro">From chaos to simplicity</div>
    </div>
    <div style="min-width: 280px;">
      <div class="pills">
        {f"<span class='pill'>Industry: {industry}</span>" if industry else ""}
        {f"<span class='pill'>Type: {ptype}</span>" if ptype else ""}
        {f"<span class='pill'>Impact: {impact_type}</span>" if impact_type else ""}
        {f"<span class='pill'>Status: {status}</span>" if status else ""}
        {f"<span class='pill'>Year: {year}</span>" if year else ""}
        {f"<span class='pill'>Tools: {', '.join(tools[:6])}</span>" if tools else ""}
        {f"<span class='pill'>Skills: {', '.join(skills[:4])}</span>" if skills else ""}
      </div>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# Links row
btns = []
if links.get("github"):
    btns.append(("GitHub", links["github"]))
if links.get("report"):
    btns.append(("Report", links["report"]))
if links.get("demo"):
    btns.append(("Demo", links["demo"]))
if links.get("colab"):
    btns.append(("Colab", links["colab"]))

if btns:
    html_btns = ["<div class='links'>"]
    for label, url in btns:
        html_btns.append(f"<a href='{url}' target='_blank'>{label} ↗</a>")
    html_btns.append("</div>")
    st.markdown("".join(html_btns), unsafe_allow_html=True)

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)


# =========================
# Load demo asset
# =========================
lab_cfg = selected.get("lab", {}) or {}
demo_asset = lab_cfg.get("demo_asset", "")
demo_path = (ROOT / demo_asset) if demo_asset else None

if not demo_asset or demo_path is None or not demo_path.exists():
    st.markdown(
        f"""
<div class="card resultwarn">
  <h3 style="margin-top:0;">Dataset not found</h3>
  <div class="subtitle">
    This project doesn’t have a valid <code>lab.demo_asset</code> path in <code>data/projects.yaml</code>.
  </div>
  <div class="subtitle"><b>Expected:</b> <code>lab: demo_asset: "data/lab/taxi_demo.csv"</code></div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.stop()

# Load CSV (cached-ish via session)
@st.cache_data(show_spinner=False)
def _load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

df_raw = _load_csv(str(demo_path))


# =========================
# Minimal KPIs (always)
# =========================
n_rows, n_cols = df_raw.shape
n_missing = int(df_raw.isna().sum().sum())
n_num = sum(pd.api.types.is_numeric_dtype(df_raw[c]) for c in df_raw.columns)

st.markdown(
    f"""
<div class="kpi">
  <div class="k"><b>{n_rows:,}</b><span>rows</span></div>
  <div class="k"><b>{n_cols}</b><span>columns</span></div>
  <div class="k"><b>{n_num}</b><span>numeric</span></div>
  <div class="k"><b>{n_missing:,}</b><span>missing cells</span></div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)


# =========================
# Keep it simple (single action)
# =========================
st.markdown("## ▶️ Keep it simple")
st.markdown("<div class='smallhint'>One click. Small proof. Clear outcome. Optional deep dive.</div>", unsafe_allow_html=True)

# Button row
cA, cB = st.columns([1, 3], gap="large")
with cA:
    run = st.button("Keep it simple", type="primary", use_container_width=True)

with cB:
    st.markdown(
        "<div class='smallhint'>This runs a minimal time-series pipeline: resample hourly → feature engineering (lags/rolling/calendar) → train → evaluate (RMSE).</div>",
        unsafe_allow_html=True,
    )

# Persist outputs so page doesn't feel empty after rerun
st.session_state.setdefault("lab_ran", False)
st.session_state.setdefault("lab_payload", {})

if run:
    st.session_state["lab_ran"] = True

    # --- Prepare data as a time series
    df = df_raw.copy()
    dt_col = infer_datetime_col(df)
    y_col = infer_target_col(df)

    payload = {"ok": False}

    if not dt_col or not y_col:
        payload["error"] = "Could not infer datetime column or target column."
        st.session_state["lab_payload"] = payload
    else:
        df[dt_col] = pd.to_datetime(df[dt_col], errors="coerce")
        df = df.dropna(subset=[dt_col])
        df = df.sort_values(dt_col)

        # Build hourly series
        ts = (
            df.set_index(dt_col)[y_col]
            .resample("H")
            .sum()
            .astype(float)
        )

        # Feature engineering
        feat = make_features(ts, max_lag=24, roll=24)
        train, test = time_split(feat, train_frac=0.9)

        X_train = train.drop(columns=["y"])
        y_train = train["y"]
        X_test = test.drop(columns=["y"])
        y_test = test["y"]

        # Baseline: Linear Regression
        lr = LinearRegression()
        lr.fit(X_train, y_train)
        pred_lr = lr.predict(X_test)
        rmse_lr = rmse(y_test, pred_lr)

        # Stronger: Random Forest (kept small for fast demo)
        rf = RandomForestRegressor(
            n_estimators=120,
            random_state=42,
            n_jobs=-1,
            max_depth=None,
            min_samples_leaf=2,
        )
        rf.fit(X_train, y_train)
        pred_rf = rf.predict(X_test)
        rmse_rf = rmse(y_test, pred_rf)

        best_name, best_rmse = ("Random Forest", rmse_rf) if rmse_rf <= rmse_lr else ("Linear Regression", rmse_lr)

        payload.update(
            {
                "ok": True,
                "dt_col": dt_col,
                "y_col": y_col,
                "ts": ts,
                "rmse_lr": float(rmse_lr),
                "rmse_rf": float(rmse_rf),
                "best_name": best_name,
                "best_rmse": float(best_rmse),
                "head5": df_raw.head(5),
                "info": to_info_text(df_raw),
            }
        )
        st.session_state["lab_payload"] = payload


# =========================
# Render outputs (only after run)
# =========================
if st.session_state["lab_ran"]:
    payload = st.session_state.get("lab_payload", {})
    if not payload.get("ok"):
        st.markdown(
            f"""
<div class="card resultwarn">
  <h3 style="margin-top:0;">Could not run the demo</h3>
  <div class="subtitle">{payload.get("error","Unknown error")}</div>
</div>
""",
            unsafe_allow_html=True,
        )
    else:
        # Proof of work: head + info
        st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
        st.markdown("### Proof of work (minimal)")

        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='dslabel'>df.head(5)</div>", unsafe_allow_html=True)
            st.dataframe(payload["head5"], use_container_width=True, height=220)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='dslabel'>df.info()</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='dsbox'>{payload['info'].replace(chr(10), '<br/>')}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Small visual
        st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
        st.markdown("### Tiny visual (example)")
        ts = payload["ts"]
        fig = small_series_plot(ts.tail(min(len(ts), 24 * 21)), title=f"Hourly {payload['y_col']} (last ~3 weeks)")
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.pyplot(fig, clear_figure=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Result: recruiter-friendly expected outcome
        st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
        st.markdown("### Result (expected outcome)")

        st.markdown(
            f"""
<div class="card resultok">
  <h3 style="margin-top:0;">✅ What did the model solve?</h3>
  <div class="subtitle">
    The pipeline converted raw time data into an hourly forecasting system and learned short-term demand patterns
    (seasonality + recent history) using simple lag/rolling features.
  </div>
  <div class="subtitle" style="margin-top:10px;">
    <b>Best model (demo):</b> {payload["best_name"]} &nbsp;•&nbsp; <b>RMSE:</b> {payload["best_rmse"]:.2f}
    <br/>
    <span style="color:rgba(255,255,255,.65); font-size:12px;">
      Baseline LR RMSE: {payload["rmse_lr"]:.2f} &nbsp;|&nbsp; Random Forest RMSE: {payload["rmse_rf"]:.2f}
    </span>
  </div>
  <div class="subtitle" style="margin-top:12px;">
    <b>Operational meaning:</b> this turns historical orders into a planning signal to anticipate peaks and support staffing decisions.
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        # System summary (business + systems)
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        st.markdown(
            """
<div class="card">
  <h3 style="margin-top:0;">🧠 What this system does</h3>
  <ul>
    <li>Structures raw timestamps into an hourly time-series</li>
    <li>Captures trend + seasonality + short-term dependency via calendar, lag and rolling features</li>
    <li>Produces short-horizon forecasts usable for operational planning</li>
    <li>Evaluates on future (holdout) data using RMSE</li>
  </ul>
  <h3 style="margin-top:12px;">🎯 Business impact</h3>
  <ul>
    <li>Anticipate peak hours</li>
    <li>Reduce idle capacity</li>
    <li>Support airport operations</li>
    <li>Enable near real-time planning systems</li>
  </ul>
</div>
""",
            unsafe_allow_html=True,
        )


# =========================
# How I built it (optional)
# =========================
st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

with st.expander("How I built it (optional)"):
    st.markdown(
        """
### Problem framing
Operations need reliable short-horizon demand forecasts to plan staffing efficiently, especially around airport peaks.

### Data preparation
- Parse timestamps and enforce chronological order  
- Convert events into an hourly time-series (resampling)  
- Validate missing values, duplicates and data types  

### Exploratory analysis
- Trend over time (growth/decline)  
- Seasonality by hour of day and day of week  
- Volatility and demand spikes  

### Feature engineering (why this approach)
Time-series forecasting often improves by encoding *recent history* and *calendar structure*:
- **Calendar features** (hour, day-of-week, month) capture recurring patterns  
- **Lag features** capture autocorrelation (recent demand influences next hour)  
- **Rolling mean** stabilizes short-term noise and provides a local baseline  

This is a strong, interpretable baseline before moving to heavier models.

### Modeling strategy
- Start with a simple regression baseline (Linear Regression)  
- Compare against a non-linear model (Random Forest) for richer interactions  
- Use a time-based holdout split (future data as test) to avoid leakage  

### Evaluation
Primary metric: **RMSE** on the holdout set  
- Lower RMSE = better average error in hourly order predictions  
- Time-based split ensures the evaluation mimics production usage

### Outcome → operational decision
The output is a forecasting signal used to plan:
- driver availability  
- capacity allocation during peak hours  
- operational response to demand spikes
"""
    )


# =========================
# Bottom navigation
# =========================
st.markdown(
    """
<div class="hr"></div>
<div class="navbtns">
  <a href="./" target="_self">← Back to Home</a>
  <a href="./About_Me" target="_self">About</a>
  <a href="./Projects" target="_self">Projects</a>
  <a href="./Contact" target="_self">Contact</a>
</div>
""",
    unsafe_allow_html=True,
)
