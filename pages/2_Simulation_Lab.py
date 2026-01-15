import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Simulation Lab — Portfolio JRR", layout="wide")

st.title("Simulation Lab")
st.caption("Interactive demos — small, explainable systems that show how I design intelligence.")

st.divider()

st.subheader("Demo 001 — Monte Carlo: Scenario Outcomes")
st.write(
    """
A minimal Monte Carlo simulator to show: **assumptions → uncertainty → distribution → decision**.
Next we’ll replace this with a domain-specific demo (Finance / Sports / Energy).
"""
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    n = st.slider("Simulations", 2000, 50000, 12000, step=1000)
with col2:
    mu = st.slider("Expected value (μ)", -10.0, 10.0, 1.5, step=0.1)
with col3:
    sigma = st.slider("Volatility (σ)", 0.1, 10.0, 2.5, step=0.1)
with col4:
    threshold = st.slider("Decision threshold", -10.0, 10.0, 0.0, step=0.1)

seed = st.number_input("Random seed", value=42, step=1)

rng = np.random.default_rng(int(seed))
samples = rng.normal(mu, sigma, n)

df = pd.DataFrame({"outcome": samples})
p_above = float((samples > threshold).mean())
p_tail_hi = float((samples > (mu + sigma)).mean())
p_tail_lo = float((samples < (mu - sigma)).mean())

m1, m2, m3 = st.columns(3)
m1.metric("P(outcome > threshold)", f"{p_above*100:.1f}%")
m2.metric("Upper tail P(> μ+σ)", f"{p_tail_hi*100:.1f}%")
m3.metric("Lower tail P(< μ-σ)", f"{p_tail_lo*100:.1f}%")

fig = px.histogram(df, x="outcome", nbins=60, title="Outcome Distribution")
fig.add_vline(x=threshold, line_width=2, line_dash="dash")
st.plotly_chart(fig, use_container_width=True)

st.markdown("### Interpretation")
st.write(
    """
- **μ** shifts the center (expected performance).
- **σ** controls uncertainty (risk).
- The **threshold** represents the policy line: _accept / reject / act / no-act_.
- This is the building block for real decision systems: **simulate → evaluate regimes → choose a policy**.
"""
)

st.markdown("### Next upgrade (after deploy)")
st.write(
    """
- Add **two regimes** (bull vs bear / favorite dominates vs underdog controls pace).
- Add **EV / risk metrics** and scenario weights.
- Tie it to a real domain (Finance risk, NFL props, Energy demand).
"""
)
