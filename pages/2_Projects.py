import streamlit as st
from src.loaders import load_projects, group_by_industry

st.set_page_config(page_title="Projects", layout="wide")

projects, errors = load_projects()

st.title("Projects")
st.caption("Organizados por industria. Fuente: data/projects.yaml")

if errors:
    st.error("Hay errores en projects.yaml:")
    for e in errors:
        st.write(f"- {e}")
    st.stop()

if not projects:
    st.warning("Aún no hay proyectos. Agrega entradas en data/projects.yaml")
    st.stop()

grouped = group_by_industry(projects)

for industry, items in grouped.items():
    with st.expander(f"{industry} ({len(items)})", expanded=False):
        for p in items:
            with st.container(border=True):
                st.subheader(p["title"])
                st.write(p["summary"])

                meta = f"**Fecha:** {p.get('date','')} · **Status:** {p.get('status','')}"
                st.markdown(meta)

                if p.get("highlights"):
                    st.markdown("**Highlights**")
                    for h in p["highlights"]:
                        st.markdown(f"- {h}")

                artifacts = p.get("artifacts", {}) or {}
                cols = st.columns(3)
                if artifacts.get("demo"):
                    cols[0].link_button("Demo", artifacts["demo"])
                if artifacts.get("repo"):
                    cols[1].link_button("Repo", artifacts["repo"])
                if artifacts.get("report"):
                    cols[2].link_button("Report", artifacts["report"])
