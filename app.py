import streamlit as st
from time import sleep
from datetime import datetime
from gestion_user.control_usuarios import aut_user
from gestion_user.usuarios_roles import ClsUsuariosRoles


st.set_page_config(
    page_title="Células",
    layout="centered",
    initial_sidebar_state="collapsed",
    page_icon=":vs:",
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
        st.success("Sesión iniciada exitosamente!")
        st.cache_data.clear()
        sleep(0.5)
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
    st.write(f"### Usuario ingresado: :red[{st.session_state.usuario}]")

    # Pedir la contraseña
    password = st.text_input("Ingresa tu contraseña:", type="password")
    if st.button("Log in", type="primary"):
        login(user=st.session_state.usuario, passw=password)

    if password:
        if not login(user=st.session_state.usuario, passw=password):
            st.error("usuario o clave incorrecta")
            sleep(1)
            st.rerun()
