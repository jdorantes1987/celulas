import datetime

import pytz
import streamlit as st

from gestion_user.usuarios import ClsUsuarios
from helpers.navigation import make_sidebar
from scripts.Celulas import Celulas

st.set_page_config(
    page_title="Células - Registro de sobres", layout="wide", page_icon=""
)
make_sidebar()
# Configurar datetime con zona horaria de Venezuela
# Esto es necesario para que las fechas se manejen correctamente en la zona horaria local

pytz.timezone("America/Caracas")
today = datetime.datetime.now(pytz.timezone("America/Caracas"))

for key, default in [
    ("stage3", 0),
]:
    if key not in st.session_state:
        st.session_state[key] = default

st.header("Sobre célula")


def set_state(i):
    st.session_state.stage3 = i


if st.session_state.stage3 == 0:
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
    st.session_state.w_fecha = today
    st.session_state.w_fecha_e = today
    st.session_state.w_fecha_r = today

    set_state(2)

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
    fecha_celula = st.date_input("fecha célula", key="w_fecha", value=today)
with col4:
    fecha_recibido = st.date_input("fecha recibido", key="w_fecha_r", value=today)
with col5:
    fecha_entregado = st.date_input("fecha entregado", key="w_fecha_e", value=today)

celulas = st.session_state.celulas.copy()
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
    temas = st.session_state.temas.copy()
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
    st.session_state.id_registro_celulas,
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

if st.session_state.stage3 == 2:
    st.button("agregar", on_click=set_state, args=[3])


if st.session_state.stage3 == 3:
    st.info(f"Insertando registro {st.session_state.id_registro_celulas}...")
    Celulas(manager_sheets=st.session_state.manager_sheets).add_actividad(registro)
    st.success(
        f"Registro {st.session_state.id_registro_celulas} insertado exitosamente!"
    )
    # Actualizar los datos en la sesión
    st.session_state.celulas_historico = (
        st.session_state.data.get_celulas_historico_con_liderazgo()
    )
    st.session_state.id_registro_celulas = str(
        st.session_state.celulas_historico["id"].max() + 1
    )
    set_state(4)


if st.session_state.stage3 == 4:
    if st.button("Nuevo registro"):
        set_state(1)
