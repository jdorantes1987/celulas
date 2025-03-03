import streamlit as st
from numpy import nan

from helpers.navigation import make_sidebar
from scripts.oDiscipulados import DataDiscipulados

st.set_page_config(
    page_title="Discipulados - Registro de sobres", layout="wide", page_icon="⚡"
)
make_sidebar()
data = DataDiscipulados()

st.header("Datos del sobre")


if "stage" not in st.session_state:
    st.session_state.stage = 0


def set_state(i):
    st.session_state.stage = i


if st.session_state.stage == 0:
    st.session_state.w_exp = ""
    st.session_state.w_tema = ""
    st.session_state.w_observ = ""
    st.session_state.w_n_asist = 10
    st.session_state.w_m_bs = 0
    st.session_state.w_m_usd = 0
    set_state(1)


@st.cache_data
def liderazgo_activo():
    df = data.liderazgo()
    return df[df["estatus"] == 1]


@st.cache_data
def liderazgo_redes():
    return data.liderazgo_redes()


liderazgo = liderazgo_activo()
col1, col2 = st.columns(2, gap="small")
with col1:
    id_liderazgo = st.text_input(
        label="id liderazgo",
        value=liderazgo.iloc[0, 1],
        disabled=True,
    )
with col2:
    nombre = st.text_input(
        label="nombre",
        value=liderazgo.iloc[0, 2],
        disabled=True,
    )

col3, col4, col5 = st.columns(3, gap="small")

with col3:
    fecha_celula = st.date_input("fecha dicipulado")
with col4:
    fecha_recibido = st.date_input("fecha recibido")
with col5:
    fecha_entregado = st.date_input("fecha entregado")

col6, col7, col8 = st.columns(3, gap="small")

with col6:
    redes = liderazgo_redes().replace(nan, "").copy()
    redes["buscador"] = redes["cod_red"] + " | " + redes["c_lider"]
    cod_red = st.selectbox(
        "Lista de redes:",
        redes["buscador"],
        index=None,
        placeholder="seleccionar..",
    )

    cod_red = str.strip(cod_red.split("|")[0]) if cod_red is not None else ""


with col7:
    expositor = st.text_input(
        label="expositor",
        key="w_exp",
        disabled=False,
        placeholder="ingrese el nombre del expositor del tema.",
    )
with col8:
    tema = st.text_input(
        label="tema",
        key="w_tema",
        disabled=False,
        placeholder="ingrese el tema impartido.",
    )

numero_asistentes = st.slider(
    "número de asistentes",
    min_value=0,
    max_value=100,
    key="w_n_asist",
)
bs = st.number_input("ingrese el monto en bolívares.", key="w_m_bs")
usd = st.number_input("ingrese el monto en dólares.", key="w_m_usd")

sobre_entregado = st.checkbox("sobre entregado?")
if sobre_entregado:
    sobre_entregado = True

observ = st.text_input(
    label="observaciones",
    key="w_observ",
    disabled=False,
    placeholder="ingrese las observaciones",
)

registro = [
    (
        None,
        id_liderazgo,
        fecha_celula,
        fecha_recibido,
        fecha_entregado,
        cod_red,
        expositor,
        tema,
        numero_asistentes,
        bs,
        usd,
        sobre_entregado,
        observ,
    )
]

if st.button("agregar"):
    # data.insert_hist_discipulados(registro)
    set_state(3)

if st.session_state.stage >= 3:
    st.info("Registro insertado.")
    col1, col2 = st.columns([0.1, 0.1])
    with col1:
        col1.button("Continuar con otro registro?", on_click=set_state, args=[0])
    with col2:
        col2.button("ir a estadisticas", on_click=set_state, args=[4])

if st.session_state.stage == 4:
    del st.session_state.stage
    st.switch_page("pages/page5.py")
