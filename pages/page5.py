import datetime

import streamlit as st
from pandas import to_datetime

from helpers.navigation import make_sidebar

st.set_page_config(page_title="Estadísticas Generales", layout="wide", page_icon="")

make_sidebar()

today = datetime.datetime.now()

for key, default in [
    ("stage5", 0),
]:
    if key not in st.session_state:
        st.session_state[key] = default


def set_state(i):
    st.session_state.stage5 = i


if st.session_state.stage5 == 0:
    # Inicializar el estado de la sesión
    set_state(1)

# Título principal
st.title("📊 Estadísticas Generales")

# Layout profesional con columnas
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏠 Células")
    df_celulas = st.session_state.celulas
    st.metric(
        label="Activas",
        value=df_celulas.shape[0],
    )

with col2:
    st.subheader("🎯Discipulados")
    df_discipulados = st.session_state.discipulados
    st.metric(
        label="Activos",
        value=df_discipulados.shape[0],
    )

col3, col4 = st.columns(2)
with col3:
    df_celulas_historico = st.session_state.celulas_historico.copy()
    df_celulas_historico = df_celulas_historico[
        df_celulas_historico["sobre_entregado"] == 0
    ]
    df_discipulados_historico = st.session_state.discipulados_historico.copy()
    df_discipulados_historico = df_discipulados_historico[
        df_discipulados_historico["sobre_entregado"] == 0
    ]
    total_bs = (
        df_celulas_historico["monto_bs"].sum()
        + df_discipulados_historico["monto_bs"].sum()
    )
    st.metric(
        label="💶 Sobres por entregar",
        value=f"Bs. {total_bs:,.2f}",
    )

    total_usd = (
        df_celulas_historico["monto_usd"].sum()
        + df_discipulados_historico["monto_usd"].sum()
    )

with col4:
    st.metric(
        label="💵 Sobres por entregar",
        value=f"$. {total_usd:,.2f}",
    )

with st.expander("🧑‍🏫 Ver liderazgo activo"):
    liderazgo = st.session_state.liderazgo.copy()
    liderazgo = liderazgo[liderazgo["estatus"] == 1]  # Filtrar solo liderazgo activo
    liderazgo.sort_values(by=["cod_base_lider", "cod_red"], inplace=True)

    st.subheader("Liderazgo activo")
    # Metrica cantidad de líderes
    total_lideres = liderazgo.shape[0]
    st.metric(label="Total líderes", value=total_lideres, width="content")

    # Agrupar por código de base y contar los líderes
    st.subheader("Bases de liderazgo")
    base_counts = liderazgo.groupby("cod_base_lider").size().reset_index(name="count")
    base_counts.sort_values(by="count", ascending=False, inplace=True)
    st.dataframe(
        base_counts,
        column_config={
            "cod_base_lider": st.column_config.TextColumn("Código de base"),
            "count": st.column_config.NumberColumn("Cantidad de códigos"),
        },
        use_container_width=False,
        hide_index=True,
    )

    st.subheader("Liderazgo por red")
    st.dataframe(
        liderazgo[
            [
                "cod_red",
                "nombre",
                "cod_lider",
                "nombre_lider",
            ]
        ],
        column_config={
            "cod_red": st.column_config.TextColumn("Código"),
            "nombre": st.column_config.TextColumn("Nombre"),
            "cod_lider": st.column_config.TextColumn("Código del líder"),
            "nombre_lider": st.column_config.TextColumn("Nombre del líder"),
        },
        use_container_width=False,
        hide_index=True,
    )

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

with st.expander("⚠️ Ver últimas 10 células suspendidas"):
    campos_celulas_suspendidas = [
        "id_celula",
        "observ",
        "fecha",
        "fecha_recibido",
        "anfitriones",
        "cod_red",
        "nombre",
        "cod_lider",
        "nombre_lider",
    ]
    df_celulas_suspendidas = st.session_state.celulas_historico.copy()
    df_celulas_suspendidas = df_celulas_suspendidas[
        df_celulas_suspendidas["asistentes"] == 0
    ]  # Filtrar solo células suspendidas
    df_celulas_suspendidas = df_celulas_suspendidas[campos_celulas_suspendidas].tail(10)
    df_celulas_suspendidas.sort_values(by="fecha", ascending=True, inplace=True)
    st.dataframe(
        df_celulas_suspendidas,
        column_config={
            "id_celula": st.column_config.TextColumn("ID de la célula"),
            "observ": st.column_config.TextColumn("Observaciones"),
            "fecha": st.column_config.DateColumn("Fecha"),
            "fecha_recibido": st.column_config.DateColumn("Fecha recibido"),
            "anfitriones": st.column_config.TextColumn("Anfitriones"),
            "cod_red": st.column_config.TextColumn("Código"),
            "nombre": st.column_config.TextColumn("Nombre"),
            "cod_lider": st.column_config.TextColumn("Código del lider"),
            "nombre_lider": st.column_config.TextColumn("Nombre del lider"),
        },
        use_container_width=False,
        hide_index=True,
    )

with st.expander("⚠️ Códigos sin células"):
    liderazgo = st.session_state.liderazgo.copy()[
        [
            "id_cod",
            "cod_red",
            "nombre",
            "cod_lider",
            "nombre_lider",
            "cod_base_lider",
            "estatus",
        ]
    ]
    liderazgo = liderazgo[liderazgo["estatus"] == 1]  # Filtrar solo liderazgo activo
    celulas_activas = st.session_state.celulas.copy()
    celulas_activas = (
        celulas_activas.groupby(
            [
                "id_cod",
                "cod_red",
                "nombre",
                "cod_lider",
                "nombre_lider",
                "cod_base_lider",
            ]
        )
        .agg({"estatus_celula": "count"})
        .reset_index()
    )
    # Unir los datos de liderazgo con las células activas
    df_join = liderazgo.merge(
        celulas_activas,
        left_on="id_cod",
        right_on="id_cod",
        how="left",
    )
    # Filtrar los códigos que no tienen células asociadas
    df_join = df_join[df_join["estatus_celula"].isna()]
    df_join = df_join[
        [
            "cod_red_x",
            "nombre_x",
            "cod_lider_x",
            "nombre_lider_x",
            "cod_base_lider_x",
        ]
    ]

    # Metrica de códigos sin células
    l_activo = st.session_state.liderazgo.copy()
    l_activo = l_activo[l_activo["estatus"] == 1]
    st.metric(
        label="Cantidad",
        value=df_join.shape[0],
        delta=abs(df_join.shape[0] - l_activo.shape[0]),
        help="Cantidad de códigos que no tienen células activas versus los activos. El número más pequeño indica la cantidad de códigos base con células activas.",
    )

    df_join.sort_values(by=["cod_base_lider_x", "cod_red_x"], inplace=True)
    st.dataframe(
        df_join,
        column_config={
            "cod_red_x": st.column_config.TextColumn("Código"),
            "nombre_x": st.column_config.TextColumn("Nombre"),
            "cod_lider_x": st.column_config.TextColumn("Código del líder"),
            "nombre_lider_x": st.column_config.TextColumn("Nombre del líder"),
            "cod_base_lider_x": st.column_config.TextColumn("Código del base líder"),
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
