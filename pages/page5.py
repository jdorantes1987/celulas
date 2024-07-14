import time
from numpy import nan
from pandas import to_datetime
import datetime
import streamlit as st
from helpers.navigation import make_sidebar
from scripts.oCelulas import DataCelulas
from scripts.oDiscipulados import DataDiscipulados

st.set_page_config(page_title='Estadísticas Generales', 
                   layout='wide', 
                   page_icon='⚡')

make_sidebar()
data_celulas = DataCelulas()
data_discipulados = DataDiscipulados()
today = datetime.datetime.now()

@st.cache_data
def celulas_activas():
    return data_celulas.celulas_activas()

@st.cache_data
def celulas_activas_historico():
    return data_celulas.celulas_activas_hist()

@st.cache_data
def discipulados_historico():
    return data_discipulados.discipulados_historico()

st.title('Células')

with st.expander('Activas'):
    celulas_activas = celulas_activas()
    st.dataframe(celulas_activas,
                        use_container_width=False, 
                        hide_index=True)
    st.header('Cantidad de células')
    col1, col2 = st.columns(2, 
                        gap="small")
    celulas_activas.rename(columns={'c_lider': 'lider', 
                                'id_celula': 'cantidad'}, inplace=True)
    
    with col1:
        st.write('-> Por código base')
        st.write(celulas_activas.groupby(['cod_base'])['cantidad'].count())
        cantidad = celulas_activas['lider'].value_counts().sum()
        st.write(f'Total cantidad de células:  {cantidad}')
        
    with col2:
        st.write('-> Por sub-código')
        st.write(celulas_activas.groupby(['cod_red', 'lider'])['cantidad'].count())
        
    st.header('-> Sobres por entregar:')
    sobres_por_entregar = DataCelulas().sobres_por_entregar().groupby(['cod_red', 
                                                                       'c_lider']).agg({'monto_bs': 'sum', 
                                                                                        'monto_usd': 'sum',
                                                                                        'id': 'count'}).reset_index()
    sobres_por_entregar.loc['999'] = ['TOTAL', ' ', sobres_por_entregar['monto_bs'].sum(), sobres_por_entregar['monto_usd'].sum(), sobres_por_entregar['id'].sum()]
    sobres_por_entregar = sobres_por_entregar.reset_index(drop=True)
    sobres_por_entregar['monto_bs'] = sobres_por_entregar['monto_bs'].apply('{:,.2f}'.format)
    sobres_por_entregar['monto_usd'] = sobres_por_entregar['monto_usd'].apply('${:,.2f}'.format)
    sobres_por_entregar.rename(columns={'id': 'cantidad'}, inplace=True)
    st.write(sobres_por_entregar)
    
    st.header('-> Última actividad del mes:')
 
    celula_con_activ = celulas_activas_historico().copy()
    celula_con_activ['fecha'] = to_datetime(celula_con_activ['fecha'], yearfirst=True)
    grouped = celula_con_activ.groupby(['cod_red', 'anfitriones' ,'c_lider', 'direccion'])
    last_day_of_month = grouped['fecha'].max().reset_index()
    last_day_of_month["dias_transc"] = (today - last_day_of_month['fecha']).dt.days  # Dias transcurridos entre la ultima fecha al dia de hoy
    last_day_of_month['fecha'] = last_day_of_month['fecha'].dt.date
    grouped2 = last_day_of_month.groupby(['cod_red',
                                         'anfitriones', 
                                         'c_lider',
                                         'direccion'])[['fecha', 'dias_transc']].max()
    st.write(grouped2)
    
    st.header('-> Histórico de celulas:')
    hist_celulas = celulas_activas_historico().copy()
    st.write(hist_celulas)


st.title('Discipulados')
with st.expander('Datos'):
    discipulados_historico = discipulados_historico()
    st.header('-> Sobres por entregar:')
    sobres = discipulados_historico[discipulados_historico['sobre_entregado']==0]
    sobres_por_entregar = sobres.groupby(['cod_red', 
                                          'c_lider']).agg({'monto_bs': 'sum', 
                                                           'monto_usd': 'sum',
                                                           'id': 'count'}).reset_index()
    sobres_por_entregar.loc['999'] = ['TOTAL', ' ', sobres_por_entregar['monto_bs'].sum(), sobres_por_entregar['monto_usd'].sum(), sobres_por_entregar['id'].sum()]
    sobres_por_entregar = sobres_por_entregar.reset_index(drop=True)
    sobres_por_entregar['monto_bs'] = sobres_por_entregar['monto_bs'].apply('{:,.2f}'.format)
    sobres_por_entregar['monto_usd'] = sobres_por_entregar['monto_usd'].apply('${:,.2f}'.format)
    sobres_por_entregar.rename(columns={'id': 'cantidad'}, inplace=True)
    st.write(sobres_por_entregar)
    
    
    st.header('-> Última actividad del mes:')
    discipulados_historico['fecha'] = to_datetime(discipulados_historico['fecha'], yearfirst=True)
    grouped = discipulados_historico.groupby(['cod_red', 'c_lider'])
    last_day_of_month = grouped['fecha'].max().reset_index()
    last_day_of_month["dias_transc"] = (today - last_day_of_month['fecha']).dt.days  # Dias transcurridos entre la ultima fecha al dia de hoy
    last_day_of_month['fecha'] = last_day_of_month['fecha'].dt.date
    grouped2 = last_day_of_month.groupby(['cod_red',
                                         'c_lider',])[['fecha', 'dias_transc']].max()
    st.write(grouped2)
    
    st.header('-> Histórico de díscipulados:')
    st.write(discipulados_historico)

    