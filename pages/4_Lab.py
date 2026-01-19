from __future__ import annotations

import re
from io import BytesIO
from pathlib import Path
from typing import Dict, Optional, Tuple

import streamlit as st

# Safe imports (page won't crash without clear message)
try:
    import numpy as np
except Exception:
    np = None

try:
    import pandas as pd
except Exception:
    pd = None

try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None


st.set_page_config(page_title="Lab • Portfolio JRR", page_icon="🧪", layout="wide")

# ---- Minimal UI cleanup ----
st.markdown(
    """
<style>
header[data-testid="stHeader"] {display:none;}
footer {visibility:hidden;}
.block-container { padding-top: 1.4rem; padding-bottom: 3rem; max-width: 1180px; }
</style>
""",
    unsafe_allow_html=True,
)

# ---- Console UI theme ----
st.markdown(
    """
<style>
:root{
  --fg: rgba(255,255,255,.92);
  --fg2: rgba(255,255,255,.72);
  --line: rgba(255,255,255,.12);
  --card: rgba(255,255,255,.04);
  --glass: rgba(0,0,0,.35);
}
html, body, [data-testid="stAppViewContainer"]{
  background: radial-gradient(980px 560px at 50% 0%, rgba(255,255,255,.06), rgba(0,0,0,.985)) !important;
  color: var(--fg) !important;
}
h1,h2,h3{ letter-spacing: -0.03em; }
.hr{ height:1px; background: var(--line); margin: 14px 0 18px 0; }

.topbar{
  display:flex; align-items:flex-start; justify-content:space-between;
  gap: 12px; padding: 10px 0 2px 0;
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

.console{
  border: 1px solid rgba(255,255,255,.14);
  border-radius: 20px;
  background: linear-gradient(180deg, rgba(255,255,255,.05), rgba(0,0,0,.22));
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
.small{ color: rgba(255,255,255,.72); }

.kpi{
  display:grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
  margin-top: 12px;
}
.kpi .k{
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 12px 12px;
  background: rgba(255,255,255,.03);
}
.kpi .k b{ font-size: 16px; color: rgba(255,255,255,.92); }
.kpi .k span{ display:block; margin-top: 2px; font-size: 12px; color: rgba(255,255,255,.68); }
@media (max-width: 900px){
  .kpi{ grid-template-columns: 1fr 1fr; }
}

.log{
  border: 1px solid rgba(255,255,255,.10);
  border-radius: 16px;
  background: rgba(0,0,0,.35);
  padding: 12px 12px;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  font-size: 12px;
  color: rgba(255,255,255,.78);
}
.log .line{ margin: 2px 0; }
.log .ok{ color: rgba(170,255,210,.92); }
.log .warn{ color: rgba(255,230,170,.90); }
.log .err{ color: rgba(255,170,170,.90); }

.pills{ display:flex; gap:8px; flex-wrap:wrap; margin-top: 10px; }
.pill{
  padding: 6px 9px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: rgba(0,0,0,.22);
  color: rgba(255,255,255,.78);
  font-size: 12px;
}

</style>
""",
    unsafe_allow_html=True,
)

# ---- Guardrails ----
missing = []
if np is None:
    missing.append("numpy")
if pd is None:
    missing.append("pandas")
if plt is None:
    missing.append("matplotlib")

if missing:
    st.error(
        "Lab needs these packages installed to render results: "
        + ", ".join(missing)
        + ".\n\nAdd them to requirements.txt and redeploy."
    )
    st.stop()


