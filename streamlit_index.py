import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection 

st.set_page_config(layout="wide")
st.title("📊 Requisitos del Proyecto desde Google Sheets")

conn = st.connection("gsheets", type=GSheetsConnection)

spreadsheet_id = "PEGA_AQUÍ_EL_ID_DE_TU_HOJA_DE_CÁLCULO" 

try:
    df_requisitos = conn.read(
        spreadsheet=spreadsheet_id,
        worksheet="Hoja1",
        ttl=5 
    )

    st.subheader("Datos Cargados:")
    st.dataframe(df_requisitos)

except Exception as e:
    st.error(f"Error al leer Google Sheets. Revisa el ID de la hoja, el nombre de la pestaña y los permisos de la Cuenta de Servicio. Error: {e}")
