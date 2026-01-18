import streamlit as st

st.set_page_config(page_title="About me | Portfolio JRR", page_icon="🛰️", layout="wide")

st.title("About me")

# =========================
# HERO
# =========================
st.markdown(
    """
### Jorge Reyes  
**Engineer · Data Scientist · Technical Architect**

Construyo soluciones donde convergen **ingeniería, datos y sistemas complejos**.  
Me muevo entre la ejecución técnica (código, modelos, dashboards, automatización) y el análisis profundo de **cómo se comportan los sistemas**: técnicos, industriales y sociales.

Este portafolio es dos cosas al mismo tiempo:

- 🧾 Un **perfil profesional claro** (lo que he hecho, cómo genero impacto y qué sé construir)
- 🧪 Un **laboratorio activo** (experimentos, modelos, simulaciones y documentación técnica)
"""
)

# =========================
# QUICK SIGNALS (reclutador-friendly)
# =========================
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

st.divider()

# =========================
# PROFESSIONAL PROFILE
# =========================
st.markdown("## Professional profile")

st.markdown(
    """
Soy ingeniero industrial y mecatrónico con enfoque en **ciencia de datos, analítica avanzada y diseño de sistemas**.

Me especializo en trabajar donde los problemas **no vienen “limpios”**:
- múltiples variables y restricciones reales,
- información incompleta,
- trade-offs técnicos y de negocio,
- y consecuencias operativas / económicas.

Lo que mejor hago es **convertir complejidad en estructura**:
definir el sistema, traducirlo a datos, construir una solución medible y comunicar decisiones con claridad.
"""
)

st.markdown("### What I build")
st.markdown(
    """
- **Dashboards y métricas** para monitoreo y toma de decisiones (Power BI / Plotly)
- **Modelos predictivos** (clasificación, regresión, NLP) y evaluación seria
- **Simulaciones Monte Carlo** para escenarios, incertidumbre y riesgo
- **Pipelines y automatización** (SQL/Python) para reducir fricción y tiempo manual
- **Arquitecturas simples pero robustas**: datos → lógica → visualización → decisión
"""
)

st.markdown("### What I’m looking for")
st.markdown(
    """
Roles donde se crucen: **ingeniería · datos · automatización · toma de decisiones**  
y donde se valore: **pensamiento sistémico, calidad técnica y comunicación clara**.
"""
)

st.divider()

# =========================
# LAB MINDSET
# =========================
st.markdown("## My lab mindset")

st.markdown(
    """
Este portafolio no es solo un escaparate de resultados finales.  
Es un **laboratorio técnico en evolución**: aquí documento el proceso, los supuestos, las métricas y los límites.

Mi enfoque es el de un **arquitecto de sistemas**:
entender el todo antes de optimizar las partes. Eso incluye modelar flujos, dependencias, incentivos y efectos secundarios.
"""
)

st.markdown("### What you’ll find in my lab")
st.markdown(
    """
- 🔬 Modelos predictivos + explicación de features, errores y trade-offs  
- 📊 EDA serio: sesgos, distribución, calidad de datos, leakage  
- ⚙️ Automatización: scripts, loaders, estructura de datos, reproducibilidad  
- 🧠 Experimentos: baseline → iteración → comparación → conclusión  
- 🛰️ Proyectos “real-world”: supuestos explícitos, limitaciones y decisiones accionables  
"""
)

st.divider()

# =========================
# SOCIAL & POLITICAL (evidence-driven)
# =========================
st.markdown("## Social & political analysis (evidence-driven)")

st.markdown(
    """
Además de sistemas técnicos, me interesa profundamente entender **cómo funcionan los sistemas sociales y políticos**.

No lo abordo desde ideología, sino desde un enfoque **analítico y estructural**:
**datos → incentivos → comportamiento colectivo → consecuencias**.

Me interesa construir herramientas y análisis que ayuden a:
- entender el sistema tal como es,
- medir impacto,
- evaluar escenarios,
- y proponer mejoras basadas en evidencia.
"""
)

st.markdown("### Topics I explore")
st.markdown(
    """
- 🏛️ **Política pública y regulación:** qué incentiva realmente una regla  
- 📈 **Evaluación de impacto:** antes/después, contrafactuales, métricas útiles  
- 🗳️ **Opinión pública y comportamiento electoral:** patrones, segmentación, sesgos  
- ⚖️ **Diseño de incentivos:** por qué las reglas producen resultados inesperados  
- 🌎 **Acceso a oportunidades:** desigualdad, movilidad, “cuellos de botella” del sistema  
"""
)

st.markdown(
    """
> Mi objetivo no es “opinar más fuerte”, sino **modelar mejor**: identificar palancas de mejora y riesgos de implementación.
"""
)

st.divider()

# =========================
# STACK & TOOLS
# =========================
st.markdown("## Stack & tools")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
**Data & Modeling**
- Python (pandas, NumPy)
- Scikit-learn
- Simulación / Monte Carlo
- Estadística aplicada
- Visualización (Plotly, Power BI)
"""
    )

with col2:
    st.markdown(
        """
**Engineering & Systems**
- Diseño de sistemas técnicos
- Automatización de procesos (Python/SQL)
- Optimización y trade-offs
- Documentación técnica
- Pensamiento sistémico (arquitectura + ejecución)
"""
    )

st.divider()

# =========================
# LINES OF WORK
# =========================
st.markdown("## Lines of work")

st.markdown(
    """
Actualmente desarrollo proyectos en:

- 📊 **Data Science & Analytics**
- ⚙️ **Ingeniería aplicada e industrial**
- 🧪 **Simulación, optimización y modelos complejos**
- 🏭 **Manufactura / energía / operaciones**
- 🏛️ **Análisis social y político basado en datos**

Cada proyecto en **Projects** y **Lab** está tratado como si fuera parte de un entorno real:
con supuestos claros, métricas, limitaciones y conclusiones accionables.
"""
)
