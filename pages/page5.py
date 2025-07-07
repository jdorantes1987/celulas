import datetime

import streamlit as st
from pandas import to_datetime

from helpers.navigation import make_sidebar
from scripts.oCelulas import DataCelulas
from scripts.oDiscipulados import DataDiscipulados
from scripts.data_sheets import ManagerSheets

st.set_page_config(page_title="Estadísticas Generales", layout="wide", page_icon="⚡")

make_sidebar()
oCelulas = DataCelulas()
oDicipulados = DataDiscipulados()
today = datetime.datetime.now()


@st.cache_data
def celulas_activas():
    return oCelulas.celulas_activas()


@st.cache_data
def celuas_historico():
    return oCelulas.celuas_historico()


@st.cache_data
def celulas_activas_historico():
    data = oCelulas.celuas_historico()
    return data[data["estatus_celula"] == 1]


@st.cache_data
def get_dicipulados():
    return oDicipulados.get_discipulados()


@st.cache_data
def get_dicipulados_activos():
    data = oDicipulados.get_discipulados()
    return data[data["estatus_liderazgo"] == 1]


# Título principal
st.title("Estadísticas Generales")

# Layout profesional con columnas
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏠 Células activas")
    celulas_activas_df = celulas_activas()
    st.metric(
        label="Células activas",
        value=celulas_activas_df.shape[0],
    )

with col2:
    st.subheader("🎯Discipulados activos")
    dicipulados_activos_df = get_dicipulados_activos()
    st.metric(
        label="Discipulados activos",
        value=dicipulados_activos_df.shape[0],
    )

# Sección de detalles históricos (opcional)
with st.expander("🏠 Ver células activas"):
    historico = celulas_activas().copy()
    # Ocultar algunas columnas
    historico = historico.drop(
        columns=["id_cod", "estatus_celula", "id_liderazgo", "estatus_liderazgo"]
    )
    st.dataframe(historico, use_container_width=True, hide_index=True)

with st.expander("📆 Ver ultima actividad de células"):
    celula_con_activ = celulas_activas_historico().copy()
    celula_con_activ["fecha"] = to_datetime(celula_con_activ["fecha"], yearfirst=True)
    grouped = celula_con_activ.groupby(
        ["cod_red", "anfitriones", "c_lider", "direccion"]
    )
    last_day_of_month = grouped["fecha"].max().reset_index()
    last_day_of_month["dias_transc"] = (
        today - last_day_of_month["fecha"]
    ).dt.days  # Dias transcurridos entre la ultima fecha al dia de hoy
    last_day_of_month["fecha"] = last_day_of_month["fecha"].dt.date
    grouped2 = last_day_of_month.groupby(
        ["cod_red", "anfitriones", "c_lider", "direccion"]
    )[["fecha", "dias_transc"]].max()
    st.dataframe(grouped2.reset_index(), use_container_width=True, hide_index=True)

with st.expander("📊 Ver historico de celulas"):
    columnas_historico_celulas = [
        "id_celula",
        "fecha",
        "fecha_recibido",
        "fecha_entregado",
        "id_tema",
        "descrip",
        "cod_red",
        "c_lider",
        "anfitriones",
        "expositor",
        "direccion",
        "asistentes",
        "monto_bs",
        "monto_usd",
        "sobre_entregado",
        "estatus_celula",
        "estatus_liderazgo",
    ]
    hist_celulas = celuas_historico().copy()

    # Eliminar columnas innecesarias
    hist_celulas = hist_celulas.drop(columns=["id", "id_cod", "id_liderazgo"], axis=1)

    # Formatear columnas de montos
    hist_celulas["monto_bs"] = hist_celulas["monto_bs"].map(lambda x: f"{x:,.2f}")
    hist_celulas["monto_usd"] = hist_celulas["monto_usd"].map(lambda x: f"{x:,.2f}")
    hist_celulas = hist_celulas[columnas_historico_celulas]
    st.dataframe(
        hist_celulas,
        column_config={
            "fecha": st.column_config.DateColumn(
                "Fecha de la célula", format="DD/MM/YYYY"
            ),
            "fecha_recibido": st.column_config.DateColumn(
                "Fecha recibido", format="DD/MM/YYYY"
            ),
            "fecha_entregado": st.column_config.DateColumn(
                "Fecha entregado", format="DD/MM/YYYY"
            ),
            "descrip": st.column_config.TextColumn("Tema"),
            "cod_red": st.column_config.TextColumn("Código de red"),
            "c_lider": st.column_config.TextColumn("Líder"),
            "anfitriones": st.column_config.TextColumn("Anfitriones"),
            "expositor": st.column_config.TextColumn("Expositor"),
            "direccion": st.column_config.TextColumn("Dirección"),
            "asistentes": st.column_config.NumberColumn("Asistentes"),
            "monto_bs": st.column_config.NumberColumn("Monto Bs", format="%s"),
            "monto_usd": st.column_config.NumberColumn("Monto USD", format="$%s"),
            "sobre_entregado": st.column_config.CheckboxColumn("Sobre entregado?"),
            "estatus_celula": st.column_config.CheckboxColumn("Estatus Célula"),
            "estatus_liderazgo": st.column_config.CheckboxColumn("Estatus Liderazgo"),
        },
        use_container_width=True,
        hide_index=True,
    )

st.markdown("---")
with st.expander("🎯 Ver discipulados activos"):
    discipulados = get_dicipulados_activos().copy()
    # Ocultar algunas columnas
    discipulados = discipulados.drop(
        columns=[
            "id_discipulado",
            "id_cod",
            "cod_base",
            "c_lider_red",
            "id_liderazgo",
            "estatus_liderazgo",
            "nombre_lider",
        ]
    )
    st.dataframe(discipulados, use_container_width=True, hide_index=True)


with st.expander("Ver datos sheet"):
    import os

    # import toml

    # # Construir la ruta absoluta al archivo de configuración
    # config_path = os.path.abspath(
    #     os.path.join(os.path.dirname(__file__), "..", ".streamlit", "config.toml")
    # )
    # config = toml.load(config_path)

    # Acceso seguro a las claves
    # if "google_sheets" not in config:
    #     st.error(
    #         "No se encontró la sección [google_sheets] en el archivo de configuración."
    #     )
    # else:
    SPREADSHEET_ID = st.secrets.google_sheets.CELULAS_ID
    FILE_CELULAS_NAME = st.secrets.google_sheets.FILE_CELULAS_NAME
    SHEET_NAME = st.secrets.google_sheets.SHEET_CELULAS
    CREDENTIALS_DICT = dict(st.secrets.google_service_account)

    oTemas = ManagerSheets(
        file_sheet_name=FILE_CELULAS_NAME,
        spreadsheet_id=SPREADSHEET_ID,
        credentials_file=CREDENTIALS_DICT,
    )
    df = oTemas.get_data_hoja(sheet_name=SHEET_NAME)
    st.dataframe(df, use_container_width=True, hide_index=True)