# =========================
# Helpers: dataset + engine
# =========================
@st.cache_data(show_spinner=False)
def make_ops_dataset(n: int = 900, seed: int = 7) -> pd.DataFrame:
    """Synthetic but realistic 'ops/industrial' dataset with profit/risk/impact flavor."""
    rng = np.random.default_rng(seed)

    sites = np.array(["Altamira", "Tuxpan", "Veracruz", "Monterrey"])
    assets = np.array(["Pump", "Compressor", "Valve", "Sensor", "Line"])
    teams = np.array(["Ops", "Maintenance", "Reliability"])

    df = pd.DataFrame(
        {
            "site": rng.choice(sites, size=n, p=[0.30, 0.20, 0.25, 0.25]),
            "asset": rng.choice(assets, size=n, p=[0.22, 0.18, 0.20, 0.25, 0.15]),
            "team": rng.choice(teams, size=n, p=[0.45, 0.35, 0.20]),
        }
    )

    # time axis (monthly)
    months = pd.date_range("2024-01-01", periods=18, freq="MS")
    df["month"] = rng.choice(months, size=n)
    df["month"] = df["month"].dt.strftime("%Y-%m")

    # operational metrics
    df["pressure_bar"] = np.clip(rng.normal(78, 12, size=n), 35, 115)
    df["temp_c"] = np.clip(rng.normal(46, 8, size=n), 18, 78)
    df["flow_m3h"] = np.clip(rng.normal(120, 35, size=n), 30, 240)

    # events / reliability
    base_inc = rng.poisson(lam=0.8, size=n)
    stress = (df["pressure_bar"] > 92).astype(int) + (df["temp_c"] > 58).astype(int)
    df["incidents"] = np.clip(base_inc + stress + rng.binomial(1, 0.12, size=n), 0, 8)

    df["downtime_h"] = np.clip(
        rng.gamma(shape=1.6, scale=3.2, size=n) + df["incidents"] * rng.uniform(0.8, 3.2, size=n),
        0,
        72,
    )

    # costs and savings (simple business layer)
    df["maintenance_cost"] = np.round(
        np.clip(rng.lognormal(mean=8.2, sigma=0.35, size=n), 1500, 25000)
        + df["incidents"] * rng.uniform(150, 900, size=n),
        0,
    )

    df["revenue"] = np.round(
        np.clip(rng.lognormal(mean=9.2, sigma=0.22, size=n), 8000, 120000)
        - df["downtime_h"] * rng.uniform(50, 220, size=n),
        0,
    )

    df["profit"] = np.round(df["revenue"] - df["maintenance_cost"], 0)

    # risk score (0-100), intentionally explainable
    risk = (
        0.35 * (df["pressure_bar"] / 115) * 100
        + 0.22 * (df["temp_c"] / 78) * 100
        + 0.28 * (df["incidents"] / 8) * 100
        + 0.15 * (df["downtime_h"] / 72) * 100
    )
    df["risk_score"] = np.round(np.clip(risk, 0, 100), 1)

    # social impact proxy (0-100): safer ops + less downtime -> higher
    impact = 100 - (0.55 * df["risk_score"] + 0.45 * (df["downtime_h"] / 72) * 100)
    df["impact_score"] = np.round(np.clip(impact, 0, 100), 1)

    return df


def _infer_time_col(df: pd.DataFrame) -> Optional[str]:
    for c in df.columns:
        if "month" in c.lower() or "date" in c.lower() or "time" in c.lower():
            return c
    return None


def _numeric_cols(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]


def _cat_cols(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if df[c].dtype == "object"]


def _find_col_by_keyword(df: pd.DataFrame, keyword: str) -> Optional[str]:
    k = keyword.lower().strip()
    # direct match
    for c in df.columns:
        if c.lower() == k:
            return c
    # contains match
    for c in df.columns:
        if k in c.lower():
            return c
    return None


def detect_intent(q: str) -> str:
    s = q.lower().strip()

    if any(w in s for w in ["correlation", "correlate", "corr", "relationship"]):
        return "correlation"
    if any(w in s for w in ["trend", "over time", "time series", "month", "evolution"]):
        return "trend"
    if any(w in s for w in ["compare", "vs", "by", "group", "segment", "site", "team", "asset"]):
        return "group_compare"
    if any(w in s for w in ["outlier", "anomaly", "weird", "extreme"]):
        return "outliers"
    if any(w in s for w in ["top", "highest", "best", "max"]):
        return "top"
    if any(w in s for w in ["bottom", "lowest", "worst", "min"]):
        return "bottom"
    if any(w in s for w in ["distribution", "hist", "histogram", "spread"]):
        return "distribution"
    if any(w in s for w in ["summary", "describe", "overview", "what columns", "schema"]):
        return "summary"
    return "auto"


def extract_metric(df: pd.DataFrame, q: str) -> str:
    """Pick a metric column based on question keywords; fallback to 'profit' or first numeric."""
    s = q.lower()
    preferred = ["profit", "risk_score", "impact_score", "revenue", "maintenance_cost", "downtime_h", "incidents"]
    for p in preferred:
        if p.replace("_", " ") in s or p in s:
            if p in df.columns:
                return p
    nums = _numeric_cols(df)
    return "profit" if "profit" in df.columns else (nums[0] if nums else df.columns[0])


def extract_group(df: pd.DataFrame, q: str) -> Optional[str]:
    s = q.lower()
    for g in ["site", "asset", "team", "segment", "category"]:
        if g in df.columns and g in s:
            return g
    # heuristic: if user writes "by X"
    m = re.search(r"\bby\s+([a-zA-Z_]+)", s)
    if m:
        candidate = _find_col_by_keyword(df, m.group(1))
        if candidate and candidate in _cat_cols(df):
            return candidate
    # fallback: choose a common categorical if present
    for g in ["site", "asset", "team"]:
        if g in df.columns:
            return g
    cats = _cat_cols(df)
    return cats[0] if cats else None


