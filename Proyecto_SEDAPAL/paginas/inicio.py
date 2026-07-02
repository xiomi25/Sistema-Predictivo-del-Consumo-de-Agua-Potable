import streamlit as st
from PIL import Image
from pathlib import Path


def mostrar():
    logo = Path(__file__).resolve().parent.parent / "assets" / "logo_sedapal.png"
    col1, col2 = st.columns([1, 4])
    with col1:
        if logo.exists():
            st.image(Image.open(logo), width=120)
    with col2:
        st.title("Sistema Predictivo del Consumo de Agua Potable")
        st.caption("SEDAPAL | Empresa de Servicio de Agua Potable y Alcantarillado de Lima")

    st.divider()
    st.markdown("""
    ## Sistema de análisis y predicción
    Este sistema integra análisis exploratorio de datos y modelos de Machine Learning
    para **predecir el porcentaje de Agua No Facturada (ANF)** en SEDAPAL
    a partir de variables operativas históricas.

    Su objetivo es apoyar la toma de decisiones institucionales orientadas a
    **reducir las pérdidas de agua** y mejorar la eficiencia en la distribución
    del recurso hídrico en Lima Metropolitana.
    """)

    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("Objetivo", "Predecir Agua No Facturada")
    c2.metric("Modelo", "Regresión multivariable")
    c3.metric("Tecnología", "Python + Scikit-learn")

    st.divider()
    st.markdown("""
    ### Alcance del sistema
    - Análisis exploratorio de variables operativas (2005–2017)
    - Matriz de correlación entre variables y ANF
    - Modelado predictivo con regresión lineal múltiple
    - Evaluación del modelo con métricas R², MAE y RMSE
    - Simulación de escenarios para estimar el ANF futuro

    ### Fuente de datos
    - **Anuario Estadístico SEDAPAL 2017** — Gerencia de Desarrollo e Investigación
    - **Portal de Transparencia SEDAPAL** — datos abiertos de producción y conexiones
    """)
