import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from pathlib import Path

# Con 13 años de datos (2005-2017) el dataset ya soporta las 5 variables
# operativas completas planteadas en el marco teórico del proyecto.
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


def entrenar_modelo(df):
    X = df[FEATURES]
    y = df["agua_no_facturada_pct"]

    loo = LeaveOneOut()
    y_real, y_pred_loo = [], []

    for train_idx, test_idx in loo.split(X):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
        m = LinearRegression()
        m.fit(X_train, y_train)
        y_real.append(y_test.values[0])
        y_pred_loo.append(m.predict(X_test)[0])

    modelo_final = LinearRegression()
    modelo_final.fit(X, y)

    mae  = mean_absolute_error(y_real, y_pred_loo)
    mse  = mean_squared_error(y_real, y_pred_loo)
    rmse = np.sqrt(mse)
    r2   = r2_score(y_real, y_pred_loo)

    return modelo_final, FEATURES, y_real, y_pred_loo, mae, mse, rmse, r2


def mostrar():
    st.title("Modelo Predictivo")
    st.markdown("""
    Se aplica un modelo de **regresión lineal múltiple** para predecir el porcentaje
    de **Agua No Facturada (ANF)** de SEDAPAL a partir de las cinco variables
    operativas planteadas en el marco teórico: inversión anual, cobertura de
    micromedición, roturas en redes, atoros en alcantarillado y continuidad
    del servicio.
    """)

    df = cargar_datos()

    modelo, features, y_real, y_pred, mae, mse, rmse, r2 = entrenar_modelo(df)
    st.session_state["modelo"]   = modelo
    st.session_state["features"] = features
    st.session_state["df"]       = df

    st.subheader("Métricas del modelo (validación Leave-One-Out)")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("MAE",  f"{mae:.4f} %")
    c2.metric("MSE",  f"{mse:.4f}")
    c3.metric("RMSE", f"{rmse:.4f} %")
    c4.metric("R²",   f"{r2:.4f}")

    st.caption(
        f"Modelo entrenado con {len(df)} observaciones anuales (2005–2017), "
        "lo que permite incorporar las 5 variables operativas sin riesgo de "
        "sobreajuste, a diferencia de la versión inicial con solo 5 años de datos."
    )
    st.divider()

    st.subheader("Valores reales vs predichos")
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(y_real, y_pred, color="#0b3d91", zorder=5, s=70)
    lim = [min(y_real + y_pred) - 0.5, max(y_real + y_pred) + 0.5]
    ax.plot(lim, lim, "r--", label="Predicción perfecta")
    for i, anio in enumerate(df["anio"]):
        ax.annotate(str(anio), (y_real[i], y_pred[i]),
                    textcoords="offset points", xytext=(6, 4), fontsize=7)
    ax.set_xlabel("ANF real (%)")
    ax.set_ylabel("ANF predicha (%)")
    ax.set_title("Desempeño del modelo — Agua No Facturada")
    ax.legend()
    st.pyplot(fig)
    st.divider()

    st.subheader("Importancia de variables (coeficientes del modelo)")
    coef_df = pd.DataFrame({
        "Variable": features,
        "Coeficiente": modelo.coef_
    }).sort_values("Coeficiente", key=abs, ascending=True)

    fig2, ax2 = plt.subplots(figsize=(7, 4))
    colores = ["#d9534f" if c < 0 else "#0b3d91" for c in coef_df["Coeficiente"]]
    ax2.barh(coef_df["Variable"], coef_df["Coeficiente"], color=colores)
    ax2.axvline(0, color="black", linewidth=0.8)
    ax2.set_title("Coeficientes de regresión")
    ax2.set_xlabel("Valor del coeficiente")
    st.pyplot(fig2)
    st.caption(
        "Coeficiente negativo = la variable reduce el ANF. "
        "Coeficiente positivo = la variable aumenta el ANF."
    )
    st.divider()
