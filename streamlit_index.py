import streamlit as st
import pandas as pd
# Asegúrate de que esta librería esté en tu requirements.txt
from streamlit_gsheets import GSheetsConnection 

# --- VARIABLES CORREGIDAS ---

# 1. CORRECCIÓN: Se debe usar solo el ID, no la URL completa.
# Tu ID extraído de la URL es: 1ffNb-jFqt9S0O2CaUQS59mleOkyOk911EaD2uDaMgVw
SPREADSHEET_ID = "1ffNb-jFqt9S0O2CaUQS59mleOkyOk911EaD2uDaMgVw" 

# 2. NOMBRE DE LA PESTAÑA: Correcto
WORKSHEET_NAME = "REPOSITORIO" 

# --- CÓDIGO DE CONEXIÓN ---

st.title("👥 Datos de REPOSITORIO desde Google Sheets")

try:
    # Conexión usando el Secret [gsheets]
    conn = st.connection("gsheets", type=GSheetsConnection) 

    # CORRECCIÓN: La variable SPREADSHEET_ID ahora se usa correctamente
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
    # Mensaje de error más detallado
    st.error(f"¡Error! Revisa que el Secret, el ID y el nombre de la hoja ('{WORKSHEET_NAME}') sean correctos. Detalle: {e}")
