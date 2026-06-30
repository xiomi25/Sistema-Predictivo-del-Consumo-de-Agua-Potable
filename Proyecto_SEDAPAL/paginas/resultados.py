import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from pathlib import Path

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


def obtener_modelo_y_metricas():
    df = cargar_datos()
    X = df[FEATURES]
    y = df["agua_no_facturada_pct"]

    if "modelo" in st.session_state and st.session_state.get("features") == FEATURES:
        modelo = st.session_state["modelo"]
    else:
        modelo = LinearRegression()
        modelo.fit(X, y)
        st.session_state["modelo"] = modelo
        st.session_state["features"] = FEATURES

    loo = LeaveOneOut()
    y_real, y_pred = [], []
    for train_idx, test_idx in loo.split(X):
        m = LinearRegression()
        m.fit(X.iloc[train_idx], y.iloc[train_idx])
        y_real.append(y.iloc[test_idx].values[0])
        y_pred.append(m.predict(X.iloc[test_idx])[0])

    mae  = mean_absolute_error(y_real, y_pred)
    mse  = mean_squared_error(y_real, y_pred)
    rmse = np.sqrt(mse)
    r2   = r2_score(y_real, y_pred)

    return modelo, df, FEATURES, y_real, y_pred, mae, mse, rmse, r2


def mostrar():
    st.title("Resultados del Modelo — SEDAPAL")

    modelo, df, features, y_real, y_pred, mae, mse, rmse, r2 = obtener_modelo_y_metricas()

    st.subheader("Indicadores de desempeño del modelo")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("MAE",  f"{mae:.4f} %")
    c2.metric("MSE",  f"{mse:.4f}")
    c3.metric("RMSE", f"{rmse:.4f} %")
    c4.metric("R²",   f"{r2:.4f}")
    st.divider()

    st.subheader("Interpretación del modelo")
    coef_df = pd.DataFrame({"Variable": features, "Coeficiente": modelo.coef_})
    var_mas_influyente = coef_df.loc[coef_df["Coeficiente"].abs().idxmax(), "Variable"]

    st.markdown(f"""
    El modelo de **regresión lineal múltiple** fue entrenado con **{len(df)} años**
    de datos del Anuario Estadístico de SEDAPAL (2005–2017) para predecir el
    porcentaje de **Agua No Facturada (ANF)**, utilizando las cinco variables
    operativas planteadas en el marco teórico: inversión anual, cobertura de
    micromedición, roturas en redes, atoros en alcantarillado y continuidad
    del servicio.

    - Un **R² de {r2:.4f}** indica que el modelo explica el **{r2*100:.1f}%**
      de la variabilidad del ANF a partir de las variables operativas seleccionadas.
    - El **MAE de {mae:.4f}%** representa el error promedio absoluto entre el ANF
      real y el predicho por el modelo.
    - El **RMSE de {rmse:.4f}%** penaliza los errores grandes, siendo un indicador
      complementario de precisión.
    - La variable con mayor influencia en el modelo es **{var_mas_influyente}**.

    Ampliar el dataset de 5 a 13 observaciones anuales permitió incorporar
    nuevamente las cinco variables del marco teórico sin riesgo de sobreajuste,
    mejorando sustancialmente la capacidad predictiva del modelo respecto a la
    versión inicial entrenada solo con el periodo 2013–2017.
    """)
    st.divider()

    st.subheader("Comparación: Valores reales vs predichos")
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
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.legend()
    st.pyplot(fig)
    st.divider()

    st.subheader("Evolución del ANF real vs predicho (2005–2017)")
    fig2, ax2 = plt.subplots(figsize=(9, 4.5))
    ax2.plot(df["anio"], y_real, "o-", color="#0b3d91", label="ANF real", linewidth=2)
    ax2.plot(df["anio"], y_pred, "s--", color="#d9534f", label="ANF predicha", linewidth=2)
    ax2.set_xlabel("Año")
    ax2.set_ylabel("Agua No Facturada (%)")
    ax2.set_title("Tendencia del ANF: Real vs Predicho")
    ax2.legend()
    ax2.grid(True, linestyle="--", alpha=0.3)
    st.pyplot(fig2)

    st.caption(
        "Fuente: Anuarios Estadísticos SEDAPAL 2005–2017 — "
        "Gerencia de Desarrollo e Investigación."
    )
