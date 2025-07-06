import datetime

import streamlit as st
from pandas import to_datetime

from helpers.navigation import make_sidebar
from scripts.oCelulas import DataCelulas
from scripts.oDiscipulados import DataDiscipulados

st.set_page_config(page_title="Estadísticas Generales", layout="wide", page_icon="⚡")

make_sidebar()
oCelulas = DataCelulas()
oDicipulados = DataDiscipulados()
today = datetime.datetime.now()


@st.cache_data
def celulas_activas():
    return oCelulas.celulas_activas()


@st.cache_data
def celulas_activas_historico():
    return oCelulas.celulas_activas_hist()


@st.cache_data
def get_dicipulados():
    return oDicipulados.get_discipulados()


@st.cache_data
def get_dicipulados_activos():
    data = oDicipulados.get_discipulados()
    return data[data["estatus_liderazgo"] == 1]


# Título principal
st.title("Estadísticas Generales")

# Layout profesional con columnas
col1, col2 = st.columns(2)

with col1:
    st.subheader("Células activas")
    celulas_activas_df = celulas_activas()
    st.metric(
        label="Células activas",
        value=celulas_activas_df.shape[0],
    )

with col2:
    st.subheader("Discipulados activos")
    dicipulados_activos_df = get_dicipulados_activos()
    st.metric(
        label="Discipulados activos",
        value=dicipulados_activos_df.shape[0],
    )

st.markdown("---")

# Sección de detalles históricos (opcional)
with st.expander("Ver células activas"):
    historico = celulas_activas().copy()
    # Ocultar algunas columnas
    historico = historico.drop(
        columns=["id_cod", "estatus_celula", "id_liderazgo", "estatus_liderazgo"]
    )
    st.dataframe(historico, use_container_width=True, hide_index=True)

with st.expander("Ver discipulados activos"):
    discipulados = get_dicipulados_activos().copy()
    # Ocultar algunas columnas
    discipulados = discipulados.drop(
        columns=[
            "id_discipulado",
            "id_cod",
            "cod_base",
            "c_lider_red",
            "id_liderazgo",
            "estatus_liderazgo",
            "nombre_lider",
        ]
    )
    st.dataframe(discipulados, use_container_width=True, hide_index=True)
