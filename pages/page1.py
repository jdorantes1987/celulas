import streamlit as st

from helpers.navigation import make_sidebar
from scripts.htmlTemplates import css, hide_st_style, footer

st.set_page_config(page_title="Células: Inicio", layout="wide", page_icon="")
st.write(css, unsafe_allow_html=True)

t1, t2 = st.columns((0.5, 5))
t1.image("images/logo.png")
t2.title("Aposento Alto para las Naciones")
make_sidebar()
st.markdown("---")

st.header(
    "🏠 ¿Cómo registrar la información de las casas de bendición?"
)  # Added house emoji
st.markdown(
    """
    Para registrar la información de las casas de bendición, sigue estos pasos:
    1. **Selecciona la pestaña "Registro de sobres"** en el menú lateral.
    2. **Completa los campos requeridos**:
        - **id liderazgo_red**: Selecciona el ID del liderazgo de la red.
        - **nombre liderazgo_red**: Ingresa el nombre del liderazgo de la red.
        - **fecha célula**: Selecciona la fecha de la célula.
        - **tema**: Selecciona el tema de la célula.
        - **asistentes**: Ingresa el número de asistentes.
        - **estatus**: Marca si la célula está activa o inactiva.
        - **expositor**: Ingresa el nombre del expositor.
        - **observaciones**: Agrega cualquier observación relevante.
    3. **Haz clic en "Agregar"** para registrar la información. ➕
    4. **Repite el proceso** para cada célula que desees registrar. 🔄
""",
    unsafe_allow_html=True,
)

# Footer
st.markdown(hide_st_style, unsafe_allow_html=True)
st.markdown(footer, unsafe_allow_html=True)