def run_query(df: pd.DataFrame, q: str) -> Tuple[str, Optional[pd.DataFrame], Optional[plt.Figure], Dict[str, str]]:
    """
    Returns: (answer_text, result_table, figure, debug)
    """
    debug = {}
    intent = detect_intent(q)
    debug["intent"] = intent

    metric = extract_metric(df, q)
    debug["metric"] = metric

    group = extract_group(df, q)
    debug["group"] = group or "(none)"

    time_col = _infer_time_col(df)
    debug["time_col"] = time_col or "(none)"

    nums = _numeric_cols(df)
    cats = _cat_cols(df)

    # AUTO intent: pick a useful default based on keywords
    if intent == "auto":
        if any(w in q.lower() for w in ["risk", "safe", "incident", "downtime"]):
            intent = "group_compare"
        else:
            intent = "summary"
        debug["intent"] = f"auto → {intent}"

    fig = None
    table = None

    # ---------- SUMMARY ----------
    if intent == "summary":
        answer = (
            f"Loaded **{len(df):,} rows** and **{df.shape[1]} columns**.\n\n"
            f"• Categorical: {', '.join(cats[:8]) if cats else '(none)'}\n"
            f"• Numeric: {', '.join(nums[:10]) if nums else '(none)'}\n\n"
            "If you ask something like **'compare profit by site'** or **'correlation with risk'**, "
            "I'll compute it and show the result."
        )
        # small schema table
        table = pd.DataFrame({"column": df.columns, "dtype": [str(df[c].dtype) for c in df.columns]})
        return answer, table, None, debug

    # ---------- DISTRIBUTION ----------
    if intent == "distribution":
        if metric not in df.columns or not pd.api.types.is_numeric_dtype(df[metric]):
            metric = nums[0] if nums else df.columns[0]
            debug["metric"] = metric

        x = df[metric].dropna().values
        p05, p50, p95 = np.quantile(x, [0.05, 0.50, 0.95])

        answer = (
            f"Distribution of **{metric}**:\n\n"
            f"• Mean: **{np.mean(x):,.2f}**\n"
            f"• P05 / Median / P95: **{p05:,.2f} / {p50:,.2f} / {p95:,.2f}**\n"
            f"• Std: **{np.std(x):,.2f}**"
        )

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.hist(x, bins=60)
        ax.set_title(f"Distribution: {metric}")
        ax.set_xlabel(metric)
        ax.set_ylabel("Frequency")

        return answer, None, fig, debug

    # ---------- GROUP COMPARE ----------
    if intent == "group_compare":
        if not group:
            return "I couldn't find a categorical column to group by. Try: `by site` or `by asset`.", None, None, debug

        if metric not in df.columns or not pd.api.types.is_numeric_dtype(df[metric]):
            metric = nums[0] if nums else df.columns[0]
            debug["metric"] = metric

        g = (
            df.groupby(group, dropna=False)[metric]
            .agg(["mean", "median", "count"])
            .sort_values("mean", ascending=False)
            .reset_index()
        )
        table = g

        top_row = g.iloc[0]
        bottom_row = g.iloc[-1]
        answer = (
            f"Comparison of **{metric} by {group}**:\n\n"
            f"• Best: **{top_row[group]}** (mean **{top_row['mean']:,.2f}**, n={int(top_row['count'])})\n"
            f"• Lowest: **{bottom_row[group]}** (mean **{bottom_row['mean']:,.2f}**, n={int(bottom_row['count'])})\n"
            "Showing mean/median/count."
        )

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.bar(g[group].astype(str).values[:12], g["mean"].values[:12])
        ax.set_title(f"Mean {metric} by {group} (top)")
        ax.set_xlabel(group)
        ax.set_ylabel(f"Mean {metric}")
        ax.tick_params(axis="x", rotation=25)

        return answer, table, fig, debug

    # ---------- TREND ----------
    if intent == "trend":
        if not time_col:
            return "I couldn't infer a time column. Try adding a `month` or `date` column.", None, None, debug

        if metric not in df.columns or not pd.api.types.is_numeric_dtype(df[metric]):
            metric = nums[0] if nums else df.columns[0]
            debug["metric"] = metric

        s = df.groupby(time_col)[metric].mean().reset_index()
        table = s

        answer = (
            f"Trend of **{metric} over {time_col}** (mean by period).\n"
            "If you want a specific grouping, ask: *'trend of profit by site'* (we can add that next)."
        )

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(s[time_col].astype(str).values, s[metric].values, marker="o")
        ax.set_title(f"{metric} trend over {time_col}")
        ax.tick_params(axis="x", rotation=28)
        ax.set_xlabel(time_col)
        ax.set_ylabel(metric)

        return answer, table, fig, debug

    # ---------- CORRELATION ----------
    if intent == "correlation":
        if len(nums) < 2:
            return "Not enough numeric columns to compute correlations.", None, None, debug

        corr = df[nums].corr(numeric_only=True)
        # correlations with metric
        if metric in corr.columns:
            rel = corr[metric].drop(index=metric).sort_values(ascending=False).reset_index()
            rel.columns = ["feature", "corr_with_" + metric]
            table = rel

            top = rel.iloc[0]
            low = rel.iloc[-1]
            answer = (
                f"Correlation analysis (numeric) — **what relates to {metric}**:\n\n"
                f"• Strongest positive: **{top['feature']}** (ρ={top.iloc[1]:.2f})\n"
                f"• Most negative: **{low['feature']}** (ρ={low.iloc[1]:.2f})\n"
                "Correlation is not causality, but it’s a fast signal for what to inspect."
            )

            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.bar(rel["feature"].values[:10].astype(str), rel.iloc[:10, 1].values)
            ax.set_title(f"Top correlations with {metric}")
            ax.set_xlabel("Feature")
            ax.set_ylabel("Correlation (ρ)")
            ax.tick_params(axis="x", rotation=25)

            return answer, table, fig, debug

        return "Metric not found for correlation. Try: `correlation with risk_score`.", None, None, debug

    # ---------- OUTLIERS ----------
    if intent == "outliers":
        if metric not in df.columns or not pd.api.types.is_numeric_dtype(df[metric]):
            metric = nums[0] if nums else df.columns[0]
            debug["metric"] = metric

        x = df[metric].dropna()
        q1, q3 = x.quantile(0.25), x.quantile(0.75)
        iqr = q3 - q1
        lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr

        out = df[(df[metric] < lo) | (df[metric] > hi)].copy()
        out = out.sort_values(metric, ascending=False).head(20)
        table = out

        answer = (
            f"Outliers for **{metric}** using IQR rule:\n\n"
            f"• Bounds: [{lo:,.2f}, {hi:,.2f}]\n"
            f"• Found: **{len(out):,}** sample rows (showing top 20 by {metric})."
        )

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.hist(df[metric].dropna().values, bins=60)
        ax.set_title(f"Outliers context: {metric}")
        ax.set_xlabel(metric)
        ax.set_ylabel("Frequency")

        return answer, table, fig, debug

    # ---------- TOP/BOTTOM ----------
    if intent in ["top", "bottom"]:
        if metric not in df.columns or not pd.api.types.is_numeric_dtype(df[metric]):
            metric = nums[0] if nums else df.columns[0]
            debug["metric"] = metric

        n = 12
        ascending = intent == "bottom"
        sample_cols = [c for c in ["site", "asset", "team", "month", metric, "risk_score", "impact_score"] if c in df.columns]
        out = df[sample_cols].sort_values(metric, ascending=ascending).head(n).copy()
        table = out
        answer = f"Showing **{n} {'lowest' if ascending else 'highest'}** rows by **{metric}**."

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(out[metric].values[::-1] if ascending else out[metric].values, marker="o")
        ax.set_title(f"{'Lowest' if ascending else 'Highest'} {metric} (sample)")
        ax.set_xlabel("Rank")
        ax.set_ylabel(metric)

        return answer, table, fig, debug

    return "I couldn't interpret that yet. Try: `compare profit by site` or `correlation with risk_score`.", None, None, debug


