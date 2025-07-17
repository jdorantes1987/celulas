from datetime import datetime
from time import sleep

import streamlit as st

from gestion_user.control_usuarios import aut_user
from gestion_user.usuarios_roles import ClsUsuariosRoles
from scripts.data_manage import DataManageSingleton
from scripts.data_sheets import ManageSheets

# Configuración de página con fondo personalizado
st.set_page_config(
    page_title="Células",
    layout="centered",
    initial_sidebar_state="expanded",
    page_icon="",
)

MENU_INICIO = "pages/page1.py"


def roles():
    return ClsUsuariosRoles.roles()


st.title("Inicio de sesión")


def set_stage(i):
    st.session_state.stage = i


if "stage" not in st.session_state:
    st.session_state.stage = 0


def login(user, passw):
    if aut_user(user=user, pw=passw):
        set_stage(0)
        date = datetime.now()
        print(f"{date} Usuario {user} ha iniciado sesión.")
        st.session_state.logged_in = True
        st.cache_data.clear()
        st.success("Sesión iniciada exitosamente!")
        with st.spinner("Preparando inicio de sesión..."):
            SPREADSHEET_ID = st.secrets.google_sheets.CELULAS_ID
            FILE_NAME = st.secrets.google_sheets.FILE_NAME
            CREDENTIALS_DICT = dict(st.secrets.google_service_account)

            st.session_state.manager_sheets = ManageSheets(
                file_sheet_name=FILE_NAME,
                spreadsheet_id=SPREADSHEET_ID,
                credentials_file=CREDENTIALS_DICT,
            )

            # Cargar data variables globales de sesión
            st.session_state.data = DataManageSingleton.get_instance(
                st.session_state.manager_sheets
            )
            st.session_state.liderazgo_red = (
                st.session_state.data.get_liderazgo_de_red()
            )

            st.session_state.celulas = st.session_state.data.get_celulas_con_liderazgo()
            # Filtrar las células activas
            st.session_state.celulas = st.session_state.celulas[
                st.session_state.celulas["estatus_celula"] == 1
            ]

            st.session_state.discipulados = (
                st.session_state.data.get_discipulados_con_liderazgo()
            )
            # Filtrar los discipulados activos
            st.session_state.discipulados = st.session_state.discipulados[
                st.session_state.discipulados["estatus_liderazgo"] == 1
            ]
            # Obtener los históricos de células y discipulados
            st.session_state.celulas_historico = (
                st.session_state.data.get_celulas_historico_con_liderazgo()
            )
            st.session_state.discipulados_historico = (
                st.session_state.data.get_discipulados_historico_con_liderazgo()
            )
            # Obtener los temas de las células
            st.session_state.temas = st.session_state.data.get_temas_celulas()

            st.session_state.liderazgo = st.session_state.data.get_liderazgo()

            # Obtener el nuevo id del registro de actividad en las células
            st.session_state.id_registro_celulas = str(
                st.session_state.celulas_historico["id"].max() + 1
            )
            # Obtener el nuevo id del registro de actividad en los discipulados
            st.session_state.id_registro_discipulado = str(
                st.session_state.discipulados_historico["id"].max() + 1
            )
            st.switch_page(MENU_INICIO)
        return True
    return False


if "usuario" not in st.session_state:
    st.write("Por favor ingrese su usuario.")
    # Si el usuario aún no ha sido ingresado
    usuario = st.text_input("Usuario:")
    if usuario and len(str.strip(usuario)) > 0:
        st.session_state.usuario = usuario
        st.rerun()
else:
    # Si el usuario ya ha sido ingresado, se oculta el input y se muestra el usuario ingresado
    st.write(f"### Usuario ingresado: *:orange[{st.session_state.usuario}]*")

    # Pedir la contraseña
    password = st.text_input("Ingresa tu contraseña:", type="password")
    if st.button("Log in", type="primary"):
        login(user=st.session_state.usuario, passw=password)

    if password:
        if not login(user=st.session_state.usuario, passw=password):
            st.error("usuario o clave incorrecta")
            sleep(1)
            st.rerun()
