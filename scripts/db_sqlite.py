from sqlite3 import IntegrityError

from pandas import read_sql

from scripts.interfaz_data_source import IDataSource


class BD_SQLite_Celulas(IDataSource):
    def __init__(self, conexion) -> None:
        self.conexion = conexion
        self.cur = conexion.cursor()

    def get_celulas_activas(self):
        sql = """
                SELECT id_celula, cod_red, c_lider, c_lider_red, nombre_lider,
                       cod_base, anfitriones, direccion
                FROM V_CELULAS_ACTIVAS
            """
        return read_sql(sql, self.conexion)

    def get_celulas_activas_hist(self):
        return read_sql("SELECT * FROM V_HIST_CELULAS_ACTIVAS", self.conexion)

    def get_liderazgo(self):
        return read_sql("SELECT * FROM liderazgo", self.conexion)

    def get_liderazgo_redes(self):
        return read_sql(
            """
                        SELECT *
                        FROM V_LIDERAZGO_X_COD_RED_ACTIVO
                        """,
            self.conexion,
        )

    def get_temas(self):
        return read_sql(
            """SELECT *
                        FROM temas ORDER BY id_tema DESC
                        """,
            self.conexion,
        )

    def insert_hist_celulas(self, data):
        try:
            self.cur.executemany(
                """INSERT INTO hist_celulas
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                data,
            )
            print("Registro insertado.")
            self.conexion.commit()
            self.cur.close()
        except IntegrityError:
            print(
                "Error al insertar los datos.",
            )

    def insert_hist_discipulados(self, data):
        try:
            self.cur.executemany(
                """INSERT INTO hist_discipulados
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                data,
            )
            self.conexion.commit()
            self.cur.close()
            print("Registro insertado.")
        except IntegrityError:
            print(
                "Error al insertar los datos.",
            )

    def get_discipulados_hist(self):
        return read_sql("SELECT * FROM V_HIST_DISCIPULADOS", self.conexion)
