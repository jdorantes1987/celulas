import datetime

import pytz
import streamlit as st

from gestion_user.usuarios import ClsUsuarios
from helpers.navigation import make_sidebar
from scripts.Discipulados import Discipulados

st.set_page_config(
    page_title="Discipulados - Registro de sobres", layout="wide", page_icon=""
)

make_sidebar()

pytz.timezone("America/Caracas")
today = datetime.datetime.now(pytz.timezone("America/Caracas"))

st.header("Sobre discipulado")

for key, default in [
    ("stage4", 0),
]:
    if key not in st.session_state:
        st.session_state[key] = default


def set_state(i):
    st.session_state.stage4 = i


if st.session_state.stage4 == 0:
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

    df_discipuldos = st.session_state.discipulados.copy()
    df_discipuldos["buscador"] = (
        df_discipuldos["id_discipulado"]
        + " | "
        + df_discipuldos["cod_red"]
        + " | "
        + df_discipuldos["nombre"]
    )
id_discipulado = st.selectbox(
    "Lista de discipulados activos:",
    df_discipuldos["buscador"],
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
    st.session_state.id_registro_discipulado,
    id_liderazgo,
    id_discipulado,
    fecha.strftime("%Y-%m-%d"),
    fecha_recibido.strftime("%Y-%m-%d"),
    fecha_entregado.strftime("%Y-%m-%d"),
    expositor,
    tema,
    numero_asistentes,
    bs,
    usd,
    sobre_entregado,
    observ,
    user,
    fecha_insert,
]

if st.session_state.stage4 == 1:
    st.button("agregar", on_click=set_state, args=[3])

if st.session_state.stage4 == 3:
    oDiscipulados = Discipulados(manager_sheets=st.session_state.manager_sheets)
    if not oDiscipulados.existe_registro(
        data_historico=st.session_state.discipulados_historico,
        id_discipulado=id_discipulado,
        fecha=fecha.strftime("%Y-%m-%d"),
    ):
        oDiscipulados.add_actividad(registro)
        st.success(
            f"Registro {st.session_state.id_registro_discipulado} insertado exitosamente!"
        )
        set_state(4)
    else:
        st.error(
            f"El discipulado {id_discipulado} de fecha {fecha.strftime('%d-%m-%Y')}, ya se encuentra registrado."
        )
        set_state(1)

if st.session_state.stage4 == 4:
    if st.button("Nuevo registro"):
        # Actualizar los datos en la sesión
        st.session_state.discipulados_historico = (
            st.session_state.data.get_discipulados_historico_con_liderazgo()
        )
        st.session_state.id_registro_discipulado = str(
            st.session_state.discipulados_historico["id"].max() + 1
        )
        set_state(0)
        st.rerun()
