import streamlit as st
import pandas as pd
from pathlib import Path


@st.cache_data
def cargar_anuario():
    ruta = Path(__file__).resolve().parent.parent / "datos" / "sedapal_anuario.csv"
    return pd.read_csv(ruta)


@st.cache_data
def cargar_produccion():
    ruta = Path(__file__).resolve().parent.parent / "datos" / "produccion_agua.csv"
    if ruta.exists():
        return pd.read_csv(ruta)
    return None


@st.cache_data
def cargar_conexiones():
    ruta = Path(__file__).resolve().parent.parent / "datos" / "conexiones.csv"
    if ruta.exists():
        return pd.read_csv(ruta)
    return None


def mostrar():
    st.title("Datos Oficiales de SEDAPAL")
    st.markdown("""
    Esta sección presenta los conjuntos de datos utilizados en el proyecto,
    obtenidos del **Anuario Estadístico SEDAPAL 2017** y del
    **Portal de Transparencia de SEDAPAL**.
    """)

    # ── Dataset principal del modelo ──────────────────────────────────────────
    st.subheader("Dataset principal — Anuario Estadístico 2013–2017")
    st.markdown("""
    Datos agregados por año extraídos del Anuario Estadístico de SEDAPAL.
    Este dataset es la fuente principal del modelo de regresión multivariable.
    """)
    df_anuario = cargar_anuario()
    st.write(f"Registros: {df_anuario.shape[0]}  |  Variables: {df_anuario.shape[1]}")
    st.dataframe(df_anuario, use_container_width=True)
    st.caption("Fuente: Anuario Estadístico SEDAPAL 2017 — Gerencia de Desarrollo e Investigación.")
    st.divider()

    # ── Dataset de producción mensual ─────────────────────────────────────────
    df_prod = cargar_produccion()
    if df_prod is not None:
        st.subheader("Producción de Agua Potable (datos mensuales)")
        st.markdown("Datos de producción mensual por cuenca e infraestructura del portal de transparencia.")
        st.write(f"Registros: {df_prod.shape[0]}  |  Columnas: {df_prod.shape[1]}")
        st.dataframe(df_prod, use_container_width=True)
        st.divider()

    # ── Dataset de conexiones ─────────────────────────────────────────────────
    df_con = cargar_conexiones()
    if df_con is not None:
        st.subheader("Conexiones de Agua Potable")
        st.markdown("Datos de conexiones activas por distrito y categoría de usuario.")
        st.write(f"Registros: {df_con.shape[0]}  |  Columnas: {df_con.shape[1]}")
        st.dataframe(df_con, use_container_width=True)
