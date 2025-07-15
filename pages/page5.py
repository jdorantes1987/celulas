import datetime

import streamlit as st
from pandas import to_datetime

from helpers.navigation import make_sidebar
from scripts.data_manage import DataManageSingleton
from scripts.data_sheets import ManageSheets

st.set_page_config(page_title="Estadísticas Generales", layout="wide", page_icon="")

make_sidebar()

SPREADSHEET_ID = st.secrets.google_sheets.CELULAS_ID
FILE_NAME = st.secrets.google_sheets.FILE_NAME
CREDENTIALS_DICT = dict(st.secrets.google_service_account)

manager_sheets = ManageSheets(
    file_sheet_name=FILE_NAME,
    spreadsheet_id=SPREADSHEET_ID,
    credentials_file=CREDENTIALS_DICT,
)

today = datetime.datetime.now()

for key, default in [
    ("stage5", 0),
    ("data", DataManageSingleton.get_instance(manager_sheets)),
    ("celulas", None),
    ("discipulados", None),
    ("celulas_historico", None),
    ("discipulados_historico", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default


def set_state(i):
    st.session_state.stage5 = i


if st.session_state.stage5 == 0:
    # Inicializar el estado de la sesión

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
    set_state(1)


# Título principal
st.title("📊 Estadísticas Generales")

# Layout profesional con columnas
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏠 Células activas")
    df_celulas = st.session_state.celulas
    st.metric(
        label="Células activas",
        value=df_celulas.shape[0],
    )

with col2:
    st.subheader("🎯Discipulados activos")
    df_discipulados = st.session_state.discipulados
    st.metric(
        label="Discipulados activos",
        value=df_discipulados.shape[0],
    )

# Sección de detalles históricos (opcional)
with st.expander("🏠 Ver células activas"):
    celulas_activas = st.session_state.celulas.copy()
    # Ocultar algunas columnas
    celulas_activas = celulas_activas.drop(columns=["estatus_liderazgo", "id_cod"])
    campos = [
        "id_celula",
        "anfitriones",
        "direccion",
        "cod_red",
        "nombre",
        "cod_lider",
        "nombre_lider",
    ]
    st.dataframe(
        celulas_activas[campos],
        column_config={
            "id_celula": st.column_config.TextColumn("ID de la célula"),
            "anfitriones": st.column_config.TextColumn("Anfitriones"),
            "direccion": st.column_config.TextColumn("Dirección"),
            "cod_red": st.column_config.TextColumn("Código"),
            "nombre": st.column_config.TextColumn("Nombre"),
            "cod_lider": st.column_config.TextColumn("Código del lider"),
            "nombre_lider": st.column_config.TextColumn("Nombre del lider"),
        },
        use_container_width=False,
        hide_index=True,
    )

with st.expander("📆 Ver ultima actividad de células"):
    df = st.session_state.celulas_historico.copy()
    df = df[df["estatus_celula"] == 1]  # Filtrar solo células activas
    df["fecha"] = to_datetime(df["fecha"], yearfirst=True)
    # Agrupar y obtener la última fecha y días transcurridos
    resumen = (
        df.groupby(
            [
                "id_celula",
                "cod_red",
                "nombre",
            ]
        )["fecha"]
        .max()
        .reset_index()
    )
    resumen["dias_transc"] = (today - resumen["fecha"]).dt.days
    resumen["fecha"] = resumen["fecha"].dt.date
    st.dataframe(
        resumen,
        column_config={
            "id_celula": st.column_config.TextColumn("ID de la célula"),
            "cod_red": st.column_config.TextColumn("Código"),
            "nombre": st.column_config.TextColumn("Nombre"),
            "fecha": st.column_config.DateColumn("Última actividad"),
            "dias_transc": st.column_config.NumberColumn(
                "Dias", help="Cantidad de días transcurridos desde la última actividad"
            ),
        },
        use_container_width=False,
        hide_index=True,
    )

# Descargar histórico de células
celulas_historico_df = st.session_state.celulas_historico
st.download_button(
    label="📥 Descargar histórico de células",
    data=celulas_historico_df.to_csv(index=False).encode("utf-8"),
    file_name="historico_celulas.csv",
    mime="text/csv",
)

st.markdown("---")
with st.expander("🎯 Ver discipulados activos"):
    discipulados = st.session_state.discipulados.copy()
    st.dataframe(
        discipulados[["cod_red", "nombre", "cod_lider", "nombre_lider"]],
        use_container_width=False,
        hide_index=True,
    )

with st.expander("📆 Ver ultima actividad de discipulados"):
    df = st.session_state.discipulados_historico.copy()
    df = df[df["estatus_liderazgo"] == 1]  # Filtrar solo discipulados activos
    df["fecha"] = to_datetime(df["fecha"], yearfirst=True)
    # Agrupar y obtener la última fecha y días transcurridos
    resumen = df.groupby(["cod_red", "nombre"])["fecha"].max().reset_index()
    resumen["dias_transc"] = (today - resumen["fecha"]).dt.days
    resumen["fecha"] = resumen["fecha"].dt.date
    st.dataframe(
        resumen,
        column_config={
            "cod_red": st.column_config.TextColumn("Código"),
            "nombre": st.column_config.TextColumn("Nombre"),
            "fecha": st.column_config.DateColumn("Última actividad"),
            "dias_transc": st.column_config.NumberColumn(
                "Dias", help="Cantidad de días transcurridos desde la última actividad"
            ),
        },
        use_container_width=False,
        hide_index=True,
    )

# Descargar histórico de discipulados
discipulados_historico_df = st.session_state.discipulados_historico
st.download_button(
    label="📥 Descargar histórico de discipulados",
    data=discipulados_historico_df.to_csv(index=False).encode("utf-8"),
    file_name="historico_discipulados.csv",
    mime="text/csv",
)
