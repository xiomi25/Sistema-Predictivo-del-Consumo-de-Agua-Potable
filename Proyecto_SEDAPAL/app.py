import streamlit as st
from paginas import inicio, datos, analisis, modelo, prediccion, resultados

st.set_page_config(
    page_title="SEDAPAL | Sistema Predictivo de Agua",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- ESTILO INSTITUCIONAL ----------------
st.markdown("""
<style>

.stApp {
    background-color: #f4f6f9;
    font-family: "Segoe UI", sans-serif;
    color: #1f2a37;
}

/* Sidebar institucional */
section[data-testid="stSidebar"] {
    background-color: #0b3d91;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Títulos */
h1, h2, h3 {
    color: #0b3d91;
    font-weight: 600;
}

/* Tarjetas */
[data-testid="metric-container"] {
    background-color: white;
    border-radius: 10px;
    padding: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
}

/* Botones */
.stButton>button {
    background-color: #0b3d91;
    color: white;
    border-radius: 6px;
    border: none;
}

.stButton>button:hover {
    background-color: #072c66;
}

hr {
    border: 0.5px solid #d0d7de;
}

</style>
""", unsafe_allow_html=True)

# ---------------- MENÚ ----------------
st.sidebar.title("SISTEMA SEDAPAL")

opcion = st.sidebar.radio(
    "Navegación",
    [
        "Inicio",
        "Datos",
        "Análisis",
        "Modelo Predictivo",
        "Predicción",
        "Resultados"
    ]
)

if opcion == "Inicio":
    inicio.mostrar()

elif opcion == "Datos":
    datos.mostrar()

elif opcion == "Análisis":
    analisis.mostrar()

elif opcion == "Modelo Predictivo":
    modelo.mostrar()

elif opcion == "Predicción":
    prediccion.mostrar()

elif opcion == "Resultados":
    resultados.mostrar()