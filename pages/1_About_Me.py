import streamlit as st

st.title("About me")

# =========================
# HERO
# =========================
st.markdown("""
### Jorge Reyes  
**Engineer · Data Scientist · Technical Architect**

Construyo soluciones donde convergen **ingeniería, datos y sistemas complejos**.  
Mi trabajo se mueve entre la ejecución técnica real y el análisis profundo de cómo funcionan los sistemas — técnicos, industriales y sociales.

Este portafolio es dos cosas al mismo tiempo:

- 🧾 Un **perfil profesional claro** para roles técnicos y estratégicos  
- 🧪 Un **laboratorio activo** donde analizo, modelo y experimento con sistemas reales
""")

# =========================
# PERFIL PROFESIONAL
# =========================
st.markdown("## Professional profile")

st.markdown("""
Ingeniero industrial y mecatrónico con enfoque en **ciencia de datos, analítica avanzada y diseño de sistemas**.

He trabajado en contextos donde los problemas no vienen “limpios”, sino con:
- múltiples variables,
- restricciones reales,
- información incompleta,
- y consecuencias operativas, económicas o sociales.

Mi especialidad es **convertir complejidad en estructura**:
modelar el sistema, entender sus dinámicas y proponer mejoras medibles.

Busco roles donde se crucen:
**ingeniería · datos · automatización · toma de decisiones**.
""")

# =========================
# MENTALIDAD DE LABORATORIO
# =========================
st.markdown("## My lab mindset")

st.markdown("""
Este portafolio no es solo un escaparate de resultados finales.  
Es un **laboratorio técnico y analítico en evolución**.

Aquí desarrollo y documento:

- 🔬 Modelos predictivos y de simulación  
- 📊 Análisis de comportamiento y patrones  
- ⚙️ Arquitecturas de datos y flujos técnicos  
- 🧠 Experimentos con machine learning y estadística  
- 🛰️ Proyectos que conectan software, industria y realidad  

Mi enfoque es el de un **arquitecto de sistemas**:  
entender el todo antes de optimizar las partes.
""")

# =========================
# DIMENSION SOCIAL Y POLITICA
# =========================
st.markdown("## Social & political analysis projects")

st.markdown("""
Además de sistemas técnicos, me interesa profundamente **entender cómo funcionan los sistemas sociales y políticos**.

No desde una postura ideológica, sino desde un enfoque **analítico y estructural**:
datos, incentivos, comportamiento colectivo y consecuencias.

Desarrollo proyectos orientados a:

- 🏛️ **Análisis de políticas públicas**  
- 📈 Evaluación de impacto social  
- 🗳️ Comportamiento electoral y opinión pública  
- ⚖️ Sistemas de incentivos, regulación y toma de decisiones  
- 🌎 Dinámicas sociales, desigualdad y acceso a oportunidades  

El objetivo no es opinar, sino **entender el sistema para identificar palancas de mejora**.
""")

st.markdown("""
Creo que muchos problemas sociales y políticos pueden analizarse como sistemas:
con entradas, procesos, retroalimentaciones y salidas.

Aplicar herramientas de ingeniería y ciencia de datos a estos dominios permite:
- detectar fallas estructurales,
- evaluar escenarios,
- y proponer soluciones basadas en evidencia.
""")

# =========================
# STACK Y HERRAMIENTAS
# =========================
st.markdown("## Stack & tools")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
**Data & Modeling**
- Python (pandas, NumPy)
- Scikit-learn, TensorFlow
- Simulación y Monte Carlo
- Estadística aplicada
- Visualización (Plotly, Power BI)
""")

with col2:
    st.markdown("""
**Engineering & Systems**
- Diseño de sistemas técnicos
- Automatización de procesos
- Análisis industrial
- Optimización
- Documentación técnica y modelado
""")

# =========================
# LINEAS DE TRABAJO
# =========================
st.markdown("## Lines of work")

st.markdown("""
Actualmente desarrollo proyectos en:

- 📊 Data Science & Analytics  
- ⚙️ Ingeniería aplicada e industrial  
- 🏭 Energía, manufactura y sistemas productivos  
- 🧪 Simulación, optimización y modelos complejos  
- 🏛️ Análisis social y político basado en datos  

Cada proyecto que aparece en **Projects** y **Lab** está tratado como si fuera parte de un entorno real:
con supuestos claros, métricas, limitaciones y conclusiones accionables.
""")
