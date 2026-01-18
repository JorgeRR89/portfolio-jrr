import streamlit as st
from src.loaders import load_projects, group_by_industry, ordered_industries

st.set_page_config(page_title="Projects", layout="wide")

st.title("Projects")
st.caption("Portafolio organizado por industria.")

projects = load_projects()

if not projects:
    st.warning("No hay proyectos aún. Agrega proyectos en data/projects.yaml")
    st.stop()

grouped = group_by_industry(projects)

for industry in ordered_industries(grouped):
    with st.expander(industry, expanded=False):
        for p in grouped[industry]:
            with st.container(border=True):
                st.subheader(p.get("title", "Untitled"))
                st.write(p.get("summary", ""))

                st.caption(
                    f"Tracks: {', '.join(p.get('tracks', []))} · "
                    f"Stack: {' · '.join(p.get('stack', []))}"
                )

                for h in p.get("highlights", []):
                    st.markdown(f"- {h}")

                artifacts = p.get("artifacts", {})
                c1, c2, c3 = st.columns(3)

                if artifacts.get("demo"):
                    c1.link_button("Demo", artifacts["demo"])
                if artifacts.get("repo"):
                    c2.link_button("Repo", artifacts["repo"])
                if artifacts.get("report"):
                    c3.link_button("Report", artifacts["report"])
