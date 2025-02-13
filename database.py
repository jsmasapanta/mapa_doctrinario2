import firebase_admin
from firebase_admin import credentials, db

class DatabaseManager:
    def __init__(self, cred_file, db_url):
        if not firebase_admin._apps:  # Verifica si Firebase ya está inicializado
            cred = credentials.Certificate(cred_file)
            firebase_admin.initialize_app(cred, {"databaseURL": db_url})
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
        
        # Si los datos están vacíos, devuelve una lista vacía
        if not datos:
            return []

        # Si los datos son un diccionario, procesarlos normalmente
        if isinstance(datos, dict):
            return [{"id": key, **value} for key, value in datos.items()]

        # Si los datos son una lista, procesarlos como lista
        if isinstance(datos, list):
            return [{"id": idx, **value} for idx, value in enumerate(datos) if value]  # Filtra valores vacíos

        # Si los datos no son ni un diccionario ni una lista, lanza una excepción
        raise TypeError("Formato inesperado de los datos en Firebase.")


    def fetch_manual_by_id(self, manual_id):
        """
        Obtiene un manual específico por su ID.
        """
        manual = self.ref.child(str(manual_id)).get()
        if manual:
            return manual  # Devuelve el manual como un diccionario
        return None


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
        # Convierte el manual_id a string para buscarlo como clave en Firebase
        manual_id_str = str(manual_id)
        
        # Busca el manual en la base de datos
        manual_ref = self.ref.child(manual_id_str)
        if manual_ref.get():
            # Si existe, lo elimina
            manual_ref.delete()
            return True
        return False


