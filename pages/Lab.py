from __future__ import annotations

from pathlib import Path
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

.pill{
  display:inline-flex; align-items:center; gap:8px;
  padding: 7px 10px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: rgba(255,255,255,.03);
  color: rgba(255,255,255,.84);
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

/* ✅ make Streamlit buttons readable */
div.stButton > button{
  width: auto;
  border-radius: 999px !important;
  border: 1px solid rgba(255,255,255,.18) !important;
  background: rgba(255,255,255,.06) !important;
  color: rgba(255,255,255,.92) !important;
  padding: 0.55rem 0.95rem !important;
}
div.stButton > button:hover{
  background: rgba(255,255,255,.10) !important;
  border-color: rgba(255,255,255,.28) !important;
}
</style>
""",
    unsafe_allow_html=True,
)


# =========================
# Helpers
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
        }
    )
    miss_idx = rng.choice(np.arange(n), size=int(n * 0.03), replace=False)
    df.loc[miss_idx, "lead_time_days"] = np.nan
    return df


def _log_append(msg: str):
    st.session_state.setdefault("lab_log", [])
    st.session_state["lab_log"].append(msg)
    st.session_state["lab_log"] = st.session_state["lab_log"][-160:]


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


def auto_insights(df: pd.DataFrame):
    insights, tables, figs = [], {}, []

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

    # choose a preferred measure
    preferred = None
    for c in ["demand", "demand_units", "profit"]:
        if c in df.columns:
            preferred = c
            break
    if preferred is None and nums:
        preferred = nums[0]

    # correlations
    if preferred and preferred in df.columns and len(nums) >= 2:
        corr = (
            df[nums]
            .corr(numeric_only=True)[preferred]
            .drop(index=preferred, errors="ignore")
            .sort_values(ascending=False)
        )
        if len(corr) > 0:
            top = corr.iloc[0]
            low = corr.iloc[-1]
            insights.append(f"• Strongest positive driver of {preferred}: {top.name} (ρ={top:.2f})")
            insights.append(f"• Strongest negative driver of {preferred}: {low.name} (ρ={low:.2f})")
            tables[f"correlation_with_{preferred}"] = corr.reset_index().rename(columns={"index": "feature", preferred: "correlation"})

            fig = plt.figure()
            ax = fig.add_subplot(111)
            topn = corr.head(8)
            ax.bar(topn.index, topn.values)
            ax.set_title(f"Top correlations with {preferred}")
            ax.tick_params(axis="x", rotation=25)
            figs.append(fig)

    # group means
    if preferred and preferred in df.columns and cats:
        gcol = cats[0]
        g = df.groupby(gcol)[preferred].mean().sort_values(ascending=False)
        tables[f"mean_{preferred}_by_{gcol}"] = g.reset_index().rename(columns={preferred: f"mean_{preferred}"})

    # trend
    if preferred and preferred in df.columns and time_col:
        try:
            tmp = df.copy()
            tmp[time_col] = pd.to_datetime(tmp[time_col], errors="coerce")
            tmp = tmp.dropna(subset=[time_col])
            if not tmp.empty:
                t = tmp.groupby(tmp[time_col].dt.to_period("M"))[preferred].mean()

                fig = plt.figure()
                ax = fig.add_subplot(111)
                ax.plot(t.index.astype(str), t.values, marker="o")
                ax.set_title(f"{preferred} trend (monthly)")
                ax.tick_params(axis="x", rotation=25)
                figs.append(fig)

                if len(t) >= 2:
                    delta = float(t.iloc[-1] - t.iloc[0])
                    insights.append(f"• {preferred} trend: {'upward' if delta>0 else 'downward'} ({delta:,.1f})")
        except Exception:
            pass

    return insights, tables, figs


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
# Load YAML + query param
# =========================
projects = load_projects(YAML_PATH)
project_q = st.query_params.get("project")

selected = None
if project_q:
    for p in projects:
        if str(p.get("id", "")).strip() == str(project_q).strip():
            selected = p
            break


def demo_asset_path(p: dict | None) -> Path | None:
    if not p:
        return None
    demo = (p.get("lab", {}) or {}).get("demo_asset")
    if not demo:
        return None
    path = ROOT / demo
    return path if path.exists() else None


def has_demo(p: dict | None) -> bool:
    return demo_asset_path(p) is not None


# =========================
# Data mode state
# =========================
st.session_state.setdefault("data_mode", "demo")  # demo | project_demo | upload
st.session_state.setdefault("auto_loaded_demo", False)

if selected and has_demo(selected) and not st.session_state["auto_loaded_demo"]:
    st.session_state["data_mode"] = "project_demo"
    st.session_state["auto_loaded_demo"] = True
    _log_append("<span class='badge-ok'>[auto]</span> auto-loaded Project demo on entry.")


# =========================
# Top bar (NAV)
# =========================
st.markdown(
    """
<div class="topbar">
  <div>
    <h1 style="margin:0;">Lab</h1>
    <div class="pill">🧪 Data Console • Auto Insights • Experiments</div>
  </div>
  <div class="navbtns">
    <a href="/" target="_self">← Home</a>
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
# Project header card
# =========================
if selected:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"### {selected.get('title','Project')}")
    st.caption(selected.get("tagline", ""))

    pills = []
    for k in ["industry", "type", "impact_type", "status", "year"]:
        if selected.get(k):
            pills.append(f"<span class='pill2'>{k.replace('_',' ').title()}: {selected[k]}</span>")

    tools = selected.get("tools", []) if isinstance(selected.get("tools"), list) else []
    skills = selected.get("skills", []) if isinstance(selected.get("skills"), list) else []
    if tools:
        pills.append(f"<span class='pill2'>Tools: {', '.join(tools[:6])}</span>")
    if skills:
        pills.append(f"<span class='pill2'>Skills: {', '.join(skills[:4])}</span>")

    st.markdown("<div class='pills'>" + "".join(pills) + "</div>", unsafe_allow_html=True)

    # Data source pill
    mode = st.session_state["data_mode"]
    source_label = {"project_demo": "Project demo", "demo": "Demo dataset", "upload": "Uploaded CSV"}.get(mode, mode)
    st.markdown(f"<div style='margin-top:10px;'><span class='pill'>Data source: {source_label}</span></div>", unsafe_allow_html=True)

    # Toggle button
    if has_demo(selected):
        st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
        st.markdown("<span class='pill'>🧪 Project demo available</span>", unsafe_allow_html=True)

        btn_label = "Switch to Demo dataset" if st.session_state["data_mode"] == "project_demo" else "Load Project Demo"
        if st.button(btn_label, key="toggle_project_demo"):
            if st.session_state["data_mode"] == "project_demo":
                st.session_state["data_mode"] = "demo"
                _log_append("<span class='badge-ok'>[ui]</span> switched to Demo dataset.")
            else:
                st.session_state["data_mode"] = "project_demo"
                _log_append("<span class='badge-ok'>[ui]</span> switched to Project demo.")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    _log_append(f"<span class='badge-ok'>[project]</span> loaded: {selected.get('id','')}")
