import streamlit as st
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.linear_model import LinearRegression

FEATURES = [
    "inversion_miles_soles",
    "cobertura_micromedicion_pct",
    "roturas_redes",
    "atoros_alcantarillado",
    "horas_servicio_promedio"
]


@st.cache_data
def cargar_datos():
    ruta = Path(__file__).resolve().parent.parent / "datos" / "sedapal_anuario.csv"
    return pd.read_csv(ruta)


def obtener_modelo():
    if "modelo" not in st.session_state or st.session_state.get("features") != FEATURES:
        df = cargar_datos()
        X = df[FEATURES]
        y = df["agua_no_facturada_pct"]
        modelo = LinearRegression()
        modelo.fit(X, y)
        st.session_state["modelo"]   = modelo
        st.session_state["features"] = FEATURES
        st.session_state["df"]       = df
    return st.session_state["modelo"]


def mostrar():
    st.title("Predicción de Agua No Facturada")
    st.markdown("""
    Ingrese los valores operativos para estimar el **porcentaje de Agua No Facturada (ANF)**
    que el modelo predice dado ese escenario, a partir de las cinco variables
    operativas del Anuario Estadístico SEDAPAL 2005–2017.
    """)

    df = cargar_datos()
    modelo = obtener_modelo()

    st.subheader("Parámetros de entrada")

    col1, col2 = st.columns(2)
    with col1:
        inversion = st.number_input(
            "Inversión total (miles de soles)",
            min_value=100000, max_value=900000,
            value=int(df["inversion_miles_soles"].mean()),
            step=10000,
            help="Monto total de inversiones ejecutadas en el año"
        )
        micromedicion = st.slider(
            "Cobertura de micromedición (%)",
            min_value=60.0, max_value=100.0,
            value=float(df["cobertura_micromedicion_pct"].mean()),
            step=0.1
        )
        horas = st.slider(
            "Horas promedio de servicio (horas/día)",
            min_value=18.0, max_value=24.0,
            value=float(df["horas_servicio_promedio"].mean()),
            step=0.1
        )
    with col2:
        roturas = st.number_input(
            "Roturas en redes secundarias",
            min_value=1500, max_value=5000,
            value=int(df["roturas_redes"].mean()),
            step=50,
            help="Número de roturas registradas en redes secundarias de agua"
        )
        atoros = st.number_input(
            "Atoros en alcantarillado",
            min_value=30000, max_value=90000,
            value=int(df["atoros_alcantarillado"].mean()),
            step=1000,
            help="Número de atoros registrados en redes de alcantarillado"
        )

    st.divider()

    if st.button("Predecir ANF", type="primary"):
        entrada = np.array([[inversion, micromedicion, roturas, atoros, horas]])
        pred = modelo.predict(entrada)[0]

        color = "#d9534f" if pred > df["agua_no_facturada_pct"].mean() else "#5cb85c"
        st.markdown(
            f"<h2 style='color:{color}'>ANF estimada: {pred:.2f} %</h2>",
            unsafe_allow_html=True
        )

        anf_min = df["agua_no_facturada_pct"].min()
        anf_max = df["agua_no_facturada_pct"].max()
        st.info(
            f"Referencia histórica SEDAPAL 2005–2017: "
            f"mínimo {anf_min:.2f}% (2017) — máximo {anf_max:.2f}% (2005)"
        )

        if pred <= anf_min:
            st.success("El escenario ingresado mejoraría el mejor resultado histórico de SEDAPAL.")
        elif pred >= anf_max:
            st.warning("El escenario ingresado superaría el peor nivel histórico registrado.")
        else:
            st.info("El resultado está dentro del rango histórico de SEDAPAL.")

        st.caption("Modelo entrenado con datos del Anuario Estadístico SEDAPAL 2005–2017.")
