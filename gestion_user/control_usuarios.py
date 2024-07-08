import bcrypt
from sqlite3 import connect
from pandas import read_sql
import gestion_user.usuarios as u
import gestion_user.control_roles as croles

db_path = r'DB_Celulas.db'


def data_user(user):
    user=str(user).upper()
    conn = connect(db_path)
    sql = f"""
          SELECT * FROM usuarios WHERE idusuario ='{user}'
          """
    return read_sql(sql, conn)

def aut_user(user, pw):
    aut = False
    try:
        df_users = data_user(user)
        contrasenia_encript = bytes(df_users['passw'][0], 'utf-8')
        varificar_passw = bcrypt.checkpw(bytes(pw, 'utf-8'), contrasenia_encript)
    except Exception as e:
        varificar_passw=False
    if varificar_passw:
        u.ClsUsuarios(df_users['idusuario'][0], df_users['nombre'][0], df_users['categoria'][0])
        croles.set_roles(u.ClsUsuarios.id_usuario())
        aut = True  
    return aut
    
    
# aut = aut_user('JDORANTES', '18329114')    
# print(aut)
# print(u.ClsUsuarios.id_usuario())
# print(u.ClsUsuarios.nombre())
# print(u.ClsUsuarios.categoria())
# croles.set_roles(u.ClsUsuarios.id_usuario())
# print('Modulo derecha habilitado:', r.ClsUsuariosRoles.dic_roles['Derecha'])
# print('Modulo Facturación habilitado:', r.ClsUsuariosRoles.dic_roles['Facturacion'])


