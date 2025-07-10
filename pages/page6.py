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


if "stage6" not in st.session_state:
    st.session_state.stage6 = 0


def set_state(i):
    st.session_state.stage6 = i


if st.session_state.stage6 == 0:
    # Inicializar el estado de la sesión
    st.session_state.id_tema = ""
    st.session_state.tema = ""
    st.session_state.fecha_inicio = today.date()
    st.session_state.fecha_fin = today.date()
    st.session_state.versiculo = ""
    set_state(1)


# Título principal
st.title("Temas de las Casas de Bendición")

df = get_temas()

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

df.sort_values(by="fecha_ini", ascending=False, inplace=True)

st.subheader("📋 Lista de temas")
st.dataframe(
    df,
    column_config={
        "id_tema": st.column_config.TextColumn("ID del tema"),
        "descrip": st.column_config.TextColumn("Descripción"),
        "fecha_ini": st.column_config.DateColumn("Fecha de inicio"),
        "fecha_fin": st.column_config.DateColumn("Fecha de fin"),
        "versiculo": st.column_config.TextColumn("Versículo"),
    },
    use_container_width=True,
    hide_index=True,
)

st.subheader("📌 Agregar un nuevo tema")
# Formulario para agregar un nuevo tema
with st.form("agregar_tema"):
    id_tema = st.text_input(
        "ID del tema",
        key="id_tema",
        placeholder="Ej. 'TM20250701' para el 1er tema del mes",
    )
    id_tema = id_tema.upper()  # Asegurarse de que el ID esté en mayúsculas
    st.session_state.id_tema = id_tema
    tema = st.text_input(
        "Tema", key="tema", placeholder="Ej. LA IMPORTANCIA DE LA ORACIÓN"
    )
    tema = tema.upper()  # Asegurarse de que el tema esté en mayúsculas
    st.session_state.tema = tema
    fecha_inicio = st.date_input("Fecha de inicio", key="fecha_inicio")
    fecha_fin = st.date_input("Fecha de fin", key="fecha_fin")
    versiculo = st.text_input("Versículo", key="versiculo", placeholder="Ej. Pv 4:23")
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
                set_state(0)
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
