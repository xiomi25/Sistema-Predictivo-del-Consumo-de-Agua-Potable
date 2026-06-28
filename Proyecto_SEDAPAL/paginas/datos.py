import streamlit as st
import pandas as pd
from pathlib import Path

def mostrar():
    st.title("Datos Oficiales de SEDAPAL")

    carpeta_actual = Path(__file__).resolve().parent

    ruta_produccion = carpeta_actual.parent / "datos" / "produccion_agua.csv"
    ruta_conexiones = carpeta_actual.parent / "datos" / "conexiones.csv"

    if ruta_produccion.exists():
        df_produccion = pd.read_csv(ruta_produccion)
        st.subheader("Producción de Agua Potable")
        st.write(f"Registros: {df_produccion.shape[0]}")
        st.write(f"Columnas: {df_produccion.shape[1]}")
        st.dataframe(df_produccion)
    else:
        st.error(f"No se encontró el archivo en: {ruta_produccion}")

    st.divider()

    if ruta_conexiones.exists():
        df_conexiones = pd.read_csv(ruta_conexiones)
        st.subheader("Conexiones de Agua Potable")
        st.write(f"Registros: {df_conexiones.shape[0]}")
        st.write(f"Columnas: {df_conexiones.shape[1]}")
        st.dataframe(df_conexiones)
    else:
        st.error(f"No se encontró el archivo en: {ruta_conexiones}")
