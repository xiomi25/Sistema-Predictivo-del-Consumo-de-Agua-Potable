import streamlit as st
from pathlib import Path
from paginas import inicio, datos, analisis, modelo, prediccion, resultados

st.set_page_config(
    page_title="SEDAPAL | Sistema Predictivo de Agua",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- ESTILO INSTITUCIONAL ----------------
st.markdown("""
<style>

/* Contenedores principales */
.stApp, [data-testid="stAppViewContainer"] {
    background-color: #f4f6f9 !important;
    font-family: "Segoe UI", sans-serif;
}

/* Forzar color oscuro en textos generales contra modo nocturno de móviles */
.stApp p, .stApp span, .stApp label, .stApp li {
    color: #1f2a37 !important;
}

/* Sidebar institucional */
section[data-testid="stSidebar"] {
    background-color: #0b3d91 !important;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Títulos con máxima prioridad */
h1, h2, h3, h4, h5, h6,
.stApp h1, .stApp h2, .stApp h3,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 {
    color: #0b3d91 !important;
    font-weight: 600;
}

/* Tarjetas */
[data-testid="metric-container"] {
    background-color: white !important;
    border-radius: 10px;
    padding: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08) !important;
}

/* Textos internos de métricas */
[data-testid="stMetricLabel"] div, [data-testid="stMetricValue"] div {
    color: #1f2a37 !important;
}

/* Botones */
.stButton>button {
    background-color: #0b3d91 !important;
    color: white !important;
    border-radius: 6px;
    border: none;
}

.stButton>button:hover {
    background-color: #072c66 !important;
}

hr {
    border: 0.5px solid #d0d7de !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOGO DE SEDAPAL ----------------
raiz_proyecto = Path(__file__).resolve().parent
ruta_logo = raiz_proyecto / "assets" / "logo_sedapal.png"

if ruta_logo.exists():
    st.sidebar.image(str(ruta_logo), use_container_width=True)
else:
    pass

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
