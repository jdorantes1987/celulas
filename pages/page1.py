import streamlit as st

from helpers.navigation import make_sidebar

st.set_page_config(page_title="Células: Inicio", layout="wide", page_icon="⚡")

t1, t2 = st.columns((0.5, 5))
t1.image("images/logo.png")
t2.title("Aposento Alto para las Naciones")
make_sidebar()
st.markdown("---")
st.header("¿Cómo registrar la información de las casas de bendición?")
