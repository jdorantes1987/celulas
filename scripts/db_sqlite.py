from sqlite3 import IntegrityError

from pandas import read_sql

from scripts.interfaz_data_source import IDataSource


class BD_SQLite_Celulas(IDataSource):
    def __init__(self, conexion) -> None:
        self.conexion = conexion
        self.cur = conexion.cursor()

    def get_celulas(self):
        sql = """
                SELECT c.id_liderazgo, c.id_celula, c.anfitriones, c.id_cod,
                    c.direccion, c.estatus AS estatus_celula,lxc.cod_red,
                    lxc.c_lider, lxc.c_lider_red, lxc.nombre_lider,
                    lxc.estatus AS estatus_liderazgo
                FROM celulas AS c LEFT JOIN (
                    SELECT c1.id_liderazgo, c1.id_cod, c1.cod_red, c1.nombre_liderazgo as c_lider,
                    IFNULL(c1.cod_base, c1.cod_red) as cod_base,
                    IFNULL(c2.cod_red, c1.cod_red) as c_lider_red,
                    IFNULL(c2.nombre_liderazgo, c1.nombre_liderazgo) as nombre_lider, c1.estatus
                    FROM ((SELECT * FROM codigos as hl LEFT JOIN liderazgo_x_codigo AS lxc ON hl.cod_red=lxc.id_codigo LEFT JOIN liderazgo AS l ON  hl.id_liderazgo=l.id_liderazgo) as c1
                        LEFT JOIN
                        (SELECT * FROM codigos as hl LEFT JOIN liderazgo_x_codigo AS lxc ON hl.cod_red=lxc.id_codigo LEFT JOIN liderazgo AS l ON  hl.id_liderazgo=l.id_liderazgo) as c2
                        ON
                        c1.cod_lider=c2.cod_red AND c1.id_liderazgo=c2.id_liderazgo) as lxc
                        LEFT JOIN liderazgo l ON lxc.id_liderazgo=l.id_liderazgo
                    ORDER BY c1.cod_base, c1.cod_red) AS lxc ON c.id_cod=lxc.id_cod
            """
        return read_sql(sql, self.conexion)

    def get_historico_celulas(self):
        sql = """
                SELECT hcl.*, t.descrip, c.anfitriones, c.id_cod, lxc.cod_red, lxc.c_lider ,c.direccion, c.estatus as estatus_celula, lxc.estatus as estatus_liderazgo
                FROM hist_celulas AS hcl LEFT JOIN celulas AS c ON hcl.id_celula=c.id_celula LEFT JOIN (
                    SELECT c1.id_liderazgo, c1.id_cod, c1.cod_red, c1.nombre_liderazgo as c_lider,
                    IFNULL(c1.cod_base, c1.cod_red) as cod_base,
                    IFNULL(c2.cod_red, c1.cod_red) as c_lider_red,
                    IFNULL(c2.nombre_liderazgo, c1.nombre_liderazgo) as nombre_lider, c1.estatus
                    FROM ((SELECT * FROM codigos as hl LEFT JOIN liderazgo_x_codigo AS lxc ON hl.cod_red=lxc.id_codigo LEFT JOIN liderazgo AS l ON  hl.id_liderazgo=l.id_liderazgo) as c1
                        LEFT JOIN
                        (SELECT * FROM codigos as hl LEFT JOIN liderazgo_x_codigo AS lxc ON hl.cod_red=lxc.id_codigo LEFT JOIN liderazgo AS l ON  hl.id_liderazgo=l.id_liderazgo) as c2
                        ON
                        c1.cod_lider=c2.cod_red AND c1.id_liderazgo=c2.id_liderazgo) as lxc
                        LEFT JOIN liderazgo l ON lxc.id_liderazgo=l.id_liderazgo
                    ORDER BY c1.cod_base, c1.cod_red) AS lxc ON c.id_cod=lxc.id_cod LEFT JOIN temas AS t ON hcl.id_tema = t.id_tema
            """
        return read_sql(sql, self.conexion)

    def get_liderazgo(self):
        return read_sql("SELECT * FROM liderazgo", self.conexion)

    def get_liderazgo_redes(self):
        sql = """
                SELECT c1.id_liderazgo, c1.id_cod, c1.cod_red, c1.nombre_liderazgo as c_lider,
                    IFNULL(c1.cod_base, c1.cod_red) as cod_base,
                    IFNULL(c2.cod_red, c1.cod_red) as c_lider_red,
                    IFNULL(c2.nombre_liderazgo, c1.nombre_liderazgo) as nombre_lider, c1.estatus
                FROM ((SELECT * FROM codigos as hl LEFT JOIN liderazgo_x_codigo AS lxc ON hl.cod_red=lxc.id_codigo LEFT JOIN liderazgo AS l ON  hl.id_liderazgo=l.id_liderazgo) as c1
                    LEFT JOIN
                    (SELECT * FROM codigos as hl LEFT JOIN liderazgo_x_codigo AS lxc ON hl.cod_red=lxc.id_codigo LEFT JOIN liderazgo AS l ON  hl.id_liderazgo=l.id_liderazgo) as c2
                    ON
                    c1.cod_lider=c2.cod_red AND c1.id_liderazgo=c2.id_liderazgo) as lxc
                    LEFT JOIN liderazgo l ON lxc.id_liderazgo=l.id_liderazgo
                WHERE l.estatus=1
                ORDER BY c1.cod_base, c1.cod_red
            """
        return read_sql(sql, self.conexion)

    def get_discipulados(self):
        sql = """
                SELECT d.id_discipulado, d.id_liderazgo, d.id_cod, lxc.cod_red, lxc.c_lider, lxc.cod_base, lxc.c_lider_red, lxc.nombre_lider, lxc.estatus AS estatus_liderazgo
                FROM discipulados AS d LEFT JOIN (
                    SELECT c1.id_liderazgo, c1.id_cod, c1.cod_red, c1.nombre_liderazgo as c_lider,
                    IFNULL(c1.cod_base, c1.cod_red) as cod_base,
                    IFNULL(c2.cod_red, c1.cod_red) as c_lider_red,
                    IFNULL(c2.nombre_liderazgo, c1.nombre_liderazgo) as nombre_lider, c1.estatus
                    FROM ((SELECT * FROM codigos as hl LEFT JOIN liderazgo_x_codigo AS lxc ON hl.cod_red=lxc.id_codigo LEFT JOIN liderazgo AS l ON  hl.id_liderazgo=l.id_liderazgo) as c1
                        LEFT JOIN
                        (SELECT * FROM codigos as hl LEFT JOIN liderazgo_x_codigo AS lxc ON hl.cod_red=lxc.id_codigo LEFT JOIN liderazgo AS l ON  hl.id_liderazgo=l.id_liderazgo) as c2
                        ON
                        c1.cod_lider=c2.cod_red AND c1.id_liderazgo=c2.id_liderazgo) as lxc
                        LEFT JOIN liderazgo l ON lxc.id_liderazgo=l.id_liderazgo
                    WHERE l.estatus=1
                    ORDER BY c1.cod_base, c1.cod_red
                    ) as lxc ON d.id_cod=lxc.id_cod
            """
        return read_sql(sql, self.conexion)

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

    def get_historico_discipulados(self):
        sql = """
                SELECT hd.*, d.id_cod, cxl.cod_red, cxl.c_lider, cxl.estatus
                FROM hist_discipulados AS hd LEFT JOIN discipulados AS d ON hd.id_discipulado=d.id_discipulado LEFT JOIN
                (
                    SELECT c1.id_liderazgo, c1.id_cod, c1.cod_red, c1.nombre_liderazgo as c_lider,
                        IFNULL(c1.cod_base, c1.cod_red) as cod_base,
                        IFNULL(c2.cod_red, c1.cod_red) as c_lider_red,
                        IFNULL(c2.nombre_liderazgo, c1.nombre_liderazgo) as nombre_lider, c1.estatus
                    FROM ((SELECT * FROM codigos as hl LEFT JOIN liderazgo_x_codigo AS lxc ON hl.cod_red=lxc.id_codigo LEFT JOIN liderazgo AS l ON  hl.id_liderazgo=l.id_liderazgo) as c1
                        LEFT JOIN
                        (SELECT * FROM codigos as hl LEFT JOIN liderazgo_x_codigo AS lxc ON hl.cod_red=lxc.id_codigo LEFT JOIN liderazgo AS l ON  hl.id_liderazgo=l.id_liderazgo) as c2
                        ON
                        c1.cod_lider=c2.cod_red AND c1.id_liderazgo=c2.id_liderazgo) as lxc
                        LEFT JOIN liderazgo l ON lxc.id_liderazgo=l.id_liderazgo
                    ORDER BY c1.cod_base, c1.cod_red) as cxl ON d.id_cod=cxl.id_cod
            """
        return read_sql(sql, self.conexion)


if __name__ == "__main__":
    import sqlite3

    # Example usage
    conn = sqlite3.connect("DB_Celulas.db")
    db = BD_SQLite_Celulas(conn)

    data = db.get_discipulados()
    print(data)

    # Close the connection
    conn.close()
