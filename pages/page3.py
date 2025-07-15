import datetime

import streamlit as st

from gestion_user.usuarios import ClsUsuarios
from helpers.navigation import make_sidebar
from scripts.data_manage import DataManageSingleton
from scripts.data_sheets import ManageSheets
from scripts.celulas import Celulas

st.set_page_config(
    page_title="Células - Registro de sobres", layout="wide", page_icon=""
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

today = datetime.datetime.now()

for key, default in [
    ("stage3", 0),
    ("data", DataManageSingleton.get_instance(manager_sheets)),
    ("liderazgo_red", None),
    ("celulas_activas", None),
    ("temas", None),
    ("id_registro", 0),
]:
    if key not in st.session_state:
        st.session_state[key] = default

st.header("Datos del sobre")


def set_state(i):
    st.session_state.stage3 = i


if st.session_state.stage3 == 0:
    st.session_state.liderazgo_red = st.session_state.data.get_liderazgo_de_red()
    celulas = st.session_state.data.get_celulas_con_liderazgo()
    celulas = celulas[celulas["estatus_celula"] == 1]
    st.session_state.celulas_activas = celulas
    st.session_state.temas = st.session_state.data.get_temas_celulas()
    st.session_state.id_registro = str(
        st.session_state.data.get_celulas_historico_con_liderazgo()["id"].max() + 1
    )
    st.session_state.w_n_asist = 10
    set_state(2)

if st.session_state.stage3 == 1:
    # Inicializar el estado de la sesión
    st.session_state.w_exp = ""
    st.session_state.w_observ = ""
    st.session_state.w_n_asist = 10
    st.session_state.w_m_bs = 0
    st.session_state.w_m_usd = 0
    st.session_state.w_s_entr = False

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
    fecha_celula = st.date_input("fecha célula")
with col4:
    fecha_recibido = st.date_input("fecha recibido")
with col5:
    fecha_entregado = st.date_input("fecha entregado")

celulas = st.session_state.celulas_activas
celulas["buscador"] = (
    celulas["id_celula"]
    + " | "
    + celulas["cod_red"]
    + " | "
    + celulas["nombre"]
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
    temas = st.session_state.temas
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

numero_asistentes = str(st.slider("número de asistentes", 0, 100, key="w_n_asist"))
# Monto en bolívares y dólares con coma como separador decimal
bs = str(
    st.number_input(
        "ingrese el monto en bolívares (usar coma para decimales)", key="w_m_bs"
    )
)
bs = str(bs.replace(",", "").replace(".", ","))

usd = str(st.number_input("ingrese el monto en dólares.", key="w_m_usd"))
usd = str(usd.replace(",", "").replace(".", ","))

sobre_entregado = str(int(st.checkbox("sobre entregado?", key="w_s_entr")))

observ = st.text_input(
    label="observaciones",
    disabled=False,
    key="w_observ",
    placeholder="ingrese las observaciones",
    autocomplete="on",
)

user = ClsUsuarios.id_usuario()
fecha_insert = today.strftime("%Y-%m-%d %H:%M:%S")

registro = [
    st.session_state.id_registro,
    id_liderazgo,
    fecha_celula.strftime("%Y-%m-%d"),
    fecha_recibido.strftime("%Y-%m-%d"),
    fecha_entregado.strftime("%Y-%m-%d"),
    id_celula,
    expositor,
    tema_select,
    numero_asistentes,
    bs,
    usd,
    sobre_entregado,
    observ,
    user,
    fecha_insert,
]

if st.button("agregar"):
    Celulas(manager_sheets=manager_sheets).add_actividad(registro)
    set_state(3)

# if st.session_state.stage >= 1 and st.session_state.stage != 3:
#    st.button('agregar', on_click=agregar_registro, args=[3])

if st.session_state.stage3 >= 3:
    st.success(f"Registro {st.session_state.id_registro} insertado.")
    col1, col2 = st.columns([0.1, 0.1])
    with col1:
        col1.button("Continuar con otro registro?", on_click=set_state, args=[1])
    with col2:
        col2.button("ir a estadisticas", on_click=set_state, args=[4])

if st.session_state.stage3 == 4:
    del st.session_state.stage3
    st.switch_page("pages/page5.py")
