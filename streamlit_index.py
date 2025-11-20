import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection 

# --- VARIABLES QUE DEBES REEMPLAZAR ---

# 1. PEGA EL ID LARGO de tu hoja de cálculo (el mismo que has estado usando)
spreadsheet_id = "https://docs.google.com/spreadsheets/d/1ffNb-jFqt9S0O2CaUQS59mleOkyOk911EaD2uDaMgVw/edit?gid=0#gid=0" 

# 2. NOMBRE ACTUALIZADO DE LA PESTAÑA
WORKSHEET_NAME = "REPOSITORIO" 

# --- CÓDIGO DE CONEXIÓN ---

st.title("👥 Datos de REPOSITORIO desde Google Sheets")

try:
    # Conexión usando el Secret [gsheets]
    conn = st.connection("gsheets", type=GSheetsConnection) 

    # Lectura de la pestaña "REPOSITORIO"
    df_datos = conn.read(
        spreadsheet=SPREADSHEET_ID,
        worksheet=WORKSHEET_NAME,
        ttl=5 
    )

    # Muestra los datos
    st.subheader(f"Primer registro cargado: {df_datos.shape[0]} filas")
    
    # Muestra los datos en Streamlit
    st.dataframe(df_datos)
    
    # Opcional: Muestra un valor específico para confirmar
    st.write(f"Nombre del primer registro: **{df_datos['nombres'][0]}**")

except Exception as e:
    st.error(f"¡Error! Revisa que el Secret, el ID y el nombre de la hoja ('{WORKSHEET_NAME}') sean correctos. Detalle: {e}")
