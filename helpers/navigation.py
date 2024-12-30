from time import sleep

import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages

import gestion_user.usuarios_roles as ur


def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("No se pudo obtener el contexto del script.")

    pages = get_pages("")
    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar():
    with st.sidebar:
        # Custom CSS for changing the sidebar color
        custom_css = """
        """
        # Apply custom CSS
        st.markdown(custom_css, unsafe_allow_html=True)
        st.markdown(
            "<h1 style='text-align: center; color: grey;'>Gestión de Casas de Bendición</h1>",
            unsafe_allow_html=True,
        )
        st.sidebar.markdown("---")
        st.write("")
        st.write("")

        if st.session_state.get("logged_in", False):
            _extracted_from_make_sidebar()
        elif get_current_page_name() != "inicio":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("app.py")


# TODO Rename this here and in `make_sidebar`
def _extracted_from_make_sidebar():
    st.page_link("pages/page1.py", label="Inicio", icon=None)
    # st.page_link("pages/page2.py", label="Datos liderazgo", icon=None)
    if ur.ClsUsuariosRoles.roles()["SOBRES-CELULAS"] == 1:
        st.page_link("pages/page3.py", label="Células - registro de sobre", icon=None)
    if ur.ClsUsuariosRoles.roles()["SOBRES-DISCIPULADOS"] == 1:
        st.page_link(
            "pages/page4.py", label="Discipulados - registro de sobre", icon=None
        )
    st.page_link("pages/page5.py", label="Estadísticas Generales", icon=None)

    if st.button("Cerrar sesión"):
        logout()


def logout():
    st.session_state.logged_in = False
    st.info("Se ha cerrado la sesión con éxito!")
    sleep(0.5)
    st.switch_page("app.py")
