import mysql.connector

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Rafaela13",
            database="bd_saludtotal"
        )
        return conexion
    except mysql.connector.Error as error:
        print(f"Error al conectar a la base de datos: {error}")
        return None
