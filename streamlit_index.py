import streamlit as st
import pandas as pd
import gspread 
import tempfile
import json
import os 

# --- VARIABLES DE CONFIGURACIÓN ---
# ID de tu hoja de cálculo (reemplaza si es necesario)
SPREADSHEET_ID = "1ffNb-jFqt9S0O2CaUQS59mleOkyOk911EaD2uDaMgVw" 
# Nombre de la pestaña que contiene los datos de REPOSITORIO
WORKSHEET_NAME = "REPOSITORIO" 

st.set_page_config(layout="wide")
st.title("👥 Datos de REPOSITORIO (Conexión Estable con gspread)")

# Usamos @st.cache_data para guardar los datos en caché y evitar peticiones repetidas a Google
@st.cache_data(ttl=5)
def load_data():
    temp_filepath = None
    try:
        # 1. AUTENTICACIÓN: Lee el contenido del Secret [gsheets]
        if "gsheets" not in st.secrets:
            st.error("Error: El secret [gsheets] no está configurado en Streamlit Cloud. Revisa que el nombre sea 'gsheets'.")
            return pd.DataFrame()
            
        gcp_secrets = st.secrets["gsheets"]

        # 2. CREACIÓN DE ARCHIVO TEMPORAL: gspread necesita el JSON de la clave en un archivo
        # Esto es un patrón de seguridad estándar.
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_json_file:
            # 🛑 CORRECCIÓN APLICADA AQUÍ: Convertimos el objeto especial (AttrDict) a un dict estándar de Python.
            gcp_secrets_dict = dict(gcp_secrets)
            json.dump(gcp_secrets_dict, temp_json_file)
            temp_filepath = temp_json_file.name

        # 3. CONEXIÓN: Usa gspread para autenticarse con el archivo temporal
        gc = gspread.service_account(filename=temp_filepath)
        
        # 4. ACCESO AL ARCHIVO: Abre la hoja por su ID
        spreadsheet = gc.open_by_key(SPREADSHEET_ID)
        
        # 5. LECTURA: Selecciona la pestaña (worksheet)
        worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
        
        # 6. Conversión a DataFrame de Pandas (Lee la primera fila como encabezados)
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        
        return df

    except gspread.exceptions.WorksheetNotFound:
        st.error(f"Error: La pestaña '{WORKSHEET_NAME}' no fue encontrada. Revisa que el nombre en Google Sheets sea EXACTO.")
        return pd.DataFrame()
    except gspread.exceptions.SpreadsheetNotFound:
        st.error(f"Error: Hoja de cálculo con ID '{SPREADSHEET_ID}' no encontrada. Revisa el ID.")
        return pd.DataFrame()
    except Exception as e:
        # Manejo de otros errores críticos
        # Si este error persiste, la causa es el formato TOML o permisos.
        st.error(f"Error crítico en la conexión o autenticación. Causas comunes: 1) Formato TOML del secret incorrecto. 2) El email de la cuenta de servicio no tiene permiso de lectura en Google Sheets. Detalle: {e}")
        return pd.DataFrame()
    
    finally:
        # 7. LIMPIEZA: Eliminamos el archivo temporal (IMPORTANTE para la seguridad)
        if temp_filepath and os.path.exists(temp_filepath):
            os.remove(temp_filepath)

# --- EJECUCIÓN ---

st.info("Intentando cargar datos...")
df_datos = load_data()

if not df_datos.empty:
    st.success(f"¡Conexión exitosa! {df_datos.shape[0]} filas cargadas desde {WORKSHEET_NAME}.")
    st.subheader("Datos cargados:")
    st.dataframe(df_datos)
    
    # Muestra un valor de prueba para confirmar la lectura de la columna
    try:
        st.info(f"El valor de la columna 'nombres' del primer registro es: **{df_datos['nombres'].iloc[0]}**")
    except KeyError:
        st.warning("Verifica que la columna 'nombres' exista exactamente con ese nombre en la primera fila de tu hoja.")
