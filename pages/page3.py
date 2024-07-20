import time
from numpy import nan
import streamlit as st
from helpers.navigation import make_sidebar
from scripts.oCelulas import DataCelulas



st.set_page_config(page_title='Células - Registro de sobres', 
                   layout='wide', 
                   page_icon='⚡')
make_sidebar()
data = DataCelulas()

st.header('Datos del sobre')

@st.cache_data
def liderazgo_activo():
    df = data.liderazgo()
    return df[df['estatus']==1]

@st.cache_data
def celulas_activas():
    return data.celulas_activas()

@st.cache_data
def temas():
    return data.temas()


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

celulas = celulas_activas().replace(nan, '').copy()
celulas['buscador'] = celulas['id_celula'] + ' | ' + celulas['cod_red'] + ' | ' + celulas['c_lider']  + ' | ' + celulas['anfitriones'] + ' | ' + celulas['direccion'] 
id_celula = st.selectbox('Lista de células:', 
                                        celulas['buscador'],
                                        index=None,
                                        placeholder="seleccionar..",)

id_celula = str.strip(id_celula.split('|')[0]) if not id_celula==None else ''

col6, col7 = st.columns(2, gap="small")

with col6:
    expositor = st.text_input(
                                label='expositor',
                                disabled=False,
                                placeholder='ingrese el nombre del expositor del tema')

with col7:
    temas = temas().copy()
    temas['buscador'] = temas['id_tema'] + ' | ' + temas['descrip']
    tema_select = st.selectbox('lista de temas:', 
                                            temas['buscador'],
                                            index=None,
                                            placeholder="seleccionar..",)
    tema_select = str.strip(tema_select.split('|')[0]) if not tema_select==None else ''

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
             id_celula, 
             expositor, 
             tema_select,
             numero_asistentes,
             bs,
             usd,
             sobre_entregado,
             observ)]  

if st.button("agregar"):
    data.insert_hist_celulas(registro)
    st.info('Registro insertado.')
    time.sleep(3)

