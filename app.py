import streamlit as st
from time import sleep
from datetime import datetime
from gestion_user.control_usuarios import aut_user
from gestion_user.usuarios_roles import ClsUsuariosRoles


st.set_page_config(page_title='Células', 
                   layout="centered", 
                   initial_sidebar_state="collapsed", 
                   page_icon=':vs:')

MENU_INICIO = 'pages/page1.py'

def roles():
    return ClsUsuariosRoles.roles()

st.title("Datos del usuario")
st.write("Ingrese sus datos.")
username = st.text_input("usuario")
password = st.text_input("clave", type="password")

if st.button("Iniciar sesión", type="primary"):
    if is_valid := aut_user(username, password):
        date = datetime.now()
        st.cache_data.clear()
        print(f"{date} Usuario {username} ha iniciado sesión.")
        st.session_state.logged_in = True
        st.success("Sesión iniciada!")
        sleep(0.5)
        roles = roles()
        st.switch_page(MENU_INICIO)
    else:
        st.error("usuario o clave incorrecta")
        