import time
from numpy import nan
import streamlit as st
from helpers.navigation import make_sidebar
from scripts.oDiscipulados import DataDiscipulados

st.set_page_config(page_title='Discipulados - Registro de sobres', 
                   layout='wide', 
                   page_icon='⚡')
make_sidebar()
data = DataDiscipulados()

st.header('Datos del sobre')

@st.cache_data
def liderazgo_activo():
    df = data.liderazgo()
    return df[df['estatus']==1]

@st.cache_data
def liderazgo_redes():
    return data.liderazgo_redes()

liderazgo = liderazgo_activo()
col1, col2 = st.columns(2, 
                        gap="small")
with col1:
    id_liderazgo = st.text_input(
                                label='id liderazgo',
                                value=liderazgo.iloc[0, 1],
                                disabled=True,
                 )
with col2:
    nombre = st.text_input(
                                label='nombre',
                                value=liderazgo.iloc[0, 2],
                                disabled=True,
                 )

col3, col4, col5 = st.columns(3, gap="small")

with col3:
    fecha_celula = st.date_input("fecha célula")
with col4:
    fecha_recibido = st.date_input("fecha recibido")
with col5:
    fecha_entregado = st.date_input("fecha entregado")

col6, col7, col8 = st.columns(3, gap="small")

with col6:
    redes = liderazgo_redes().replace(nan, '').copy()
    redes['buscador'] = redes['cod_red'] + ' | ' + redes['c_lider'] 
    cod_red = st.selectbox('Lista de redes:', 
                                            redes['buscador'],
                                            index=None,
                                            placeholder="seleccionar..",)

    cod_red = str.strip(cod_red.split('|')[0]) if not cod_red==None else ''


with col7:
    expositor = st.text_input(
                              label='expositor',
                              disabled=False,
                              placeholder='ingrese el nombre del expositor del tema.')
with col8:
    tema = st.text_input(
                         label='tema',
                         disabled=False,
                         placeholder='ingrese el tema impartido.')

numero_asistentes = st.slider("número de asistentes", 0, 100, 10)
bs = st.number_input("ingrese el monto en bolívares.")
usd = st.number_input("ingrese el monto en dólares.")

sobre_entregado = st.checkbox("sobre entregado?")
if sobre_entregado:
   sobre_entregado=True
   
observ = st.text_input(
                       label='observaciones',
                       disabled=False,
                       placeholder='ingrese las observaciones')

registro = [(None, 
             id_liderazgo, 
             fecha_celula, 
             fecha_recibido, 
             fecha_entregado, 
             cod_red,
             expositor, 
             tema,
             numero_asistentes,
             bs,
             usd,
             sobre_entregado,
             observ)]  

if st.button("agregar"):
    data.insert_hist_discipulados(registro)
    st.info('Registro insertado.')
    time.sleep(3)

