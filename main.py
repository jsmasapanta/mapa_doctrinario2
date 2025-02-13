import streamlit as st
from database import DatabaseManager  # Asegúrate de usar la nueva versión con Firebase
from forms import ManualForm
from visualization import Visualization
from excel_generator import ExcelGenerator

# Estilo personalizado para los colores de la interfaz
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {{
        background-color: #d9d9d9 !important;
        color: black !important;
        z-index: 2;
        box-shadow: 2px 0px 5px rgba(0, 0, 0, 0.5);
    }}
    [data-testid="stSidebar"] .css-1v3fvcr, [data-testid="stSidebar"] .css-qrbaxs {{
        font-size: 20px !important;
        color: black !important;
    }}
    [data-testid="stAppViewContainer"] {{
        background-color: #f5f5dc !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    # Configurar menú lateral
    st.sidebar.image("cede.png", use_container_width=True)
    st.sidebar.markdown("<h1>Menú</h1>", unsafe_allow_html=True)
    menu = ["Inicio", "Agregar Manual", "Ver Mapa", "Modificar Manual", "Generar Excel", "Borrar Manual"]
    choice = st.sidebar.radio("Seleccione una opción:", menu)

    # 🔹 CORREGIDO: Inicializar DatabaseManager sin parámetros
    db = DatabaseManager()

    # Navegar entre las opciones
    if choice == "Inicio":
        st.title("🏠 Bienvenido al Mapa Doctrinario del Ejército")
        st.write("Usa el menú de la izquierda para navegar por las opciones.")
    elif choice == "Agregar Manual":
        st.title("➕ Agregar Manual")
        ManualForm.agregar_manual_form(db)
    elif choice == "Ver Mapa":
        st.title("🗺️ Mapa Doctrinario Filtrado")
        Visualization.mostrar_mapa_filtrado(db)
    elif choice == "Modificar Manual":
        st.title("✏️ Modificar Manual")
        manual_id = st.text_input("ID del Manual a Modificar:")
        if manual_id:
            ManualForm.modificar_manual_form(db, manual_id)
    elif choice == "Generar Excel":
        st.title("📊 Generar Excel")
        st.write("Selecciona las opciones de filtro antes de generar el archivo Excel.")
        ExcelGenerator.generar_excel_filtrado(db)
    elif choice == "Borrar Manual":
        st.title("🗑️ Borrar Manual")
        ManualForm.borrar_manual_form(db)

if __name__ == "__main__":
    main()
