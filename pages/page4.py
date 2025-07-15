import streamlit as st

from helpers.navigation import make_sidebar
from scripts.data_manage import DataManageSingleton
from scripts.data_sheets import ManageSheets

st.set_page_config(
    page_title="Discipulados - Registro de sobres", layout="wide", page_icon=""
)

make_sidebar()


SPREADSHEET_ID = st.secrets.google_sheets.CELULAS_ID
FILE_NAME = st.secrets.google_sheets.FILE_NAME
CREDENTIALS_DICT = dict(st.secrets.google_service_account)
manager_sheets = ManageSheets(
    file_sheet_name=FILE_NAME,
    spreadsheet_id=SPREADSHEET_ID,
    credentials_file=CREDENTIALS_DICT,
)

st.header("Datos del sobre")

for key, default in [
    ("stage4", 0),
    ("discipulados", None),
    ("liderazgo_red", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default


def set_state(i):
    st.session_state.stage4 = i


if st.session_state.stage4 == 0:
    data = DataManageSingleton.get_instance(manager_sheets)
    liderazgo_red = data.get_liderazgo_de_red()
    liderazgo_red = liderazgo_red[liderazgo_red["estatus_liderazgo_red"] == 1]
    st.session_state.liderazgo_red = liderazgo_red
    discipulados = data.get_discipulados_con_liderazgo()
    discipulados = discipulados[discipulados["estatus_liderazgo"] == 1]
    st.session_state.discipulados = discipulados
    st.session_state.w_tema = ""
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
        label="id liderazgo_red",
        value=st.session_state.liderazgo_red.iloc[0, 1],
        disabled=True,
    )
with col2:
    nombre = st.text_input(
        label="nombre_liderazgo_red",
        value=st.session_state.liderazgo_red.iloc[0, 2],
        disabled=True,
    )

col3, col4, col5 = st.columns(3, gap="small")

with col3:
    fecha = st.date_input("fecha")
with col4:
    fecha_recibido = st.date_input("fecha recibido")
with col5:
    fecha_entregado = st.date_input("fecha entregado")

    st.session_state.discipulados["buscador"] = (
        st.session_state.discipulados["id_discipulado"]
        + " | "
        + st.session_state.discipulados["cod_red"]
        + " | "
        + st.session_state.discipulados["nombre"]
    )
id_discipulado = st.selectbox(
    "Lista de discipulados activos:",
    st.session_state.discipulados["buscador"],
    index=None,
    placeholder="seleccionar..",
)

id_discipulado = (
    str.strip(id_discipulado.split("|")[0]) if id_discipulado is not None else ""
)

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
    tema = st.text_input(
        label="tema",
        disabled=False,
        key="w_tema",
        placeholder="ingrese el tema expuesto",
        autocomplete="on",
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
        fecha,
        fecha_recibido,
        fecha_entregado,
        id_discipulado,
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
    data.insert_hist_celulas(registro)
    set_state(3)

# if st.session_state.stage4 >= 1 and st.session_state.stage4 != 3:
#    st.button('agregar', on_click=agregar_registro, args=[3])

if st.session_state.stage4 >= 3:
    st.info("Registro insertado.")
    col1, col2 = st.columns([0.1, 0.1])
    with col1:
        col1.button("Continuar con otro registro?", on_click=set_state, args=[0])
    with col2:
        col2.button("ir a estadisticas", on_click=set_state, args=[4])

if st.session_state.stage4 == 4:
    del st.session_state.stage4
    st.switch_page("pages/page5.py")
