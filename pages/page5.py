import time
from numpy import nan
import streamlit as st
from helpers.navigation import make_sidebar
from scripts.oCelulas import DataCelulas

st.set_page_config(page_title='Estadísticas Generales', 
                   layout='wide', 
                   page_icon='⚡')

make_sidebar()
data = DataCelulas()

@st.cache_data
def celulas_activas():
    return data.celulas_activas()

st.header('CELULAS')

with st.expander('Activas'):
    celulas_activas = celulas_activas()
    st.dataframe(celulas_activas,
                        use_container_width=False,
                        hide_index=True)
    st.write('Cantidad por código')
    celulas_activas.rename(columns={'c_lider': 'lider', 
                                'id_celula': 'cantidad'}, inplace=True)
    
    st.write('->Por códigos base')
    st.write(celulas_activas.groupby(['cod_base'])['cantidad'].count())
    st.write('->Por sub-códigos')
    st.write(celulas_activas.groupby(['cod_red', 'lider'])['cantidad'].count())
    cantidad = celulas_activas['lider'].value_counts().sum()
    st.write(f'Total cantidad de células:  {cantidad}')

st.header('DISCIPULADOS')
