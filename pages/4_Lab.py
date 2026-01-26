from pathlib import Path
import io
import html as _html

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
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
# Styles (console / lab)
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
  --line: rgba(255,255,255,.10);
  --card: rgba(255,255,255,.04);
  --card2: rgba(0,0,0,.22);
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

.console{
  border: 1px solid var(--line);
  border-radius: 16px;
  background: rgba(0,0,0,.35);
  padding: 14px 14px;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  font-size: 12px;
  color: rgba(255,255,255,.82);
  overflow: auto;
  max-height: 260px;
}
.badge-ok{ color: var(--ok); }
.badge-warn{ color: var(--warn); }
.badge-err{ color: var(--err); }

.pill{
  display:inline-flex; align-items:center; gap:8px;
  padding: 7px 10px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: rgba(255,255,255,.03);
  color: rgba(255,255,255,.80);
  font-size: 12px;
}
.pills{ display:flex; gap:8px; flex-wrap:wrap; margin-top: 10px; }
.pill2{
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
</style>
""",
    unsafe_allow_html=True,
)


# =========================
# Helpers: project id match
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
        return str(pid)
    return slugify(p.get("title", "project"))


def find_project(projects: list[dict], q: str | None) -> dict | None:
    if not q:
        return None
    q = str(q).strip().lower()

    # 1) match direct id
    for p in projects:
        if str(p.get("id", "")).strip().lower() == q and p.get("id"):
            return p

    # 2) match slug(title)
    for p in projects:
        if slugify(p.get("title", "")) == q:
            return p

    # 3) contains match title (fallback)
    for p in projects:
        if q and q in str(p.get("title", "")).lower():
            return p

    return None


# =========================
# Helpers: columns
# =========================
def _numeric_cols(df: pd.DataFrame):
    return [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]


def _cat_cols(df: pd.DataFrame):
    return [c for c in df.columns if (df[c].dtype == "object" or pd.api.types.is_categorical_dtype(df[c]))]


def _infer_time_col(df: pd.DataFrame):
    for c in df.columns:
        if "date" in c.lower() or "time" in c.lower() or "timestamp" in c.lower():
            try:
                _ = pd.to_datetime(df[c], errors="raise")
                return c
            except Exception:
                pass
    return None


def _demo_dataset(seed: int = 7, n: int = 900) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2025-01-01", periods=n, freq="D")
    channel = rng.choice(["Amazon", "Mercado Libre", "Direct", "Wholesale"], size=n, p=[0.34, 0.38, 0.18, 0.10])
    region = rng.choice(["North", "Central", "South"], size=n, p=[0.32, 0.43, 0.25])

    price = np.clip(rng.normal(45, 12, size=n), 10, None)
    marketing = np.clip(rng.normal(1800, 650, size=n), 200, None)
    lead_time = np.clip(rng.normal(4.5, 2.0, size=n), 0.5, None)

    demand = (
        120
        + (region == "Central") * 12
        + (channel == "Mercado Libre") * 18
        - 0.85 * price
        + 0.006 * marketing
        - 2.6 * lead_time
        + rng.normal(0, 9, size=n)
    )

    demand = np.clip(demand, 5, None)

    cost = np.clip(rng.normal(26, 7, size=n), 6, None)
    profit = (price - cost) * demand - 0.15 * marketing

    risk_score = (
        0.35 * (lead_time / (lead_time.max() + 1e-9))
        + 0.25 * (price / (price.max() + 1e-9))
        + 0.40 * (rng.random(n))
    )
    risk_score = (risk_score * 100).round(2)

    profitable = (profit > np.percentile(profit, 55)).astype(int)

    df = pd.DataFrame(
        {
            "date": dates,
            "channel": channel,
            "region": region,
            "price": price.round(2),
            "marketing_spend": marketing.round(0),
            "lead_time_days": lead_time.round(2),
            "demand_units": demand.round(0),
            "profit": profit.round(2),
            "risk_score": risk_score,
            "profitable": profitable,
        }
    )

    miss_idx = rng.choice(np.arange(n), size=int(n * 0.03), replace=False)
    df.loc[miss_idx, "lead_time_days"] = np.nan

    return df


# =========================
# Output log (safe)
# =========================
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


# =========================
# Auto insights
# =========================
def auto_insights(df: pd.DataFrame):
    insights = []
    tables = {}
    figs = []

    nums = _numeric_cols(df)
    cats = _cat_cols(df)
    time_col = _infer_time_col(df)

    insights.append(f"• Rows: {len(df):,} | Columns: {df.shape[1]}")

    missing = (df.isna().mean() * 100).sort_values(ascending=False)
    missing = missing[missing > 0].round(2)
    if len(missing) > 0:
        insights.append(f"• Missing data detected in {len(missing)} column(s).")
        tables["missing_%"] = missing.reset_index().rename(columns={"index": "column", 0: "missing_%"} if 0 in missing.reset_index().columns else {})
    else:
        insights.append("• No missing data detected.")

    profit_col = None
    if "profit" in df.columns:
        profit_col = "profit"
    elif "demand" in df.columns:
        profit_col = "demand"
    elif nums:
        profit_col = nums[0]

    if profit_col and len(nums) >= 2 and profit_col in df.columns:
        corr = df[nums].corr(numeric_only=True)[profit_col].drop(index=profit_col).sort_values(ascending=False)
        if len(corr) > 0:
            top = corr.iloc[0]
            low = corr.iloc[-1]
            insights.append(f"• Strongest positive driver of {profit_col}: {top.name} (ρ={top:.2f})")
            insights.append(f"• Strongest negative driver of {profit_col}: {low.name} (ρ={low:.2f})")
            tables["correlation_with_" + profit_col] = corr.reset_index().rename(columns={"index": "feature", profit_col: "correlation"})

            fig = plt.figure()
            ax = fig.add_subplot(111)
            topn = corr.head(8)
            ax.bar(topn.index, topn.values)
            ax.set_title(f"Top correlations with {profit_col}")
            ax.tick_params(axis="x", rotation=25)
            figs.append(fig)

    if profit_col and cats and profit_col in df.columns:
        gcol = cats[0]
        g = df.groupby(gcol)[profit_col].mean().sort_values(ascending=False)
        if len(g) >= 2:
            insights.append(f"• Best {gcol}: {g.index[0]} (avg {profit_col}: {g.iloc[0]:,.2f})")
            insights.append(f"• Worst {gcol}: {g.index[-1]} (avg {profit_col}: {g.iloc[-1]:,.2f})")
        tables[f"mean_{profit_col}_by_{gcol}"] = g.reset_index().rename(columns={profit_col: f"mean_{profit_col}"})

    if profit_col and time_col and profit_col in df.columns:
        try:
            tmp = df.copy()
            tmp[time_col] = pd.to_datetime(tmp[time_col], errors="coerce")
            tmp = tmp.dropna(subset=[time_col])
            if not tmp.empty:
                # monthly mean
                t = tmp.groupby(tmp[time_col].dt.to_period("M"))[profit_col].mean()
                if len(t) >= 2:
                    delta = t.iloc[-1] - t.iloc[0]
                    insights.append(f"• {profit_col} trend: {'upward' if delta>0 else 'downward'} ({delta:,.1f})")

                fig = plt.figure()
                ax = fig.add_subplot(111)
                ax.plot(t.index.astype(str), t.values, marker="o")
                ax.set_title(f"{profit_col} trend (monthly)")
                ax.tick_params(axis="x", rotation=25)
                figs.append(fig)
        except Exception:
            pass

    return insights, tables, figs


# =========================
# Quick model
# =========================
def build_quick_model(df: pd.DataFrame, target: str):
    X = df.drop(columns=[target])
    y = df[target]

    num_cols = _numeric_cols(X)
    cat_cols = _cat_cols(X)

    y_unique = pd.Series(y.dropna().unique())
    is_classification = False
    if pd.api.types.is_bool_dtype(y) or (pd.api.types.is_integer_dtype(y) and y_unique.nunique() <= 20):
        is_classification = True

    pre = ColumnTransformer(
        transformers=[
            ("num", Pipeline(steps=[("imputer", SimpleImputer(strategy="median"))]), num_cols),
            ("cat", Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("ohe", OneHotEncoder(handle_unknown="ignore")),
            ]), cat_cols),
        ],
        remainder="drop",
    )

    model = LogisticRegression(max_iter=1200) if is_classification else Ridge(alpha=1.0)
    pipe = Pipeline(steps=[("pre", pre), ("model", model)])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.24, random_state=42)

    pipe.fit(X_train, y_train)
    pred = pipe.predict(X_test)

    metrics = {}
    if is_classification:
        pred_bin = np.round(pred).astype(int)
        y_test_bin = pd.Series(y_test).astype(int)
        metrics["task"] = "classification"
        metrics["accuracy"] = float(accuracy_score(y_test_bin, pred_bin))
        metrics["f1"] = float(f1_score(y_test_bin, pred_bin, zero_division=0))
    else:
        metrics["task"] = "regression"
        metrics["mae"] = float(mean_absolute_error(y_test, pred))
        metrics["rmse"] = float(np.sqrt(mean_squared_error(y_test, pred)))
        metrics["r2"] = float(r2_score(y_test, pred))

    return metrics


# =========================
# Load YAML + project from URL
# =========================
ROOT = Path(__file__).parents[1]
YAML_PATH = ROOT / "data" / "projects.yaml"
projects = load_projects(YAML_PATH)

q = st.query_params.get("project")
selected = find_project(projects, q)

# =========================
# Top bar
# =========================
st.markdown(
    """
<div class="topbar">
  <div>
    <h1 style="margin:0;">Lab</h1>
    <div class="pill">🧪 Data Console • Project Demos • Auto Insights • Experiments</div>
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
# Project header (if present)
# =========================
if selected:
    pid = project_pid(selected)
    industry = selected.get("industry", "")
    ptype = selected.get("type", "")
    impact = selected.get("impact_type", "")
    tools = selected.get("tools", []) if isinstance(selected.get("tools"), list) else []
    skills = selected.get("skills", []) if isinstance(selected.get("skills"), list) else []
    links = selected.get("links", {}) or {}

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"### {selected.get('title','Project')}")
    st.caption(selected.get("tagline", ""))

    st.markdown(
        "<div class='pills'>"
        + (f"<span class='pill2'>Industry: {industry}</span>" if industry else "")
        + (f"<span class='pill2'>Type: {ptype}</span>" if ptype else "")
        + (f"<span class='pill2'>Impact: {impact}</span>" if impact else "")
        + (f"<span class='pill2'>Tools: {', '.join(tools[:6])}</span>" if tools else "")
        + (f"<span class='pill2'>Skills: {', '.join(skills[:4])}</span>" if skills else "")
        + "</div>",
        unsafe_allow_html=True,
    )

    btns = []
    if links.get("github"):
        btns.append(("GitHub", links["github"]))
    if links.get("colab"):
        btns.append(("Colab", links["colab"]))
    if links.get("demo"):
        btns.append(("Demo", links["demo"]))
    if links.get("report"):
        btns.append(("Report", links["report"]))

    if btns:
        html_btns = ["<div class='links'>"]
        for label, url in btns:
            html_btns.append(f"<a href='{url}' target='_blank'>{label} ↗</a>")
        html_btns.append("</div>")
        st.markdown("".join(html_btns), unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    _log_append(f"<span class='badge-ok'>[project]</span> loaded: {selected.get('title','')}")
else:
    if q:
        _log_append(f"<span class='badge-warn'>[warn]</span> project not found for query: {q}")
    st.caption("Tip: open Lab from a project card → **Open in Lab**.")


# =========================
# Sidebar: data source
# =========================
with st.sidebar:
    st.markdown("### System")
    st.caption("Load a dataset, explore, then run auto insights & experiments.")

    options = ["Project demo (if available)", "Demo dataset (recommended)", "Upload CSV"]
    src = st.radio("Data source", options, index=0)

    uploaded = None
    if src == "Upload CSV":
        uploaded = st.file_uploader("Upload a CSV", type=["csv"], accept_multiple_files=False)

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    st.markdown("### Actions")
    run_insights = st.button("⚡ Run Auto Insights", use_container_width=True)
    clear_log = st.button("🧹 Clear output log", use_container_width=True)

    if clear_log:
        st.session_state["lab_log"] = []
        _log_append("[system] log cleared.")


# =========================
# Load data (Project demo -> taxi_demo.csv)
# =========================
df = None

if src == "Project demo (if available)" and selected:
    lab = selected.get("lab", {}) or {}
    demo_asset = lab.get("demo_asset")
    if demo_asset:
        path = (ROOT / demo_asset).resolve()
        if path.exists():
            try:
                df = pd.read_csv(path)
                _log_append(f"<span class='badge-ok'>[data]</span> loaded project demo: {demo_asset} ({len(df):,} rows)")
            except Exception as e:
                _log_append(f"<span class='badge-err'>[error]</span> failed to read demo_asset: {e}")
                df = None
        else:
            _log_append(f"<span class='badge-warn'>[warn]</span> demo_asset not found: {demo_asset}")
            df = None
    else:
        _log_append("<span class='badge-warn'>[warn]</span> project has no lab.demo_asset")
        df = None

if df is None:
    if src == "Upload CSV":
        if uploaded is None:
            st.info("Upload a CSV to begin — or switch to Demo dataset.")
            st.stop()
        try:
            df = pd.read_csv(uploaded)
            _log_append(f"<span class='badge-ok'>[data]</span> loaded CSV: {uploaded.name} ({len(df):,} rows).")
        except Exception as e:
            _log_append(f"<span class='badge-err'>[error]</span> failed to read CSV: {e}")
            st.error("Could not read that CSV.")
            st.stop()
    else:
        df = _demo_dataset()
        _log_append("[data] demo dataset loaded.")


# =========================
# Status KPIs
# =========================
n_rows, n_cols = df.shape
n_missing = int(df.isna().sum().sum())
n_num = len(_numeric_cols(df))
n_cat = len(_cat_cols(df))

st.markdown(
    f"""
<div class="kpi">
  <div class="k"><b>{n_rows:,}</b><span>rows</span></div>
  <div class="k"><b>{n_cols}</b><span>columns</span></div>
  <div class="k"><b>{n_num}</b><span>numeric</span></div>
  <div class="k"><b>{n_missing:,}</b><span>missing cells</span></div>
</div>
<div class="hr"></div>
""",
    unsafe_allow_html=True,
)

# =========================
# Data Explorer
# =========================
st.markdown("## Data Explorer")

colA, colB = st.columns([1.1, 1], gap="large")
with colA:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Preview")
    st.dataframe(df.head(30), use_container_width=True, height=360)
    st.markdown("</div>", unsafe_allow_html=True)

with colB:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Quick filters")
    cats = _cat_cols(df)
    nums = _numeric_cols(df)

    view = df.copy()
    if cats:
        c = st.selectbox("Filter by categorical column", ["(none)"] + cats, index=0)
        if c != "(none)":
            vals = sorted([v for v in view[c].dropna().unique()])[:150]
            pick = st.multiselect("Pick values", vals, default=vals[: min(3, len(vals))])
            if pick:
                view = view[view[c].isin(pick)]
                _log_append(f"[filter] {c} in {pick[:3]}{'...' if len(pick)>3 else ''}")

    if nums:
        n = st.selectbox("Filter by numeric column", ["(none)"] + nums, index=0)
        if n != "(none)":
            lo, hi = float(view[n].min()), float(view[n].max())
            rng = st.slider("Range", min_value=lo, max_value=hi, value=(lo, hi))
            view = view[(view[n] >= rng[0]) & (view[n] <= rng[1])]
            _log_append(f"[filter] {n} in [{rng[0]:.2f}, {rng[1]:.2f}]")

    st.markdown(f"<small>Filtered rows: <b>{len(view):,}</b></small>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# =========================
# Auto Insights
# =========================
st.markdown("## ⚡ Auto Insights")

if run_insights:
    _log_append("<span class='badge-ok'>[run]</span> auto insights started...")
    insights, tables, figs = auto_insights(view)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Findings")
    for i in insights:
        st.markdown(i)
    st.markdown("</div>", unsafe_allow_html=True)

    for name, table in tables.items():
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"### {name.replace('_',' ').title()}")
        st.dataframe(table, use_container_width=True, height=280)
        st.markdown("</div>", unsafe_allow_html=True)

    for fig in figs:
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.pyplot(fig, clear_figure=True)
        st.markdown("</div>", unsafe_allow_html=True)

    _log_append("<span class='badge-ok'>[done]</span> auto insights complete.")
else:
    st.caption("Press **Run Auto Insights** to generate insights + charts automatically.")

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# =========================
# Experiments
# =========================
st.markdown("## 🧪 Experiments")

targets = ["(none)"] + list(df.columns)
default_target = "(none)"
for cand in ["profitable", "target", "demand", "demand_units"]:
    if cand in df.columns:
        default_target = cand
        break

tcol = st.selectbox("Select a target column (optional)", targets, index=targets.index(default_target))
run_model = st.button("Run quick model", type="primary")

if run_model:
    if tcol == "(none)":
        st.warning("Select a target column to run a quick model.")
        _log_append("<span class='badge-warn'>[warn]</span> model skipped — no target selected.")
    else:
        _log_append(f"<span class='badge-ok'>[run]</span> training quick model on target: {tcol}")
        try:
            metrics = build_quick_model(df, tcol)
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown(f"### Model result — {metrics['task'].title()}")
            if metrics["task"] == "classification":
                st.markdown(f"• Accuracy: **{metrics['accuracy']:.3f}**")
                st.markdown(f"• F1 score: **{metrics['f1']:.3f}**")
            else:
                st.markdown(f"• MAE: **{metrics['mae']:.3f}**")
                st.markdown(f"• RMSE: **{metrics['rmse']:.3f}**")
                st.markdown(f"• R²: **{metrics['r2']:.3f}**")
            st.markdown("</div>", unsafe_allow_html=True)
            _log_append("<span class='badge-ok'>[done]</span> model finished.")
        except Exception as e:
            st.error("Model run failed. Check your dataset types.")
            _log_append(f"<span class='badge-err'>[error]</span> model failed: {e}")

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# =========================
# Output log
# =========================
st.markdown("## Output Log")
_render_log()
