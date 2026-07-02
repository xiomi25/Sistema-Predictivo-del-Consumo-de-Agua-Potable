import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


@st.cache_data
def cargar_datos():
    ruta = Path(__file__).resolve().parent.parent / "datos" / "sedapal_anuario.csv"
    return pd.read_csv(ruta)


def mostrar():
    st.title("Análisis Exploratorio de Datos")
    st.markdown("""
    Exploración de las variables del **Anuario Estadístico SEDAPAL 2005–2017**
    utilizadas en el modelo de regresión multivariable.
    """)

    df = cargar_datos()

    # ── KPIs ─────────────────────────────────────────────────────────────────
    st.subheader("Indicadores generales")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Años analizados", f"{df['anio'].min()} – {df['anio'].max()}")
    c2.metric("ANF promedio", f"{df['agua_no_facturada_pct'].mean():.2f} %")
    c3.metric("Mejor ANF (mín)", f"{df['agua_no_facturada_pct'].min():.2f} % ({df.loc[df['agua_no_facturada_pct'].idxmin(), 'anio']})")
    c4.metric("Inversión máxima", f"S/ {df['inversion_miles_soles'].max():,} miles")
    st.divider()

    # ── Dataset ───────────────────────────────────────────────────────────────
    st.subheader("Dataset — Anuario SEDAPAL 2005–2017")
    st.dataframe(df, use_container_width=True)
    st.caption("Fuente: Anuario Estadístico SEDAPAL 2017 — Gerencia de Desarrollo e Investigación.")
    st.divider()

    # ── Evolución ANF ─────────────────────────────────────────────────────────
    st.subheader("Evolución del Agua No Facturada (2005–2017)")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df["anio"], df["agua_no_facturada_pct"], "o-",
            color="#d9534f", linewidth=2.5, markersize=8)
    for _, row in df.iterrows():
        ax.annotate(f"{row['agua_no_facturada_pct']}%",
                    (row["anio"], row["agua_no_facturada_pct"]),
                    textcoords="offset points", xytext=(0, 10), fontsize=9, ha="center")
    ax.set_xlabel("Año")
    ax.set_ylabel("ANF (%)")
    ax.set_title("Tendencia del Agua No Facturada")
    ax.grid(True, linestyle="--", alpha=0.3)
    st.pyplot(fig)
    st.divider()

    # ── Matriz de correlación ─────────────────────────────────────────────────
    st.subheader("Matriz de correlación entre variables")
    st.markdown("""
    Muestra qué variables tienen mayor relación lineal con el **Agua No Facturada (ANF)**.
    Un valor cercano a **-1** indica que cuando esa variable sube, el ANF baja (relación inversa positiva para el objetivo).
    """)
    corr = df.drop("anio", axis=1).corr()
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    im = ax2.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    plt.colorbar(im, ax=ax2)
    labels = corr.columns.tolist()
    ax2.set_xticks(range(len(labels)))
    ax2.set_yticks(range(len(labels)))
    ax2.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
    ax2.set_yticklabels(labels, fontsize=8)
    for i in range(len(labels)):
        for j in range(len(labels)):
            ax2.text(j, i, f"{corr.iloc[i, j]:.2f}",
                     ha="center", va="center", fontsize=8,
                     color="white" if abs(corr.iloc[i, j]) > 0.5 else "black")
    ax2.set_title("Correlación entre variables operativas y ANF")
    st.pyplot(fig2)
    st.divider()

    # ── Dispersión variables vs ANF ────────────────────────────────────────────
    st.subheader("Relación de cada variable independiente con el ANF")
    vars_ind = ["inversion_miles_soles", "cobertura_micromedicion_pct",
                "roturas_redes", "atoros_alcantarillado", "horas_servicio_promedio"]
    labels_map = {
        "inversion_miles_soles": "Inversión (miles S/)",
        "cobertura_micromedicion_pct": "Cobertura micromedición (%)",
        "roturas_redes": "Roturas en redes",
        "atoros_alcantarillado": "Atoros en alcantarillado",
        "horas_servicio_promedio": "Horas de servicio (horas/día)"
    }

    cols = st.columns(2)
    for i, var in enumerate(vars_ind):
        with cols[i % 2]:
            fig3, ax3 = plt.subplots(figsize=(5, 3))
            ax3.scatter(df[var], df["agua_no_facturada_pct"],
                        color="#0b3d91", s=80, zorder=5)
            for _, row in df.iterrows():
                ax3.annotate(str(row["anio"]), (row[var], row["agua_no_facturada_pct"]),
                             textcoords="offset points", xytext=(5, 3), fontsize=7)
            # Línea de tendencia
            z = np.polyfit(df[var], df["agua_no_facturada_pct"], 1)
            p = np.poly1d(z)
            x_line = np.linspace(df[var].min(), df[var].max(), 100)
            ax3.plot(x_line, p(x_line), "r--", alpha=0.7)
            ax3.set_xlabel(labels_map[var], fontsize=8)
            ax3.set_ylabel("ANF (%)", fontsize=8)
            ax3.set_title(f"{labels_map[var]} vs ANF", fontsize=9)
            ax3.grid(True, linestyle="--", alpha=0.3)
            st.pyplot(fig3)
