import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="About me | Portfolio JRR", page_icon="🛰️", layout="wide")
st.warning("RUNNING 1_About_Me.py — build 2026-01-18 17:05 ✅")


# =========================
# GLOBAL STYLES
# =========================
CSS = """
<style>
.block-container { padding-top: 2rem; padding-bottom: 2.5rem; max-width: 1200px; }

html, body, [data-testid="stAppViewContainer"] {
  background: radial-gradient(1200px 600px at 20% 0%, rgba(255,255,255,0.06), transparent 60%),
              radial-gradient(900px 500px at 80% 30%, rgba(255,255,255,0.04), transparent 55%),
              #0b0f14;
}

.card {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 18px;
  padding: 18px 18px;
  box-shadow: 0 10px 35px rgba(0,0,0,0.25);
  backdrop-filter: blur(10px);
}

.card h2, .card h3 { margin: 0 0 10px 0; }
.muted { color: rgba(255,255,255,0.72); }
.tight p { margin-bottom: 0.6rem; }

.chips { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px; }
.chip {
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.16);
  background: rgba(255,255,255,0.03);
  color: rgba(255,255,255,0.86);
  font-size: 13px;
}

[data-testid="stMetric"] {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 14px;
  padding: 10px 12px;
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

def card(inner_html: str, height: int = 10):
    """
    Render seguro (evita que se muestre como bloque de código con botón copiar).
    height se auto-ajusta con 'scrolling=False' pero Streamlit requiere un número.
    """
    html = f"""
    {CSS}
    {inner_html}
    """
    components.html(html, height=height, scrolling=False)

st.title("About me")

# =========================
# HERO
# =========================
card(
    """
<div class="card tight">
  <h3>Jorge Reyes — Engineer · Data Scientist · Technical Architect</h3>
  <p class="muted">
    Construyo soluciones donde convergen <b>ingeniería, datos y sistemas complejos</b>.
    Me muevo entre la ejecución técnica (código, modelos, dashboards, automatización) y el análisis profundo de
    <b>cómo se comportan los sistemas</b>: técnicos, industriales y sociales.
  </p>
  <p class="muted">Este portafolio es dos cosas al mismo tiempo:</p>
  <ul class="muted">
    <li>🧾 Un <b>perfil profesional claro</b> (lo que he hecho, cómo genero impacto y qué sé construir)</li>
    <li>🧪 Un <b>laboratorio activo</b> (experimentos, modelos, simulaciones y documentación técnica)</li>
  </ul>

  <div class="chips">
    <span class="chip">Python</span>
    <span class="chip">Data Science</span>
    <span class="chip">Simulación / Monte Carlo</span>
    <span class="chip">Power BI</span>
    <span class="chip">Sistemas complejos</span>
  </div>
</div>
""",
    height=260,
)

st.write("")
st.markdown("## At a glance")
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Enfoque", "Sistemas + Datos")
with c2:
    st.metric("Entrega", "End-to-end")
with c3:
    st.metric("Método", "Evidencia / Métricas")
with c4:
    st.metric("Estilo", "Arquitectura + ejecución")

st.write("")

# =========================
# PROFESSIONAL PROFILE
# =========================
st.markdown("## Professional profile")
left, right = st.columns([1, 2], gap="large")

with left:
    card(
        """
<div class="card">
  <h3>Professional profile</h3>
  <p class="muted">
    Me especializo en convertir complejidad en estructura:
    modelar el sistema, entender dinámicas, y proponer mejoras medibles con datos.
  </p>
  <ul class="muted">
    <li>Análisis, preparación y modelado de datos</li>
    <li>Dashboards y métricas accionables</li>
    <li>Automatización y reducción de fricción</li>
    <li>Comunicación clara para decisión</li>
  </ul>
</div>
""",
        height=290,
    )

with right:
    card(
        """
