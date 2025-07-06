import streamlit as st
from numpy import nan

from helpers.navigation import make_sidebar
from scripts.oCelulas import DataCelulas

st.set_page_config(
    page_title="Células - Registro de sobres", layout="wide", page_icon="⚡"
)
make_sidebar()
data = DataCelulas()

st.header("Datos del sobre")


@st.cache_data
def liderazgo_activo():
    df = data.liderazgo()
    return df[df["estatus"] == 1]


@st.cache_data
def celulas_activas():
    return data.celulas_activas()


@st.cache_data
def temas():
    return data.temas()


if "stage" not in st.session_state or "liderazgo" not in st.session_state:
    st.session_state.stage = 0
    st.session_state.liderazgo = None


def set_state(i):
    st.session_state.stage = i


if st.session_state.stage == 0:
    st.session_state.liderazgo = liderazgo_activo()
    st.session_state.w_exp = ""
    st.session_state.w_observ = ""
    st.session_state.w_n_asist = 10
    st.session_state.w_m_bs = 0
    st.session_state.w_m_usd = 0
    st.session_state.w_s_entr = False
    set_state(1)

col1, col2 = st.columns(2, gap="small")
with col1:
    id_liderazgo = st.text_input(
        label="id liderazgo",
        value=st.session_state.liderazgo.iloc[0, 1],
        disabled=True,
    )
with col2:
    nombre = st.text_input(
        label="nombre",
        value=st.session_state.liderazgo.iloc[0, 2],
        disabled=True,
    )

col3, col4, col5 = st.columns(3, gap="small")

with col3:
    fecha_celula = st.date_input("fecha célula")
with col4:
    fecha_recibido = st.date_input("fecha recibido")
with col5:
    fecha_entregado = st.date_input("fecha entregado")

celulas = celulas_activas().replace(nan, "").copy()
celulas["buscador"] = (
    celulas["id_celula"]
    + " | "
    + celulas["cod_red"]
    + " | "
    + celulas["c_lider"]
    + " | "
    + celulas["anfitriones"]
    + " | "
    + celulas["direccion"]
)
id_celula = st.selectbox(
    "Lista de células:",
    celulas["buscador"],
    index=None,
    placeholder="seleccionar..",
)

id_celula = str.strip(id_celula.split("|")[0]) if id_celula is not None else ""

col6, col7 = st.columns(2, gap="small")

with col6:
    expositor = st.text_input(
        label="expositor",
        disabled=False,
        key="w_exp",
        placeholder="ingrese el nombre del expositor del tema",
        autocomplete="on",
    )

with col7:
    temas = temas().copy()
    temas["buscador"] = temas["id_tema"] + " | " + temas["descrip"]
    tema_select = st.selectbox(
        "lista de temas:",
        temas["buscador"],
        index=None,
        placeholder="seleccionar..",
    )
    tema_select = (
        str.strip(tema_select.split("|")[0]) if tema_select is not None else ""
    )

numero_asistentes = st.slider("número de asistentes", 0, 100, key="w_n_asist")
bs = st.number_input("ingrese el monto en bolívares.", key="w_m_bs")
usd = st.number_input("ingrese el monto en dólares.", key="w_m_usd")

sobre_entregado = st.checkbox("sobre entregado?", key="w_s_entr")

observ = st.text_input(
    label="observaciones",
    disabled=False,
    key="w_observ",
    placeholder="ingrese las observaciones",
    autocomplete="on",
)

registro = [
    (
        None,
        id_liderazgo,
        fecha_celula,
        fecha_recibido,
        fecha_entregado,
        id_celula,
        expositor,
        tema_select,
        numero_asistentes,
        bs,
        usd,
        sobre_entregado,
        observ,
    )
]

if st.button("agregar"):
    data.insert_hist_celulas(registro)
    set_state(3)

# if st.session_state.stage >= 1 and st.session_state.stage != 3:
#    st.button('agregar', on_click=agregar_registro, args=[3])

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
