from __future__ import annotations

from io import BytesIO
from pathlib import Path

import streamlit as st

# --- Safe imports (so the page doesn't die if env is missing something) ---
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

# --- Minimal UI cleanup ---
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

# --- Theme (matches About/Projects) ---
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
.kpi{
  display:grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}
.kpi .k{
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 14px 14px;
  background: rgba(255,255,255,.03);
}
.kpi .k b{ font-size: 18px; color: rgba(255,255,255,.92); }
.kpi .k span{ display:block; margin-top: 2px; font-size: 12px; color: rgba(255,255,255,.68); }
@media (max-width: 900px){
  .kpi{ grid-template-columns: 1fr; }
}
</style>
""",
    unsafe_allow_html=True,
)

# --- Top bar ---
st.markdown(
    """
<div class="topbar">
  <div>
    <h1 style="margin:0;">Lab</h1>
    <div class="small">A visible sandbox: simulate, explore, and test systems — live.</div>
    <div class="pills">
      <span class="pill">🧠 Data → Decisions</span>
      <span class="pill">🎛️ Interactive</span>
      <span class="pill">🧪 Experiments</span>
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

# --- Environment guardrails ---
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

# --- KPI quick scan (recruiter-friendly) ---
st.markdown(
    """
<div class="kpi">
  <div class="k"><b>Monte Carlo</b><span>Simulations with distributions + quantiles</span></div>
  <div class="k"><b>Data Explorer</b><span>Upload CSV → filter → summarize → chart</span></div>
  <div class="k"><b>Scoring</b><span>Interpretable “ML-style” risk/score demo</span></div>
</div>
<div class="hr"></div>
""",
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs(["🎲 Monte Carlo", "🧾 Data Explorer", "🧠 Scoring Demo"])


# -----------------------------
# Tab 1: Monte Carlo Simulator
# -----------------------------
with tab1:
    st.markdown(
        """
<div class="card">
  <div class="badge">🎲 Monte Carlo Simulator</div>
  <h3 style="margin:10px 0 0 0;">Simulate outcomes and visualize uncertainty</h3>
  <p class="small" style="margin-top:8px;">
    This is the same philosophy behind forecasting, operations planning, and decision systems:
    don’t guess a single number — model distributions.
  </p>
</div>
""",
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns([1, 1, 1, 1], gap="large")

    n = c1.slider("Iterations", min_value=1_000, max_value=50_000, value=10_000, step=1_000)
    mu = c2.number_input("Mean (μ)", value=0.0, step=0.1)
    sigma = c3.number_input("Std Dev (σ)", value=1.0, min_value=0.0001, step=0.1)
    seed = c4.number_input("Seed", value=42, min_value=0, step=1)

    dist = st.selectbox("Distribution", ["Normal", "Lognormal", "Uniform"], index=0)

    @st.cache_data(show_spinner=False)
    def simulate(dist_name: str, n: int, mu: float, sigma: float, seed: int):
        rng = np.random.default_rng(seed)
        if dist_name == "Normal":
            x = rng.normal(loc=mu, scale=sigma, size=n)
        elif dist_name == "Lognormal":
            # mu/sigma interpreted as underlying normal params
            x = rng.lognormal(mean=mu, sigma=max(sigma, 1e-6), size=n)
        else:
            # Uniform using mu as center and sigma as half-width-ish
            low = mu - sigma
            high = mu + sigma
            x = rng.uniform(low=low, high=high, size=n)
        return x

    x = simulate(dist, int(n), float(mu), float(sigma), int(seed))

    q05, q50, q95 = np.quantile(x, [0.05, 0.50, 0.95])
    mean = float(np.mean(x))
    std = float(np.std(x))

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Mean", f"{mean:,.3f}")
    k2.metric("Std", f"{std:,.3f}")
    k3.metric("P05", f"{q05:,.3f}")
    k4.metric("P95", f"{q95:,.3f}")

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    # Chart
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.hist(x, bins=60)
    ax.set_title("Simulated outcome distribution")
    ax.set_xlabel("Outcome")
    ax.set_ylabel("Frequency")
    st.pyplot(fig, clear_figure=True)

    st.caption("Tip: This demo is deliberately simple — the real value is turning it into a domain model (ops, finance, sports, safety, etc.).")


# -----------------------------
# Tab 2: Data Explorer
# -----------------------------
with tab2:
    st.markdown(
        """
<div class="card">
  <div class="badge">🧾 Data Explorer</div>
  <h3 style="margin:10px 0 0 0;">Upload a dataset and make it readable in seconds</h3>
  <p class="small" style="margin-top:8px;">
    Recruiters love this because it shows end-to-end thinking:
    input → cleanup → insight → visualization.
  </p>
</div>
""",
        unsafe_allow_html=True,
    )

    uploaded = st.file_uploader("Upload a CSV", type=["csv"])
    example = st.toggle("Use example dataset", value=True)

    @st.cache_data(show_spinner=False)
    def example_df():
        rng = np.random.default_rng(7)
        n = 400
        df = pd.DataFrame(
            {
                "segment": rng.choice(["A", "B", "C"], size=n, p=[0.35, 0.45, 0.20]),
                "revenue": np.round(rng.lognormal(mean=3.4, sigma=0.45, size=n), 2),
                "cost": np.round(rng.lognormal(mean=3.0, sigma=0.50, size=n), 2),
            }
        )
        df["profit"] = np.round(df["revenue"] - df["cost"], 2)
        df["month"] = rng.choice(pd.date_range("2025-01-01", periods=12, freq="MS").strftime("%Y-%m"), size=n)
        return df

    df = None
    if uploaded is not None:
        try:
            df = pd.read_csv(uploaded)
        except Exception as e:
            st.error(f"Could not read CSV: {e}")
            df = None
    elif example:
        df = example_df()

    if df is None:
        st.info("Upload a CSV to start, or enable the example dataset.")
    else:
        st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

        st.write("Preview")
        st.dataframe(df, use_container_width=True, height=320)

        st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1.1, 1, 1], gap="large")
        numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
        cat_cols = [c for c in df.columns if df[c].dtype == "object"]

        group_col = c1.selectbox("Group by (optional)", ["(none)"] + cat_cols, index=0)
        metric_col = c2.selectbox("Metric", numeric_cols if numeric_cols else ["(none)"], index=0)
        chart = c3.selectbox("Chart", ["Histogram", "Bar (mean by group)", "Line (by time-like column)"], index=0)

        if metric_col == "(none)":
            st.warning("No numeric columns detected.")
        else:
            if chart == "Histogram":
                fig = plt.figure()
                ax = fig.add_subplot(111)
                ax.hist(df[metric_col].dropna().values, bins=50)
                ax.set_title(f"Histogram: {metric_col}")
                st.pyplot(fig, clear_figure=True)

            elif chart == "Bar (mean by group)":
                if group_col == "(none)":
                    st.warning("Pick a group column for bar chart.")
                else:
                    g = df.groupby(group_col, dropna=False)[metric_col].mean().sort_values(ascending=False)
                    fig = plt.figure()
                    ax = fig.add_subplot(111)
                    ax.bar(g.index.astype(str), g.values)
                    ax.set_title(f"Mean {metric_col} by {group_col}")
                    ax.set_xlabel(group_col)
                    ax.set_ylabel(f"Mean {metric_col}")
                    st.pyplot(fig, clear_figure=True)

            else:  # line
                # heuristic: pick a time-like column
                candidates = [c for c in df.columns if "date" in c.lower() or "month" in c.lower() or "time" in c.lower()]
                time_col = st.selectbox("Time column", candidates if candidates else df.columns.tolist(), index=0)
                tmp = df[[time_col, metric_col]].copy()
                tmp[time_col] = tmp[time_col].astype(str)
                series = tmp.groupby(time_col)[metric_col].mean()
                fig = plt.figure()
                ax = fig.add_subplot(111)
                ax.plot(series.index.astype(str), series.values, marker="o")
                ax.set_title(f"{metric_col} over {time_col}")
                ax.tick_params(axis="x", rotation=30)
                st.pyplot(fig, clear_figure=True)

        st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
        st.markdown("**Quick summary**")
        st.write(df.describe(include="all"))


