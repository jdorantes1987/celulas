from sqlite3 import connect

import bcrypt
from pandas import read_sql

import gestion_user.control_roles as croles
import gestion_user.usuarios as u

db_path = r"DB_Celulas.db"


def data_user(user):
    user = str(user).upper()
    conn = connect(db_path)
    sql = f"""
          SELECT * FROM usuarios WHERE idusuario ='{user}'
          """
    return read_sql(sql, conn)


def aut_user(user, pw):
    aut = False
    try:
        df_users = data_user(user)
        contrasenia_encript = bytes(df_users["passw"][0], "utf-8")
        varificar_passw = bcrypt.checkpw(bytes(pw, "utf-8"), contrasenia_encript)
    except Exception as e:
        varificar_passw = False
        print(e)
    if varificar_passw:
        u.ClsUsuarios(
            df_users["idusuario"][0], df_users["nombre"][0], df_users["categoria"][0]
        )
        croles.set_roles(u.ClsUsuarios.id_usuario())
        aut = True
    return aut
