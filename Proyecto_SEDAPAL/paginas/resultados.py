import streamlit as st
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

#---------------------------------------------------------
# CARGA DE DATOS
#---------------------------------------------------------

@st.cache_data
def cargar_datos():
    return pd.read_csv("datos/produccion_agua.csv")


def mostrar():

    st.title("Resultados del Modelo - SEDAPAL")

    #---------------------------------------------------------
    # DATOS
    #---------------------------------------------------------

    df = cargar_datos()

    df_model = pd.get_dummies(
        df,
        columns=["MES", "CUENCA", "TIPO_FUENTE", "INFRAESTRUCTURA"]
    )

    X = df_model.drop("VOLUMEN_M3", axis=1)
    y = df_model["VOLUMEN_M3"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    modelo = LinearRegression()
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)

    #---------------------------------------------------------
    # MÉTRICAS
    #---------------------------------------------------------

    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    #---------------------------------------------------------
    # KPIs VISUALES
    #---------------------------------------------------------

    st.subheader("Indicadores de desempeño del modelo")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("MAE", f"{mae:,.2f}")

    with c2:
        st.metric("MSE", f"{mse:,.2f}")

    with c3:
        st.metric("RMSE", f"{rmse:,.2f}")

    with c4:
        st.metric("R²", f"{r2:.4f}")

    st.divider()

    #---------------------------------------------------------
    # INTERPRETACIÓN
    #---------------------------------------------------------

    st.subheader("Interpretación del modelo")

    st.write("""
    El modelo de regresión multivariable permite estimar el volumen de producción de agua potable
    a partir de variables operativas del sistema SEDAPAL.

    Un valor de R² cercano a 1 indica que el modelo explica adecuadamente la variabilidad de los datos.
    El MAE y RMSE reflejan el margen de error promedio en las predicciones.
    """)

    #---------------------------------------------------------
    # GRÁFICO REAL VS PREDICHO
    #---------------------------------------------------------

    st.subheader("Comparación: Valores reales vs predichos")

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    ax.scatter(y_test, y_pred, alpha=0.5)

    # línea ideal
    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())

    ax.plot([min_val, max_val], [min_val, max_val], "r--")

    ax.set_xlabel("Valores reales (m³)")
    ax.set_ylabel("Predicciones (m³)")
    ax.set_title("Desempeño del modelo")

    ax.ticklabel_format(style="plain", axis="both")

    ax.grid(True, linestyle="--", alpha=0.3)

    st.pyplot(fig)