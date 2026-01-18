import streamlit as st
from src.loaders import load_projects, filter_by_track

st.set_page_config(page_title="Lab", layout="wide")

st.title("Lab")
st.caption("Laboratorio técnico: modelos, simulaciones y demos.")

projects = load_projects()
lab_projects = filter_by_track(projects, "lab")

if not lab_projects:
    st.warning("No hay proyectos marcados como lab.")
    st.stop()

all_tags = sorted({t for p in lab_projects for t in p.get("stack", [])})
selected = st.multiselect("Filtrar por stack", all_tags)

def match(p):
    if not selected:
        return True
    return any(t in p.get("stack", []) for t in selected)

for p in filter(match, lab_projects):
    with st.container(border=True):
        st.subheader(p.get("title", "Untitled"))
        st.write(p.get("summary", ""))

        st.caption(f"Industria: {p.get('industry')} · Fecha: {p.get('date','')}")

        if p.get("metrics"):
            st.markdown("**Métricas**")
            st.json(p["metrics"], expanded=False)

        artifacts = p.get("artifacts", {})
        c1, c2, c3 = st.columns(3)

        if artifacts.get("demo"):
            c1.link_button("Demo", artifacts["demo"])
        if artifacts.get("repo"):
            c2.link_button("Repo", artifacts["repo"])
        if artifacts.get("report"):
            c3.link_button("Report", artifacts["report"])