def df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


# ============
# UI: Console
# ============
st.markdown(
    """
<div class="topbar">
  <div>
    <h1 style="margin:0;">Lab Console</h1>
    <div class="small">Load data → ask a question → get a structured answer (text + table + chart).</div>
    <div class="pills">
      <span class="pill">🧪 Experimental console</span>
      <span class="pill">🧠 Interpretable reasoning</span>
      <span class="pill">📈 Visible results</span>
    </div>
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

left, right = st.columns([1.0, 1.25], gap="large")

with left:
    st.markdown('<div class="console">', unsafe_allow_html=True)
    st.markdown('<div class="badge">DATA INPUT</div>', unsafe_allow_html=True)

    mode = st.radio("Dataset", ["OpsLab (built-in)", "Upload CSV"], horizontal=True)
    df = None

    if mode == "OpsLab (built-in)":
        n = st.slider("Rows", 300, 3000, 900, 100)
        seed = st.number_input("Seed", value=7, min_value=0, step=1)
        df = make_ops_dataset(int(n), int(seed))
        st.caption("Built-in dataset designed to look real: ops metrics, risk, downtime, profit, impact.")

    else:
        up = st.file_uploader("Upload a CSV", type=["csv"])
        if up is not None:
            try:
                df = pd.read_csv(up)
            except Exception as e:
                st.error(f"Could not read CSV: {e}")
                df = None

    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
    st.markdown('<div class="badge">ASK THE LAB</div>', unsafe_allow_html=True)

    examples = [
        "compare profit by site",
        "correlation with risk_score",
        "trend of downtime_h over time",
        "distribution of maintenance_cost",
        "outliers in incidents",
        "top highest risk_score",
        "summary / schema",
    ]

    ex_cols = st.columns(2)
    if ex_cols[0].button("▶ compare profit by site", use_container_width=True):
        st.session_state["lab_q"] = "compare profit by site"
    if ex_cols[1].button("▶ correlation with risk_score", use_container_width=True):
        st.session_state["lab_q"] = "correlation with risk_score"
    if ex_cols[0].button("▶ trend of profit over time", use_container_width=True):
        st.session_state["lab_q"] = "trend of profit over time"
    if ex_cols[1].button("▶ outliers in downtime_h", use_container_width=True):
        st.session_state["lab_q"] = "outliers in downtime_h"
    if ex_cols[0].button("▶ distribution of profit", use_container_width=True):
        st.session_state["lab_q"] = "distribution of profit"
    if ex_cols[1].button("▶ summary / schema", use_container_width=True):
        st.session_state["lab_q"] = "summary / schema"

    q = st.text_input("Ask a question", key="lab_q", placeholder="e.g., compare profit by asset")
    run = st.button("Run analysis", type="primary", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="console">', unsafe_allow_html=True)
    st.markdown('<div class="badge">OUTPUT</div>', unsafe_allow_html=True)

    if df is None:
        st.info("Load a dataset on the left to activate the console.")
        st.markdown("</div>", unsafe_allow_html=True)
        st.stop()

    # KPI strip
    nums = _numeric_cols(df)
    cats = _cat_cols(df)

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Rows", f"{len(df):,}")
    k2.metric("Columns", f"{df.shape[1]}")
    k3.metric("Numeric", f"{len(nums)}")
    k4.metric("Categorical", f"{len(cats)}")

    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

    # Always show preview collapsed
    with st.expander("Dataset preview", expanded=False):
        st.dataframe(df.head(40), use_container_width=True)

    if run and q.strip():
        answer, table, fig, debug = run_query(df, q)

        # Console logs
        st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
        st.markdown('<div class="badge">CONSOLE LOG</div>', unsafe_allow_html=True)

        log_lines = [
            ("ok", f"Intent: {debug.get('intent','(none)')}"),
            ("ok", f"Metric: {debug.get('metric','(none)')}"),
            ("ok", f"Group: {debug.get('group','(none)')}"),
            ("ok", f"Time col: {debug.get('time_col','(none)')}"),
        ]

        st.markdown('<div class="log">', unsafe_allow_html=True)
        for level, line in log_lines:
            st.markdown(f'<div class="line {level}">• {line}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Answer
        st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
        st.markdown("### Answer")
        st.markdown(answer)

        # Table
        if table is not None:
            st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
            st.markdown("### Table")
            st.dataframe(table, use_container_width=True, height=360)

            # Download table
            st.download_button(
                "Download table as CSV",
                data=df_to_csv_bytes(table),
                file_name="lab_result.csv",
                mime="text/csv",
                use_container_width=True,
            )

        # Chart
        if fig is not None:
            st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
            st.markdown("### Chart")
            st.pyplot(fig, clear_figure=True)

        # Logic
        with st.expander("Logic used (how the console interpreted your question)", expanded=False):
            st.write(
                {
                    "Detected intent": debug.get("intent"),
                    "Chosen metric": debug.get("metric"),
                    "Chosen group": debug.get("group"),
                    "Detected time column": debug.get("time_col"),
                    "Tip": "Try phrasing like: 'compare X by Y', 'distribution of X', 'correlation with X', 'trend of X over time'.",
                }
            )

    else:
        st.caption("Ask something on the left, then click **Run analysis**. You’ll get text + table + chart here.")

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
st.caption("This Lab is intentionally designed as a visible system: data → reasoning → output.")
