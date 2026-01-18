import streamlit as st
from src.loaders import load_projects, filter_by_track

st.set_page_config(page_title="Lab", layout="wide")

projects, errors = load_projects()

st.title("Lab")
st.caption("Exploraciones técnicas: modelos, simulaciones, notebooks. Fuente: data/projects.yaml")

if errors:
    st.error("Hay errores en projects.yaml:")
    for e in errors:
        st.write(f"- {e}")
    st.stop()

lab = filter_by_track(projects, "lab")

if not lab:
    st.warning('No hay proyectos con tracks: ["lab"].')
    st.stop()

# filtros opcionales
all_stack = sorted({s for p in lab for s in (p.get("stack") or [])})
selected_stack = st.multiselect("Filtrar por stack", all_stack)

def ok(p):
    if not selected_stack:
        return True
    return any(s in (p.get("stack") or []) for s in selected_stack)

for p in filter(ok, lab):
    with st.container(border=True):
        st.subheader(p["title"])
        st.write(p["summary"])
        st.markdown(f"**Industria:** {p.get('industry','')} · **Fecha:** {p.get('date','')}")

        if p.get("stack"):
            st.caption(" · ".join(p["stack"]))

        if p.get("metrics"):
            st.markdown("**Metrics (quick view)**")
            st.json(p["metrics"], expanded=False)

        artifacts = p.get("artifacts", {}) or {}
        cols = st.columns(3)
        if artifacts.get("demo"):
            cols[0].link_button("Demo", artifacts["demo"])
        if artifacts.get("repo"):
            cols[1].link_button("Repo", artifacts["repo"])
        if artifacts.get("report"):
            cols[2].link_button("Report", artifacts["report"])
