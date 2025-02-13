import firebase_admin
from firebase_admin import credentials, db
import streamlit as st
import json

class DatabaseManager:
    def __init__(self):
        # Cargar las credenciales desde Streamlit Secrets
        firebase_secrets = st.secrets["firebase_credenciales"]

        
        if not firebase_admin._apps:  # Verifica si Firebase ya está inicializado
            cred = credentials.Certificate(dict(firebase_secrets))

            firebase_admin.initialize_app(cred, {"databaseURL": "https://mapa-doctrinario-default-rtdb.firebaseio.com/"})
        
        self.ref = db.reference("manuales")

    def add_manual(self, manual_id, categoria_x, subcategoria_x, categoria_y, nombre, anio, estado, subproceso_estado, id_categoria=0):
        """
        Agrega un manual a Firebase. Si manual_id es None, se generará automáticamente.
        """
        nuevo_manual = {
            "id": manual_id,
            "categoria_x": categoria_x,
            "subcategoria_x": subcategoria_x,
            "categoria_y": categoria_y,
            "nombre": nombre,
            "anio": anio,
            "estado": estado,
            "subproceso_estado": subproceso_estado,
            "id_categoria": id_categoria
        }
        if manual_id:  # Si se especifica un ID manual, usa ese como clave
            self.ref.child(str(manual_id)).set(nuevo_manual)
        else:  # Genera automáticamente una clave
            self.ref.push(nuevo_manual)

    def fetch_data(self):
        """
        Obtiene todos los manuales almacenados en Firebase.
        """
        datos = self.ref.get()
        
        if not datos:  # Si los datos están vacíos, devuelve una lista vacía
            return []

        if isinstance(datos, dict):  # Si los datos son un diccionario, procesarlos normalmente
            return [{"id": key, **value} for key, value in datos.items()]

        if isinstance(datos, list):  # Si los datos son una lista, procesarlos como lista
            return [{"id": idx, **value} for idx, value in enumerate(datos) if value]  # Filtra valores vacíos

        raise TypeError("Formato inesperado de los datos en Firebase.")  # Si los datos tienen un formato desconocido

    def fetch_manual_by_id(self, manual_id):
        """
        Obtiene un manual específico por su ID.
        """
        manual = self.ref.child(str(manual_id)).get()
        return manual if manual else None  # Devuelve el manual como un diccionario o None si no existe

    def update_manual(self, manual_id, categoria_x, subcategoria_x, categoria_y, nombre, anio, estado, subproceso_estado):
        """
        Actualiza un manual existente en Firebase.
        """
        updated_data = {
            "categoria_x": categoria_x,
            "subcategoria_x": subcategoria_x,
            "categoria_y": categoria_y,
            "nombre": nombre,
            "anio": anio,
            "estado": estado,
            "subproceso_estado": subproceso_estado
        }
        self.ref.child(str(manual_id)).update(updated_data)

    def delete_manual(self, manual_id):
        """
        Elimina un manual por su ID.
        """
        manual_ref = self.ref.child(str(manual_id))
        if manual_ref.get():
            manual_ref.delete()  # Si existe, lo elimina
            return True
        return False
