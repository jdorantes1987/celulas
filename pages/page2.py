import streamlit as st

from helpers.navigation import make_sidebar
from scripts.Celulas import DataCelulas

st.set_page_config(page_title="Células: Inicio", layout="wide", page_icon="⚡")
make_sidebar()

data = DataCelulas()

st.session_state.liderazgo = data.liderazgo()
st.dataframe(st.session_state.liderazgo, use_container_width=False, hide_index=True)
