import streamlit as st

st.set_page_config(page_title="Industries — Portfolio JRR", layout="wide")

st.title("Industries")
st.caption("Projects organized by domain — inspired by IBM Solutions. Select a domain to explore case files and demos.")

domains = [
    "Finance • Banking • Insurance",
    "Sports Analytics",
    "Energy",
    "Manufacturing",
    "Healthcare",
    "Transportation & Logistics",
    "Politics & Public Systems",
    "Marketing & Growth",
]

# Sidebar selector (clean UX)
with st.sidebar:
    st.subheader("Domain")
    selected = st.radio("Select", domains, index=0)

st.divider()

# ---- Domain pages (scaffold + 1 fully written) ----
if selected == "Finance • Banking • Insurance":
    st.subheader("Finance • Banking • Insurance")
    st.write(
        """
This domain is about **decision-making under uncertainty**.
The goal is to extract signal from noisy environments and translate it into reliable actions.

**Typical problems**
- Risk scoring (PD / risk tiers / underwriting)
- Fraud & anomaly detection (behavior shifts, outliers)
- Forecasting (volume, demand, liquidity proxies)
- Decision engines (policies, thresholds, calibration, monitoring)

**What I build**
- End-to-end pipelines: data → features → model → evaluation → monitoring
- Explainable scoring systems and scenario testing
- Simulation-driven decision support (stress tests / what-if analysis)
"""
    )

    st.markdown("### Core Capabilities")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Signals", "Structured + Behavioral")
    c2.metric("Modeling", "Supervised / TS / Anomaly")
    c3.metric("Outputs", "Scores • Forecasts")
    c4.metric("Focus", "Robustness")

    st.markdown("### Case Files (starter)")
    st.info("Replace these placeholders with your real projects. We'll build the first case file next.")
    st.markdown("- **Case File 001 — Risk Scoring Engine** (coming soon)")
    st.markdown("- **Case File 002 — Anomaly Detection System** (coming soon)")
    st.markdown("- **Case File 003 — Forecasting & Stress Testing** (coming soon)")

    st.markdown("### Related Demo")
    st.write("Monte Carlo scenario outcomes (in Simulation Lab).")
    if st.button("Open Simulation Lab", use_container_width=True):
        st.switch_page("pages/2_Simulation_Lab.py")

else:
    st.subheader(selected)
    st.write("Scaffold ready. We’ll populate this domain next with real case files + demos.")
    st.markdown("### What will live here")
    st.markdown("- Context of the domain")
    st.markdown("- 2–4 case files with outcomes and links")
    st.markdown("- 1 interactive demo or dashboard")

Add Industries page

