import sqlite3

def verificar_estructura():
    conn = sqlite3.connect("mapa_doctrinario.db")  # Cambia el nombre si es diferente
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(manuales)")
    estructura = cursor.fetchall()

    print("Estructura de la tabla 'manuales':")
    for columna in estructura:
        print(columna)

    conn.close()

verificar_estructura()
