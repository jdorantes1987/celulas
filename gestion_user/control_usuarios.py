import sys
import os
# La ruta SYS es una lista de directorios que Python interpreta para buscar cuando se inicia
# sys.path.append('..\\bantel') # Agrega el directorio Bantel a la ruta SYS
# import accesos.data_base as db
# import gestion_user.usuarios as u
# import gestion_user.control_roles as croles


# def data_user(user, pw):
#     sql = f"""
#           select * from usuarios where idusuario ='{user}' and PWDCOMPARE('{pw}', passw)= 1
#           """
#     return db.get_read_sql(sql=sql, 
#                            host=os.getenv('HOST_DESARROLLO_PROFIT'), 
#                            base_de_datos=os.getenv('DB_NAME_DERECHA_PROFIT'))

# def aut_user(user, pw):
#     aut = False
#     df_users = data_user(user, pw)
#     if len(df_users) > 0:
#         u.ClsUsuarios(df_users['idusuario'][0], df_users['nombre'][0], df_users['categoria'][0])
#         croles.set_roles(u.ClsUsuarios.id_usuario())
#         aut = True  
#     return aut
    
    
# aut = aut_user('amonasterios', 'ale')    
# print(aut)
# print(u.ClsUsuarios.id_usuario())
# print(u.ClsUsuarios.nombre())
# print(u.ClsUsuarios.categoria())
# croles.set_roles(u.ClsUsuarios.id_usuario())
# print('Modulo derecha habilitado:', r.ClsUsuariosRoles.dic_roles['Derecha'])
# print('Modulo Facturación habilitado:', r.ClsUsuariosRoles.dic_roles['Facturacion'])


