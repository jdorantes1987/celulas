from pandas import DataFrame, to_datetime, to_numeric

from scripts.Celulas import Celulas
from scripts.Discipulados import Discipulados
from scripts.Liderazgo import Liderazgo
from scripts.temas import Temas


class DataManageSingleton:
    _instance = None

    @classmethod
    def get_instance(cls, manager_sheets):
        if cls._instance is None:
            cls._instance = DataManage(manager_sheets)
        return cls._instance


class DataManage:
    """
    Clase para manejar la gestión de datos de las hojas de cálculo.
    """

    def __init__(self, manager_sheets) -> None:
        self.oSheets = manager_sheets
        self.oCelulas = Celulas(manager_sheets=self.oSheets)
        self.oLiderazgo = Liderazgo(manager_sheets=self.oSheets)
        self.oDiscipulados = Discipulados(manager_sheets=self.oSheets)
        self.oTemas = Temas(manager_sheets=self.oSheets)

    def get_liderazgo_de_red(self) -> DataFrame:
        """
        Obtiene los datos de liderazgo de red.
        """
        df_liderazgo = self.oLiderazgo.get_liderazgo_de_red()
        df_liderazgo["estatus"] = df_liderazgo["estatus"].astype(int)
        df_liderazgo.rename(
            columns={
                "id_liderazgo": "id_liderazgo_red",
                "cod_red": "cod_base",
                "nombre_liderazgo": "nombre_liderazgo_red",
                "estatus": "estatus_liderazgo_red",
            },
            inplace=True,
        )
        return df_liderazgo

    def get_liderazgo(self) -> DataFrame:
        """
        Obtiene los datos de liderazgo.
        """
        return self.oLiderazgo.get_codigos_con_liderazgo()

    def get_temas_celulas(self) -> DataFrame:
        """
        Obtiene los temas de las celdas.
        """
        df_temas = self.oTemas.get_temas()
        df_temas.sort_values(by="fecha_ini", ascending=False, inplace=True)
        return df_temas

    def get_celulas_con_liderazgo(self):
        """
        Obtiene las celdas con su respectivo liderazgo.
        """

        df_celulas = self.oCelulas.get_celulas()
        df_liderazgo = self.oLiderazgo.get_codigos_con_liderazgo()

        df_join = df_celulas.merge(
            df_liderazgo,
            left_on="id_cod",
            right_on="id_cod",
            how="left",
        )
        df_join.drop(
            columns=["id_liderazgo_y"],
            inplace=True,
        )
        df_join.rename(
            columns={
                "id_liderazgo_x": "id_liderazgo",
                "estatus_x": "estatus_celula",
                "estatus_y": "estatus_liderazgo",
            },
            inplace=True,
        )
        df_join["estatus_celula"] = df_join["estatus_celula"].astype(int)
        df_join["estatus_liderazgo"] = df_join["estatus_liderazgo"].astype(int)
        return df_join[
            [
                "id_liderazgo",
                "id_celula",
                "anfitriones",
                "cod_red",
                "id_cod",
                "nombre",
                "cod_lider",
                "nombre_lider",
                "direccion",
                "estatus_celula",
                "estatus_liderazgo",
            ]
        ]

    def get_celulas_historico_con_liderazgo(self) -> DataFrame:
        """
        Obtiene las celulas históricas con su respectivo liderazgo.
        """
        celulas_con_liderazgo = self.get_celulas_con_liderazgo()
        df_celulas_hist = self.oCelulas.get_celulas_historico()
        df_join = df_celulas_hist.merge(
            celulas_con_liderazgo,
            left_on="id_celula",
            right_on="id_celula",
            how="left",
        )
        df_join.drop(columns=["id_liderazgo_y"], inplace=True)
        df_join["id"] = df_join["id"].astype(int)
        df_join["asistentes"] = df_join["asistentes"].astype(int)
        df_join["sobre_entregado"] = df_join["sobre_entregado"].astype(int)
        df_join.rename(
            columns={"id_liderazgo_x": "id_liderazgo"},
            inplace=True,
        )

        cols_montos = [
            "monto_bs",
            "monto_usd",
        ]
        # Convertir campos object a fechas de forma robusta
        for col in ["fecha", "fecha_recibido", "fecha_entregado"]:
            df_join[col] = to_datetime(df_join[col], errors="coerce")

        # Eliminar separadores de miles y reemplazar coma decimal por punto si las columnas son de tipo string
        for col in cols_montos:
            if df_join[col].dtype == "object":
                df_join[col] = (
                    df_join[col]
                    .str.replace(".", "", regex=False)  # Remove thousand separator
                    .str.replace(
                        ",", ".", regex=False
                    )  # Replace decimal comma with dot
                )
        try:
            # Convertir a float, forzando errores a NaN
            df_join[cols_montos] = df_join[cols_montos].apply(
                to_numeric, errors="raise"  # Convertir a float errores a NaN
            )
        except Exception as e:
            print(f"Error en obtener_facturas_validadas: {e}")

        return df_join[
            [
                "id",
                "id_liderazgo",
                "id_celula",
                "id_tema",
                "fecha",
                "fecha_recibido",
                "fecha_entregado",
                "anfitriones",
                "cod_red",
                "id_cod",
                "nombre",
                "cod_lider",
                "nombre_lider",
                "expositor",
                "direccion",
                "asistentes",
                "monto_bs",
                "monto_usd",
                "sobre_entregado",
                "estatus_celula",
                "estatus_liderazgo",
            ]
        ]

    def get_discipulados_con_liderazgo(self) -> DataFrame:
        """
        Obtiene los discipulados con su respectivo liderazgo.
        """
        df_discipulados = self.oDiscipulados.get_discipulados()
        df_liderazgo = self.oLiderazgo.get_codigos_con_liderazgo()

        df_join = df_discipulados.merge(
            df_liderazgo,
            left_on="id_cod",
            right_on="id_cod",
            how="left",
        )
        df_join.drop(
            columns=["id_liderazgo_y"],
            inplace=True,
        )
        df_join.rename(
            columns={
                "id_liderazgo_x": "id_liderazgo",
                "estatus": "estatus_liderazgo",
            },
            inplace=True,
        )
        df_join["estatus_liderazgo"] = df_join["estatus_liderazgo"].astype(int)
        return df_join

    def get_discipulados_historico_con_liderazgo(self) -> DataFrame:
        """
        Obtiene los discipulados históricos con su respectivo liderazgo.
        """
        df_discipulados_hist = self.oDiscipulados.get_discipulados_historico()
        df_discipulados_con_liderazgo = self.get_discipulados_con_liderazgo()

        df_join = df_discipulados_hist.merge(
            df_discipulados_con_liderazgo,
            left_on="id_discipulado",
            right_on="id_discipulado",
            how="left",
        )
        df_join.drop(
            columns=["id_liderazgo_y", "id_y"],
            inplace=True,
        )
        df_join.rename(
            columns={
                "id_liderazgo_x": "id_liderazgo",
                "id_x": "id_discipulado",
            },
            inplace=True,
        )

        df_join["asistentes"] = df_join["asistentes"].astype(int)
        df_join["estatus_liderazgo"] = df_join["estatus_liderazgo"].astype(int)

        cols_montos = [
            "monto_bs",
            "monto_usd",
        ]
        # Convertir campos object a fechas de forma robusta
        for col in ["fecha", "fecha_recibido", "fecha_entregado"]:
            df_join[col] = to_datetime(df_join[col], errors="coerce")

        # Eliminar separadores de miles y reemplazar coma decimal por punto si las columnas son de tipo string
        for col in cols_montos:
            if df_join[col].dtype == "object":
                df_join[col] = (
                    df_join[col]
                    .str.replace(".", "", regex=False)  # Remove thousand separator
                    .str.replace(
                        ",", ".", regex=False
                    )  # Replace decimal comma with dot
                )
        try:
            # Convertir a float, forzando errores a NaN
            df_join[cols_montos] = df_join[cols_montos].apply(
                to_numeric, errors="raise"  # Convertir a float errores a NaN
            )
        except Exception as e:
            print(f"Error en obtener_facturas_validadas: {e}")
        return df_join[
            [
                "id_discipulado",
                "id_liderazgo",
                "fecha",
                "fecha_recibido",
                "fecha_entregado",
                "expositor",
                "tema",
                "asistentes",
                "monto_bs",
                "monto_usd",
                "observ",
                "sobre_entregado",
                "id_cod",
                "cod_red",
                "nombre",
                "cod_lider",
                "nombre_lider",
                "cod_base_lider",
                "estatus_liderazgo",
            ]
        ]
