import streamlit as st
import pandas as pd
from pathlib import Path


def mostrar():

    st.title("Datos Oficiales de SEDAPAL")

    ruta_produccion = Path("datos/produccion_agua.csv")
    ruta_conexiones = Path("datos/conexiones.csv")

    if ruta_produccion.exists():

        df_produccion = pd.read_csv(ruta_produccion)

        st.subheader("Producción de Agua Potable")

        st.write(f"Registros: {df_produccion.shape[0]}")
        st.write(f"Columnas: {df_produccion.shape[1]}")

        st.dataframe(df_produccion)

    else:

        st.error("No se encontró el archivo produccion_agua.csv")

    st.divider()

    if ruta_conexiones.exists():

        df_conexiones = pd.read_csv(ruta_conexiones)

        st.subheader("Conexiones de Agua Potable")

        st.write(f"Registros: {df_conexiones.shape[0]}")
        st.write(f"Columnas: {df_conexiones.shape[1]}")

        st.dataframe(df_conexiones)

    else:

        st.error("No se encontró el archivo conexiones.csv")