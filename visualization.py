import streamlit as st
import pandas as pd
import numpy as np

class Visualization:
    @staticmethod
    def mostrar_mapa_filtrado(db):
        # Obtener datos desde la base de datos
        data = db.fetch_data()

        if not data:
            st.warning("No hay datos disponibles para mostrar.")
            return

        # Crear DataFrame con las columnas necesarias
        columnas = [
            "ID", "id_categoria", "categoria_x", "subcategoria_x", "categoria_y", 
            "nombre", "anio", "estado", "subproceso_estado"
        ]

        # Convertir los datos en un DataFrame y manejar valores que falten
        df = pd.DataFrame(data)
        for columna in columnas:
            if columna not in df.columns:
                df[columna] = "Desconocido"  # Llena las columnas faltantes con un valor predeterminado
            else:
                df[columna] = df[columna].replace({np.nan: "Desconocido", None: "Desconocido"})  # Reemplaza NaN o None

        # Renombrar columnas para mostrarlas de forma clara en Streamlit
        df.rename(columns={
            "categoria_x": "Categoría X",
            "subcategoria_x": "Subcategoría X",
            "categoria_y": "Categoría Y",
            "nombre": "Nombre del Manual",
            "anio": "Año",
            "estado": "Estado",
            "subproceso_estado": "Subproceso Estado"
        }, inplace=True)

        # Formatear correctamente el año (eliminar la coma en valores numéricos)
        df["Año"] = df["Año"].astype(str).str.replace(",", "")

        # Reemplazar "Desconocido" en "Subproceso Estado" por "No Aplica"
        df["Subproceso Estado"] = df["Subproceso Estado"].replace("Desconocido", "No Aplica")

        # Eliminar las columnas "ID" y "id_categoria"
        df = df.drop(columns=["ID", "id_categoria"], errors='ignore')

        # 🔹 Agregando filtros en el menú lateral (sidebar)
        st.sidebar.header("🔍 Filtros")
        categorias_x = st.sidebar.multiselect("Filtrar por Categoría X:", df["Categoría X"].unique())
        categorias_y = st.sidebar.multiselect("Filtrar por Categoría Y:", df["Categoría Y"].unique())
        subcategorias_x = st.sidebar.multiselect("Filtrar por Subcategoría X:", df["Subcategoría X"].unique())
        años = st.sidebar.multiselect("Filtrar por Año:", sorted(df["Año"].unique(), reverse=True))
        estados = st.sidebar.multiselect("Filtrar por Estado:", df["Estado"].unique())

        # 🔹 Aplicar filtros seleccionados
        if categorias_x:
            df = df[df["Categoría X"].isin(categorias_x)]
        if categorias_y:
            df = df[df["Categoría Y"].isin(categorias_y)]
        if subcategorias_x:
            df = df[df["Subcategoría X"].isin(subcategorias_x)]
        if años:
            df = df[df["Año"].isin(años)]
        if estados:
            df = df[df["Estado"].isin(estados)]

        # 🔹 Si no hay resultados tras los filtros, mostrar mensaje
        if df.empty:
            st.warning("No se encontraron datos con los filtros aplicados.")
            return

        # 🔹 Mostrar la tabla filtrada
        st.write("### 🗺️ Mapa Doctrinario Filtrado")
        st.dataframe(df)