<div class="card">
  <h3>Cómo trabajo</h3>
  <p class="muted">
    Soy ingeniero industrial y mecatrónico con enfoque en <b>ciencia de datos, analítica avanzada y diseño de sistemas</b>.
  </p>
  <p class="muted">
    Me muevo bien en problemas que no vienen “limpios”: múltiples variables y restricciones reales, información incompleta,
    trade-offs técnicos y de negocio, y consecuencias operativas/económicas.
  </p>
  <p class="muted">
    Lo que mejor hago es <b>convertir complejidad en estructura</b>: definir el sistema, traducirlo a datos,
    construir una solución medible y comunicar decisiones con claridad.
  </p>

  <h3 style="margin-top:14px;">What I build</h3>
  <ul class="muted">
    <li><b>Dashboards y métricas</b> (Power BI / Plotly) para monitoreo y decisión</li>
    <li><b>Modelos predictivos</b> (clasificación, regresión, NLP) con evaluación seria</li>
    <li><b>Simulaciones Monte Carlo</b> para escenarios, incertidumbre y riesgo</li>
    <li><b>Pipelines y automatización</b> (SQL/Python) para reducir fricción y tiempo manual</li>
    <li><b>Arquitecturas simples pero robustas</b>: datos → lógica → visualización → decisión</li>
  </ul>

  <h3 style="margin-top:14px;">What I’m looking for</h3>
  <p class="muted">
    Roles donde se crucen: <b>ingeniería · datos · automatización · toma de decisiones</b> y se valore:
    <b>pensamiento sistémico, calidad técnica y comunicación clara</b>.
  </p>
</div>
""",
        height=520,
    )

st.write("")

# =========================
# LAB MINDSET
# =========================
st.markdown("## My lab mindset")
card(
    """
<div class="card">
  <p class="muted">
    Este portafolio no es solo un escaparate de resultados finales.
    Es un <b>laboratorio técnico en evolución</b>: documento proceso, supuestos, métricas y límites.
  </p>
  <p class="muted">
    Mi enfoque es el de un <b>arquitecto de sistemas</b>: entender el todo antes de optimizar las partes.
    Eso incluye modelar flujos, dependencias, incentivos y efectos secundarios.
  </p>
  <h3 style="margin-top:14px;">What you’ll find in my lab</h3>
  <ul class="muted">
    <li>🔬 Modelos predictivos + explicación de features, errores y trade-offs</li>
    <li>📊 EDA serio: sesgos, distribución, calidad de datos, leakage</li>
    <li>⚙️ Automatización: scripts, loaders, estructura de datos, reproducibilidad</li>
    <li>🧠 Experimentos: baseline → iteración → comparación → conclusión</li>
    <li>🛰️ Proyectos “real-world”: supuestos explícitos, limitaciones y decisiones accionables</li>
  </ul>
</div>
""",
    height=360,
)

st.write("")



# =========================
# STACK & TOOLS
# =========================
st.markdown("## Stack & tools")
col1, col2 = st.columns(2, gap="large")

with col1:
    card(
        """
<div class="card">
  <h3>Data & Modeling</h3>
  <ul class="muted">
    <li>Python (pandas, NumPy)</li>
    <li>Scikit-learn</li>
    <li>Simulación / Monte Carlo</li>
    <li>Estadística aplicada</li>
    <li>Visualización (Plotly, Power BI)</li>
  </ul>
</div>
""",
        height=260,
    )

with col2:
    card(
        """
<div class="card">
  <h3>Engineering & Systems</h3>
  <ul class="muted">
    <li>Diseño de sistemas técnicos</li>
    <li>Automatización de procesos (Python/SQL)</li>
    <li>Optimización y trade-offs</li>
    <li>Documentación técnica</li>
    <li>Pensamiento sistémico (arquitectura + ejecución)</li>
  </ul>
</div>
""",
        height=260,
    )

st.write("")

# =========================
# LINES OF WORK
# =========================
st.markdown("## Lines of work")
card(
    """
<div class="card">
  <p class="muted">Actualmente desarrollo proyectos en:</p>
  <ul class="muted">
    <li>📊 <b>Data Science & Analytics</b></li>
    <li>⚙️ <b>Ingeniería aplicada e industrial</b></li>
    <li>🧪 <b>Simulación, optimización y modelos complejos</b></li>
    <li>🏭 <b>Manufactura / energía / operaciones</b></li>
    <li>🏛️ <b>Análisis social y político basado en datos</b></li>
  </ul>
  <p class="muted">
    Cada proyecto en <b>Projects</b> y <b>Lab</b> está tratado como si fuera parte de un entorno real:
    supuestos claros, métricas, limitaciones y conclusiones accionables.
  </p>
</div>
""",
    height=320,
)

