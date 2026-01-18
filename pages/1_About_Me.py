import streamlit as st

st.set_page_config(page_title="About me | Portfolio JRR", page_icon="🛰️", layout="wide")

# KILL SWITCH también aquí, por si algún otro page imprime codeblocks
st.markdown("""
<style>
div[data-testid="stCodeBlock"] { display:none !important; }
pre { display:none !important; }
</style>
""", unsafe_allow_html=True)

st.title("About me")
st.write("Esta página está en construcción. (Home ya incluye una sección About con ancla #about).")