else:
    st.caption("Tip: Open from Projects → Open in Lab.")


# =========================
# Sidebar: controls
# =========================
with st.sidebar:
    st.markdown("### Data source")
    opts = ["Demo dataset (recommended)", "Upload CSV"]
    if has_demo(selected):
        opts = ["Project demo"] + opts

    label_to_mode = {"Project demo": "project_demo", "Demo dataset (recommended)": "demo", "Upload CSV": "upload"}
    mode_to_label = {v: k for k, v in label_to_mode.items()}

    current_label = mode_to_label.get(st.session_state["data_mode"], opts[0])
    if current_label not in opts:
        current_label = opts[0]

    pick = st.radio("Select", opts, index=opts.index(current_label))
    st.session_state["data_mode"] = label_to_mode[pick]

    uploaded = None
    if st.session_state["data_mode"] == "upload":
        uploaded = st.file_uploader("Upload CSV", type=["csv"], accept_multiple_files=False)

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
    st.markdown("### Actions")
    run_insights = st.button("⚡ Run Auto Insights", use_container_width=True)
    clear_log = st.button("🧹 Clear output log", use_container_width=True)

    if clear_log:
        st.session_state["lab_log"] = []
        _log_append("[system] log cleared.")
        st.rerun()


# =========================
# Load data
# =========================
df = None
mode = st.session_state["data_mode"]

if mode == "project_demo" and selected and has_demo(selected):
    path = demo_asset_path(selected)
    df = pd.read_csv(path)
    _log_append(f"<span class='badge-ok'>[data]</span> loaded project demo: {path.relative_to(ROOT)}")

elif mode == "upload":
    if uploaded is None:
        st.info("Upload a CSV to begin — or switch back to Demo dataset.")
        st.stop()
    df = pd.read_csv(uploaded)
    _log_append(f"<span class='badge-ok'>[data]</span> loaded CSV: {uploaded.name} ({len(df):,} rows).")

else:
    df = _demo_dataset()
    _log_append("[data] demo dataset loaded.")


# =========================
# KPIs
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
# Data explorer (with filters)
# =========================
st.markdown("## Data Explorer")

colA, colB = st.columns([1.15, 1], gap="large")
with colA:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Preview")
    st.dataframe(df.head(40), use_container_width=True, height=380)
    st.markdown("</div>", unsafe_allow_html=True)

with colB:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Quick filters")

    view = df.copy()
    cats = _cat_cols(view)
    nums = _numeric_cols(view)

    if cats:
        c = st.selectbox("Filter by categorical column", ["(none)"] + cats, index=0)
        if c != "(none)":
            vals = sorted([v for v in view[c].dropna().unique()])[:200]
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
    st.caption("Press **Run Auto Insights** (sidebar) to generate insights + tables + charts automatically.")

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)


# =========================
# Experiments
# =========================
st.markdown("## 🧪 Experiments")

targets = ["(none)"] + list(df.columns)
default_target = "(none)"
for cand in ["demand", "demand_units", "target", "profit"]:
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
