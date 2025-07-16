import streamlit as st

from helpers.navigation import make_sidebar
from scripts.htmlTemplates import css, hide_st_style, footer

st.set_page_config(page_title="Células: Inicio", layout="wide", page_icon="")
st.write(css, unsafe_allow_html=True)

t1, t2 = st.columns((0.5, 5))
t1.image("images/logo.png")
t2.title("Aposento Alto para las Naciones")
make_sidebar()
st.markdown("---")
st.header("¿Cómo registrar la información de las casas de bendición?")

# Footer
st.markdown(hide_st_style, unsafe_allow_html=True)
st.markdown(footer, unsafe_allow_html=True)
