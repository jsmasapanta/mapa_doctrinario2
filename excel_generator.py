import streamlit as st
import pandas as pd
from io import BytesIO
import numpy as np

class ExcelGenerator:
    @staticmethod
    def generar_excel_filtrado(db):
        # Obtener datos desde la base de datos
        data = db.fetch_data()

        # Definir las columnas necesarias
        columnas = [
            "ID", "id_categoria", "categoria_x", "subcategoria_x", "categoria_y", 
            "nombre", "anio", "estado", "subproceso_estado"
        ]

        try:
            # Convertir los datos a un DataFrame
            df = pd.DataFrame(data)

            # Asegurarse de que todas las columnas existan y manejar valores que falten
            for columna in columnas:
                if columna not in df.columns:
                    df[columna] = "Desconocido"  # Llena las columnas faltantes con un valor predeterminado
                else:
                    df[columna] = df[columna].replace({np.nan: "Desconocido", None: "Desconocido"})  # Reemplaza NaN o None

            # Renombrar columnas para que sean claras en el Excel
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

        except ValueError:
            st.error("Error al procesar los datos: las columnas no coinciden con los datos.")
            return

        if df.empty:
            st.warning("No hay datos disponibles para generar el Excel.")
            return

        # Agregar filtros en la interfaz
        categorias_x = st.multiselect("Filtrar por Categoría X:", df["Categoría X"].unique())
        categorias_y = st.multiselect("Filtrar por Categoría Y:", df["Categoría Y"].unique())
        subcategorias_x = st.multiselect("Filtrar por Subcategoría X:", df["Subcategoría X"].unique())
        años = st.multiselect("Filtrar por Año:", sorted(df["Año"].unique()))
        estados = st.multiselect("Filtrar por Estado:", df["Estado"].unique())

        # Aplicar los filtros seleccionados
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

        if df.empty:
            st.warning("No se encontraron datos con los filtros aplicados.")
            return

        # Generar el archivo Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Manuales")
            workbook = writer.book
            worksheet = writer.sheets["Manuales"]

            # Ajustar el ancho de las columnas automáticamente
            for column in df:
                col_idx = df.columns.get_loc(column)  # Obtener el índice de la columna
                max_len = df[column].astype(str).map(len).max() + 2  # Calcular el ancho
                worksheet.set_column(col_idx, col_idx, max_len)  # Ajustar el ancho

        # Botón de descarga para el archivo Excel
        st.download_button(
            label="📥 Descargar Excel",
            data=output.getvalue(),
            file_name="manuales_filtrados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
