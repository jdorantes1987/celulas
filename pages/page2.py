import datetime

import pytz
import streamlit as st
from pandas import to_datetime

from gestion_user.usuarios import ClsUsuarios
from helpers.navigation import make_sidebar
from scripts.temas import Temas

# icono negro streamlit set_page_config
st.set_page_config(page_title="Temas", layout="wide", page_icon="")

make_sidebar()

pytz.timezone("America/Caracas")
today = datetime.datetime.now(pytz.timezone("America/Caracas"))

for key, default in [
    ("stage6", 0),
    ("temas", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default


def set_state(i):
    st.session_state.stage6 = i


if st.session_state.stage6 == 0:
    # Inicializar el estado de la sesión
    st.session_state.oTemas = Temas(st.session_state.manager_sheets)
    st.session_state.temas.sort_values(by="fecha_ini", ascending=False, inplace=True)
    st.session_state.id_tema = ""
    st.session_state.txt_tema = ""
    st.session_state.fecha_inicio = today.date()
    st.session_state.fecha_fin = today.date()
    st.session_state.versiculo = ""
    set_state(1)


# Título principal
st.title("Temas de las Casas de Bendición")

# boton con icono
if st.button("🔄 Refrescar"):
    set_state(0)
    st.rerun()  # Recargar la página para mostrar los nuevos datos

# Layout profesional con columnas
col1, col2 = st.columns(2)
with col1:
    st.subheader("📊 Temas registrados")
    st.metric(
        label="Total de temas",
        value=st.session_state.temas.shape[0],
    )

with col2:
    st.subheader("📅 Último tema registrado")
    if st.session_state.temas.shape[0] > 0:
        last_tema = st.session_state.temas.iloc[0]
        # ajustar tamaño value
        st.metric(
            label=last_tema["id_tema"],
            value=last_tema["descrip"],
            delta=to_datetime(last_tema["fecha_ini"]).strftime("%Y-%m-%d"),
        )
    else:
        st.metric(label="No hay temas registrados", value="0")

st.subheader("📋 Lista de temas")
st.dataframe(
    st.session_state.temas.drop(columns=["co_us_in", "fe_us_in"], errors="ignore"),
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
    st.write("Completa los siguientes campos para agregar un nuevo tema:")
    # Convertir todo a mayúsculas
    id_tema = st.text_input(
        "ID del tema",
        key="id_tema",
        value=st.session_state.get("id_tema", "").upper(),
        placeholder="Ej. 'TM20250701' para el 1er tema del mes",
    )
    tema = st.text_input(
        "Tema",
        key="txt_tema",
        value=st.session_state.get("txt_tema", "").upper(),
        placeholder="Ej. LA IMPORTANCIA DE LA ORACIÓN",
    )
    fecha_inicio = st.date_input("Fecha de inicio", key="fecha_inicio")
    fecha_fin = st.date_input("Fecha de fin", key="fecha_fin")
    versiculo = st.text_input("Versículo", key="versiculo", placeholder="Ej. Pv 4:23")
    submit_button = st.form_submit_button("Agregar tema")
    user = ClsUsuarios.id_usuario()
    fecha_insert = today.strftime("%Y-%m-%d %H:%M:%S")
    if submit_button:
        # Validar que todos los campos estén completos
        if not id_tema or not tema or not versiculo:
            st.error("Por favor, completa todos los campos.")
        else:
            try:
                tema_upper = tema.upper()
                response = st.session_state.oTemas.add_tema(
                    [
                        id_tema,
                        tema_upper,
                        fecha_inicio.strftime("%Y-%m-%d"),
                        fecha_fin.strftime("%Y-%m-%d"),
                        versiculo,
                        user,
                        fecha_insert,
                    ]
                )

                if response["success"]:
                    st.success(f"Tema '{id_tema}' agregado exitosamente.")
                    st.session_state.temas = st.session_state.data.get_temas_celulas()
                    set_state(0)
                    st.rerun()  # Recargar la página para mostrar el nuevo tema
                else:
                    st.error(response["message"])
            except Exception as e:
                st.error(f"Error al agregar el tema: {e}")
                st.error(response["message"])
            except Exception as e:
                st.error(f"Error al agregar el tema: {e}")
