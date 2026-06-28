import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

@st.cache_data # Si estás usando el caché de streamlit
def cargar():
    return pd.read_csv("Proyecto_SEDAPAL/datos/produccion_agua.csv")
    # O también puedes usar la ruta relativa usando dos puntos si falla:
    # return pd.read_csv("../datos/produccion_agua.csv")

def mostrar():

    st.title("Modelo Predictivo")

    df = cargar()

    # One Hot Encoding limpio
    df = pd.get_dummies(df, columns=["MES","CUENCA","TIPO_FUENTE","INFRAESTRUCTURA"])

    X = df.drop("VOLUMEN_M3", axis=1)
    y = df["VOLUMEN_M3"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, pred)
    mse = mean_squared_error(y_test, pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, pred)

    st.subheader("Métricas del modelo")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("MAE", f"{mae:,.2f}")
    c2.metric("MSE", f"{mse:,.2f}")
    c3.metric("RMSE", f"{rmse:,.2f}")
    c4.metric("R²", f"{r2:.4f}")

    st.subheader("Real vs Predicho")

    fig, ax = plt.subplots()

    ax.scatter(y_test, pred, alpha=0.5)

    min_v = min(y_test.min(), pred.min())
    max_v = max(y_test.max(), pred.max())

    ax.plot([min_v, max_v], [min_v, max_v], "r--")

    ax.set_xlabel("Real")
    ax.set_ylabel("Predicho")

    ax.ticklabel_format(style="plain", axis="both")

    st.pyplot(fig)
