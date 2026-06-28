import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression

@st.cache_data
def cargar():
    return pd.read_csv("datos/produccion_agua.csv")

def mostrar():

    st.title("Predicción de Consumo")

    df = cargar()

    le = {}

    for col in ["MES","CUENCA","TIPO_FUENTE","INFRAESTRUCTURA"]:
        le[col] = LabelEncoder()
        df[col] = le[col].fit_transform(df[col])

    X = df[["MES","CUENCA","TIPO_FUENTE","INFRAESTRUCTURA"]]
    y = df["VOLUMEN_M3"]

    model = LinearRegression()
    model.fit(X, y)

    st.subheader("Parámetros de entrada")

    mes = st.selectbox("Mes", cargar()["MES"].unique())
    cuenca = st.selectbox("Cuenca", cargar()["CUENCA"].unique())
    tipo = st.selectbox("Tipo de fuente", cargar()["TIPO_FUENTE"].unique())
    infra = st.selectbox("Infraestructura", cargar()["INFRAESTRUCTURA"].unique())

    if st.button("Predecir"):

        entrada = [
            le["MES"].transform([mes])[0],
            le["CUENCA"].transform([cuenca])[0],
            le["TIPO_FUENTE"].transform([tipo])[0],
            le["INFRAESTRUCTURA"].transform([infra])[0]
        ]

        pred = model.predict([entrada])[0]

        st.success(f"Consumo estimado: {pred:,.2f} m³")

        st.caption("Modelo entrenado con datos históricos de SEDAPAL")