import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""
<style>
.projects-wrapper {
    max-width: 1300px;
    margin: auto;
    padding-top: 40px;
}

.projects-title {
    font-size: 42px;
    font-weight: 900;
    margin-bottom: 6px;
}

.projects-sub {
    opacity: 0.7;
    margin-bottom: 40px;
}

.industry-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 26px;
}

.industry-card {
    position: relative;
    height: 230px;
    border-radius: 22px;
    padding: 22px;
    background: linear-gradient(135deg, #0f172a, #020617);
    border: 1px solid rgba(255,255,255,0.08);
    transition: all 0.3s ease;
    cursor: pointer;
    overflow: hidden;
}

.industry-card:hover {
    transform: translateY(-6px) scale(1.02);
    border-color: rgba(0,180,255,0.45);
    box-shadow: 0 0 30px rgba(0,160,255,0.18);
}

.industry-title {
    font-size: 20px;
    font-weight: 800;
    margin-bottom: 8px;
}

.industry-desc {
    font-size: 14px;
    opacity: 0.7;
    line-height: 1.4;
}

.industry-open {
    position: absolute;
    bottom: 18px;
    right: 22px;
    font-size: 13px;
    letter-spacing: 1px;
    opacity: 0.6;
}

.cardlink {
    position: absolute;
    inset: 0;
    z-index: 5;
}
</style>
""", unsafe_allow_html=True)

industries = [
    ("Bancos & Seguros", "Riesgo, fraude, scoring, churn, KPIs.", "2a_Bancos_Seguros"),
    ("Energía", "Optimización, confiabilidad, mantenimiento, forecasting.", "2b_Energia"),
    ("Entretenimiento", "Audiencias, recomendación, NLP, visión.", "3c_Entretenimiento"),
    ("Manufactura", "Calidad, visión artificial, gemelos digitales.", "2d_Manufactura"),
    ("Marketing", "Segmentación, atribución, LTV, performance.", "2e_Marketing"),
    ("Política", "Opinión pública, predicción, discurso, OSINT.", "2f_Politica"),
    ("Transporte", "Rutas, demanda, optimización, simulación.", "2g_Transporte"),
    ("Coming soon", "New industries under construction.", "")
]

html = []
html.append("<div class='projects-wrapper'>")
html.append("<div class='projects-title'>Projects</div>")
html.append("<div class='projects-sub'>Industries · Applied Data Science · AI Systems</div>")
html.append("<div class='industry-grid'>")

for title, desc, page in industries:
    link = f"/{page}" if page else "#"
    html.append(f"""
    <div class="industry-card">
        <a class="cardlink" href="{link}"></a>
        <div class="industry-title">{title}</div>
        <div class="industry-desc">{desc}</div>
        <div class="industry-open">OPEN →</div>
    </div>
    """)

html.append("</div></div>")

st.markdown("".join(html), unsafe_allow_html=True)
