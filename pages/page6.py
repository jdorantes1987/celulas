import datetime

import streamlit as st
from pandas import to_datetime

from helpers.navigation import make_sidebar
from scripts.temas import Temas
from scripts.data_sheets import ManagerSheets

st.set_page_config(page_title="Temas", layout="wide", page_icon="⚡")

make_sidebar()

SPREADSHEET_ID = st.secrets.google_sheets.CELULAS_ID
FILE_NAME = st.secrets.google_sheets.FILE_NAME
SHEET_NAME = st.secrets.google_sheets.SHEET_HIST_CELULAS
CREDENTIALS_DICT = dict(st.secrets.google_service_account)

oManagerSheets = ManagerSheets(
    file_sheet_name=FILE_NAME,
    spreadsheet_id=SPREADSHEET_ID,
    credentials_file=CREDENTIALS_DICT,
)
oTemas = Temas(manager_sheets=oManagerSheets)
today = datetime.datetime.now()


@st.cache_data
def get_temas():
    return oTemas.get_temas()


# Título principal
st.title("Temas de las Casas de Bendición")

df = get_temas()
st.dataframe(df, use_container_width=True, hide_index=True)


# Layout profesional con columnas
col1, col2 = st.columns(2)
with col1:
    st.subheader("📊 Temas registrados")
    st.metric(
        label="Total de temas",
        value=df.shape[0],
    )

with col2:
    st.subheader("📅 Último tema registrado")
    if df.shape[0] > 0:
        last_tema = df.iloc[-1]
        st.metric(
            label=last_tema["id_tema"],
            value=last_tema["descrip"],
            delta=to_datetime(last_tema["fecha_ini"]).strftime("%Y-%m-%d"),
        )
    else:
        st.metric(label="No hay temas registrados", value="0")

# Formulario para agregar un nuevo tema
st.subheader("Agregar nuevo tema")
with st.form("agregar_tema"):
    id_tema = st.text_input("ID del tema")
    tema = st.text_input("Tema")
    fecha_inicio = st.date_input("Fecha de inicio")
    fecha_fin = st.date_input("Fecha de fin")
    versiculo = st.text_input("Versículo")
    submit_button = st.form_submit_button("Agregar tema")
if submit_button:
    try:
        response = oTemas.add_tema(
            [
                id_tema,
                tema,
                fecha_inicio.strftime("%Y-%m-%d"),
                fecha_fin.strftime("%Y-%m-%d"),
                versiculo,
            ]
        )
        print(response)  # Para depuración
        if response["success"]:
            st.success(f"Tema '{tema}' agregado exitosamente.")
            st.rerun()  # Recargar la página para mostrar el nuevo tema
        else:
            st.error(response["message"])
    except Exception as e:
        st.error(f"Error al agregar el tema: {e}")

# Footer
st.markdown(
    """
---
*Desarrollado por [Jackson Dorantes](dorantes.jackson@gmail.com)*
"""
)

# Hide the footer
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
