import time

import streamlit as st

from helpers.navigation import make_sidebar
from scripts.htmlTemplates import css, footer, hide_st_style

st.set_page_config(page_title="Células: Inicio", layout="wide", page_icon="")
st.write(css, unsafe_allow_html=True)


def stream_data(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)


t1, t2 = st.columns((0.5, 5))
t1.image("images/logo.png")
t2.title("Aposento Alto para las Naciones")
make_sidebar()
st.markdown("---")

st.header("🏠 ¿Cómo registrar la información de las casas de bendición?")
texto = """
    Para registrar la información de las casas de bendición, sigue estos pasos:
    1. **Selecciona la pestaña "Células - registro de sobres"** en el menú lateral.
    2. **Completa los campos requeridos**:
        - **:blue[fecha célula]**: Selecciona la fecha de la célula.
        - **:blue[id célula]**: Ingresa el ID de la célula.
        - **:blue[tema]**: Selecciona el tema de la célula.
        - **:blue[asistentes]**: Ingresa el número de asistentes.
        - **:blue[monto en bolívares]**: Ingresa el monto recaudado en bolívares.
        - **:blue[monto en dólares]**: Ingresa el monto recaudado en dólares.
        - **:blue[estatus]**: Marca si la célula está activa o inactiva.
        - **:blue[expositor]**: Ingresa el nombre del expositor.
        - **:blue[observaciones]**: Agrega cualquier observación relevante.
    3. **Haz clic en "Agregar"** para registrar la información. ➕
    4. **Repite el proceso** para cada célula que desees registrar. 🔄
"""

st.write_stream(stream_data(texto))

# Footer
st.markdown(hide_st_style, unsafe_allow_html=True)
st.markdown(footer, unsafe_allow_html=True)