# -----------------------------
# Tab 3: Interpretable “ML-style” Scoring
# -----------------------------
with tab3:
    st.markdown(
        """
<div class="card">
  <div class="badge">🧠 Scoring Demo</div>
  <h3 style="margin:10px 0 0 0;">Interpretable scoring (ML-style) — visible logic</h3>
  <p class="small" style="margin-top:8px;">
    This is a “show the result” demo: a simple, explainable scoring function.
    In real systems, this becomes a trained model — but the UX is the same:
    inputs → score → explanation.
  </p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    left, right = st.columns([1, 1.1], gap="large")

    with left:
        st.markdown("### Inputs")
        complexity = st.slider("System complexity", 0, 100, 62)
        data_quality = st.slider("Data quality", 0, 100, 58)
        time_pressure = st.slider("Time pressure", 0, 100, 70)
        automation_level = st.slider("Automation level", 0, 100, 45)
        social_impact = st.slider("Social impact potential", 0, 100, 78)

        st.caption("These inputs mirror real decision systems: risk, readiness, and impact.")

    # Simple scoring (transparent)
    # Goal: High score if data_quality + automation + impact high, but penalize extreme time_pressure and complexity.
    score = (
        0.30 * data_quality
        + 0.22 * automation_level
        + 0.28 * social_impact
        - 0.12 * time_pressure
        - 0.08 * complexity
    )
    score = float(np.clip(score, 0, 100))

    with right:
        st.markdown("### Output")
        st.metric("Score", f"{score:,.1f} / 100")

        if score >= 75:
            verdict = "✅ Strong candidate for execution"
            note = "High value + solid readiness. This is worth shipping."
        elif score >= 55:
            verdict = "🟡 Promising, but needs refinement"
            note = "Good direction — improve data quality or reduce time pressure."
        else:
            verdict = "⚠️ Risky / not ready"
            note = "Too much uncertainty. Reduce complexity or increase data readiness."

        st.markdown(f"**Verdict:** {verdict}")
        st.write(note)

        st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
        st.markdown("**Explainability** (why the score looks like this)")
        st.write(
            {
                "Data quality (30%)": data_quality,
                "Automation (22%)": automation_level,
                "Social impact (28%)": social_impact,
                "Time pressure penalty (12%)": time_pressure,
                "Complexity penalty (8%)": complexity,
            }
        )

        st.caption("In production: swap this scoring with a trained model + calibration. The UI stays the same.")


st.markdown("<div class='hr'></div>", unsafe_allow_html=True)
st.caption("Lab is designed to make results visible — not just code.")
