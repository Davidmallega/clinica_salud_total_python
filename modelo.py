# modelo.py
from conexion import obtener_conexion
import mysql.connector

def agregar_paciente(nombre, edad, genero, email, telefono, foto):
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                INSERT INTO Pacientes (Nombre, Edad, Genero, Email, Telefono, Foto)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (nombre, edad, genero, email, telefono, foto))
            conexion.commit()
            print("Paciente agregado correctamente (con foto).")
        except mysql.connector.Error as error:
            print(f"Error al agregar paciente: {error}")
        finally:
            cursor.close()
            conexion.close()

def obtener_pacientes():
    conexion = obtener_conexion()
    pacientes = []
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Pacientes")
            pacientes = cursor.fetchall()
        except mysql.connector.Error as error:
            print(f"Error al obtener pacientes: {error}")
        finally:
            cursor.close()
            conexion.close()
    return pacientes

def obtener_paciente_por_id(id_paciente):
    conexion = obtener_conexion()
    paciente = None
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM Pacientes WHERE ID = %s", (id_paciente,))
            paciente = cursor.fetchone()
        except mysql.connector.Error as error:
            print(f"Error al obtener paciente por ID: {error}")
        finally:
            cursor.close()
            conexion.close()
    return paciente

def actualizar_paciente(id_paciente, nombre, edad, genero, email, telefono, foto):
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            sql = """
                UPDATE Pacientes
                SET Nombre = %s, Edad = %s, Genero = %s,
                    Email = %s, Telefono = %s, Foto = %s
                WHERE ID = %s
            """
            cursor.execute(sql, (nombre, edad, genero, email, telefono, foto, id_paciente))
            conexion.commit()
            print("Paciente actualizado correctamente (con foto).")
        except mysql.connector.Error as error:
            print(f"Error al actualizar paciente: {error}")
        finally:
            cursor.close()
            conexion.close()

def eliminar_paciente(id_paciente):
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM Pacientes WHERE ID = %s", (id_paciente,))
            conexion.commit()
            print("Paciente eliminado correctamente.")
        except mysql.connector.Error as error:
            print(f"Error al eliminar paciente: {error}")
        finally:
            cursor.close()
            conexion.close()

def obtener_ficha_medica(id_paciente):
    conexion = obtener_conexion()
    ficha = None
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM FichaMedica WHERE PacienteID = %s", (id_paciente,))
            ficha = cursor.fetchone()
        except mysql.connector.Error as error:
            print(f"Error al obtener ficha médica: {error}")
        finally:
            cursor.close()
            conexion.close()
    return ficha

def guardar_ficha_medica(id_paciente, patologias, operaciones, observaciones):
    conexion = obtener_conexion()
    if conexion:
        try:
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO FichaMedica (PacienteID, Patologias, Operaciones, Observaciones)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    Patologias = VALUES(Patologias),
                    Operaciones = VALUES(Operaciones),
                    Observaciones = VALUES(Observaciones)
            """, (id_paciente, patologias, operaciones, observaciones))
            conexion.commit()
            print("Ficha médica guardada correctamente.")
        except mysql.connector.Error as error:
            print(f"Error al guardar ficha médica: {error}")
        finally:
            cursor.close()
            conexion.close()