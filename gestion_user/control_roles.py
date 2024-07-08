
from sqlite3 import connect
from pandas import read_sql
from gestion_user.usuarios_roles import ClsUsuariosRoles

db_path = r'DB_Celulas.db'

def dict_users_rols(id_user):
    conexion = connect(db_path)
    sql = f"""
          SELECT * FROM usuarios_roles WHERE idusuario ='{id_user}'
          """
    df = read_sql(sql, conexion)
    users = df.set_index('modulo')['habilitado']
    return users.to_dict()

def set_roles(id_user):
    d_roles = dict_users_rols(id_user)
    ClsUsuariosRoles(d_roles)


# set_roles('JDORANTES')
# print(ClsUsuariosRoles.roles()['SOBRES-CELULAS'])


