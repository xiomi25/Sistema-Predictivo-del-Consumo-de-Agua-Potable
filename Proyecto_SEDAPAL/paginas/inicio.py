import streamlit as st
from PIL import Image
from pathlib import Path

def mostrar():

    logo = Path("assets/logo_sedapal.png")

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
    para estimar la producción de agua potable en base a variables operativas de SEDAPAL.

    Su objetivo es apoyar la toma de decisiones mediante analítica avanzada.
    """)

    st.divider()

    c1, c2, c3 = st.columns(3)

    c1.metric("Objetivo", "Predicción de consumo")
    c2.metric("Modelo", "Regresión multivariable")
    c3.metric("Tecnología", "Python + ML")

    st.divider()

    st.markdown("""
    ### Alcance del sistema
    - Análisis exploratorio de datos
    - Modelado predictivo
    - Evaluación de desempeño
    - Simulación de escenarios
    """)