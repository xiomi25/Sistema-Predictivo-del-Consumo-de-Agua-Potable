import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.ticker import FuncFormatter


def mostrar():

    st.title("Análisis Exploratorio de Datos")

    # ------------------ CORRECCIÓN DE RUTA ------------------
    # Obtiene la ruta de la carpeta actual (paginas)
    carpeta_actual = Path(__file__).resolve().parent
    
    # Sube un nivel a Proyecto_SEDAPAL y entra a la carpeta 'datos'
    ruta = carpeta_actual.parent / "datos" / "produccion_agua.csv"

    if not ruta.exists():
        st.error(f"No se encontró el archivo en la ruta esperada: {ruta}")
        return

    df = pd.read_csv(ruta)

    #---------------------------------------------------------
    # KPIs
    #---------------------------------------------------------

    st.subheader("Indicadores Generales")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Producción Total (m³)",
            f"{df['VOLUMEN_M3'].sum():,.0f}"
        )

    with c2:
        st.metric(
            "Producción Promedio",
            f"{df['VOLUMEN_M3'].mean():,.0f}"
        )

    with c3:
        st.metric(
            "Cuencas",
            df["CUENCA"].nunique()
        )

    with c4:
        st.metric(
            "Infraestructuras",
            df["INFRAESTRUCTURA"].nunique()
        )

    st.divider()

    #---------------------------------------------------------
    # Resumen
    #---------------------------------------------------------

    st.subheader("Información del Dataset")

    tipo_dato = df.dtypes.replace({
        "int64": "Numérico (entero)",
        "float64": "Numérico (decimal)",
        "object": "Texto"
    })

    info = pd.DataFrame({
        "Variable": df.columns,
        "Tipo de dato": tipo_dato.values,
        "Valores nulos": df.isnull().sum().values
    })

    st.dataframe(info, use_container_width=True)

    st.divider()

    #---------------------------------------------------------
    # Producción por mes
    #---------------------------------------------------------

    st.subheader("Producción de Agua Potable por Mes")

    orden = ["Enero","Febrero","Marzo","Abril","Mayo",
             "Junio","Julio","Agosto","Septiembre",
             "Octubre","Noviembre","Diciembre"]

    df["MES"] = pd.Categorical(df["MES"],
                               categories=orden,
                               ordered=True)

    prod = df.groupby("MES", observed=False)["VOLUMEN_M3"].sum()

    fig, ax = plt.subplots(figsize=(10,5))

    ax.bar(prod.index.astype(str), prod.values)

    ax.set_ylabel("Volumen (m³)")

    ax.set_xlabel("Mes")

    ax.set_title("Producción Mensual")

    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda x, pos: f'{x:,.0f}')
    )

    plt.xticks(rotation=45)

    st.pyplot(fig)
    )
    
    plt.xticks(rotation=45)

    st.pyplot(fig)
