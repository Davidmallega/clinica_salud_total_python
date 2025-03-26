import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os
import shutil

from modelo import (
    obtener_paciente_por_id,
    agregar_paciente,
    actualizar_paciente,
    eliminar_paciente,
    obtener_conexion,
    guardar_ficha_medica
)
from fichamedica import abrir_ficha_medica

ficha_medica_temporal = {}

def abrir_ventana_crud(id_paciente=None):
    global ficha_medica_temporal
    ficha_medica_temporal = {}

    ventana_crud = tk.Toplevel()
    ventana_crud.title("Editar Paciente" if id_paciente else "Añadir Paciente")
    ventana_crud.geometry("380x280")
    ventana_crud.attributes("-topmost", True)

    # Logo
    ruta_logo_small = os.path.join(os.path.dirname(__file__), "assets", "logo_clinica.png")
    if os.path.exists(ruta_logo_small):
        try:
            logo_small_img = Image.open(ruta_logo_small).resize((280, 60), Image.Resampling.LANCZOS)
            logo_small_tk = ImageTk.PhotoImage(logo_small_img)
            # Lo ubicamos en la fila 0, abarcando 3 columnas, para dejar espacio
            tk.Label(ventana_crud, image=logo_small_tk).grid(row=0, column=0, columnspan=3, pady=5)
            # Guardar la referencia para que Python no libere la imagen
            ventana_crud.logo_small_tk = logo_small_tk
        except Exception as e:
            print("Error cargando el logo pequeño:", e)

    carpeta_fotos = os.path.join(os.path.dirname(__file__), "assets", "fotos")
    os.makedirs(carpeta_fotos, exist_ok=True)

    paciente = obtener_paciente_por_id(id_paciente) if id_paciente else None

    campos = ["Nombre", "Edad", "Género", "Email", "Teléfono"]
    entries = {}

    for idx, campo in enumerate(campos, start=1):
        tk.Label(ventana_crud, text=f"{campo}:").grid(row=idx, column=0, padx=5, pady=5, sticky="e")
        entry = tk.Entry(ventana_crud, width=25)
        entry.grid(row=idx, column=1, padx=5, pady=5, sticky="w")
        entries[campo] = entry

    foto_actual = paciente[6] if paciente and len(paciente) > 6 else os.path.join(carpeta_fotos, "default.png")

    def cargar_preview(ruta):
        try:
            img = Image.open(ruta).resize((120,120), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print("Error al cargar preview:", e)
            return None

    preview_img = cargar_preview(foto_actual)
    foto_label = tk.Label(ventana_crud, image=preview_img)
    foto_label.grid(row=1, column=2, rowspan=5, padx=5, pady=5)

    def cambiar_foto():
        nonlocal foto_actual, preview_img
        archivo = filedialog.askopenfilename(title="Seleccionar foto", filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.gif")])
        if archivo:
            nombre_pac = entries["Nombre"].get().strip().lower().replace(" ", "_") or "paciente"
            ext = os.path.splitext(archivo)[1]
            destino = os.path.join(carpeta_fotos, f"{nombre_pac}{ext}")
            shutil.copy(archivo, destino)
            foto_actual = destino
            preview_img = cargar_preview(destino)
            foto_label.config(image=preview_img)
            foto_label.image = preview_img

    if paciente:
        datos = [paciente[1], paciente[2], paciente[3], paciente[4], paciente[5]]
        for idx, campo in enumerate(campos):
            entries[campo].insert(0, datos[idx] if datos[idx] else "")

    def guardar_temporal_ficha(datos):
        global ficha_medica_temporal
        ficha_medica_temporal = datos

    def guardar_o_actualizar():
        global ficha_medica_temporal
        valores = {campo: entries[campo].get().strip() for campo in campos}

        if not valores["Nombre"] or not valores["Edad"] or not valores["Género"]:
            messagebox.showwarning("Atención", "Los campos Nombre, Edad y Género son obligatorios.")
            return

        conexion = obtener_conexion()

        if id_paciente:
            actualizar_paciente(id_paciente, valores["Nombre"], valores["Edad"], valores["Género"], valores["Email"], valores["Teléfono"], foto_actual)
            if ficha_medica_temporal:
                guardar_ficha_medica(id_paciente, **ficha_medica_temporal)
            messagebox.showinfo("Éxito", "Paciente actualizado correctamente.")
        else:
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("""
                    INSERT INTO Pacientes (Nombre, Edad, Genero, Email, Telefono, Foto)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (valores["Nombre"], valores["Edad"], valores["Género"], valores["Email"], valores["Teléfono"], foto_actual))
                conexion.commit()
                nuevo_id = cursor.lastrowid
                cursor.close()
                conexion.close()

                if nuevo_id and ficha_medica_temporal:
                    guardar_ficha_medica(nuevo_id, **ficha_medica_temporal)
                messagebox.showinfo("Éxito", "Nuevo paciente agregado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo conectar a la base de datos.")

        ficha_medica_temporal.clear()
        ventana_crud.destroy()

    def eliminar_registro():
        if id_paciente and messagebox.askyesno("Eliminar", "¿Estás seguro de eliminar este paciente?"):
            eliminar_paciente(id_paciente)
            messagebox.showinfo("Éxito", "Paciente eliminado correctamente.")
            ventana_crud.destroy()

    btn_frame = tk.Frame(ventana_crud)
    btn_frame.grid(row=7, column=0, columnspan=3, pady=10)

    tk.Button(btn_frame, text="Cambiar Foto", command=cambiar_foto).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Ficha Médica", command=lambda: abrir_ficha_medica(id_paciente, guardar_temporal_ficha)).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Guardar" if not id_paciente else "Actualizar", fg="green", command=guardar_o_actualizar).pack(side="left", padx=5)
    if id_paciente:
        tk.Button(btn_frame, text="Eliminar", command=eliminar_registro).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Cerrar", command=ventana_crud.destroy).pack(side="left", padx=5)
