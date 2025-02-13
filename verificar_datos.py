import sqlite3

def verificar_datos():
    conn = sqlite3.connect("mapa_doctrinario.db")  # Cambia el nombre si es diferente
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM manuales")
    rows = cursor.fetchall()

    if not rows:
        print("No hay datos en la tabla 'manuales'.")
    else:
        print("Datos en la tabla 'manuales':")
        for row in rows:
            print(row)

    conn.close()

verificar_datos()
