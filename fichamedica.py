import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import os
from modelo import obtener_ficha_medica, guardar_ficha_medica

def abrir_ficha_medica(id_paciente, callback=None):
    ventana_ficha = tk.Toplevel()
    ventana_ficha.title("Ficha Médica")
    ventana_ficha.geometry("500x450")
    ventana_ficha.attributes("-topmost", True)

    # Frame principal
    frame_contenido = tk.Frame(ventana_ficha)
    frame_contenido.pack(fill="both", expand=True, padx=10, pady=10)

    # Logo en la parte superior
    ruta_logo = os.path.join(os.path.dirname(__file__), "assets", "logo_clinica.png")
    try:
        if os.path.exists(ruta_logo):
            logo_img = Image.open(ruta_logo).resize((280, 60), Image.Resampling.LANCZOS)
            logo_tk = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(frame_contenido, image=logo_tk)
            logo_label.pack(pady=5)
            logo_label.image = logo_tk  # referencia necesaria
    except Exception as e:
        print(f"Error cargando logo: {e}")

    ficha = obtener_ficha_medica(id_paciente) if id_paciente else None

    patologias_texto = ficha[2] if ficha else ""
    operaciones_texto = ficha[3] if ficha else ""
    observaciones_texto = ficha[4] if ficha else ""

    # Campos ScrolledText
    tk.Label(frame_contenido, text="Patologías:").pack(anchor="w", pady=(10,0))
    patologias_scrolled = ScrolledText(frame_contenido, width=50, height=4)
    patologias_scrolled.pack()

    patologias_scrolled.insert("1.0", patologias_texto)

    tk.Label(frame_contenido, text="Operaciones:").pack(anchor="w", pady=(10,0))
    operaciones_scrolled = ScrolledText(frame_contenido, width=50, height=4)
    operaciones_scrolled.pack()

    operaciones_scrolled.insert("1.0", operaciones_texto)

    tk.Label(frame_contenido, text="Observaciones:").pack(anchor="w", pady=(10,0))
    observaciones_scrolled = ScrolledText(frame_contenido, width=50, height=4)
    observaciones_scrolled.pack()

    observaciones_scrolled.insert("1.0", observaciones_texto)

    def guardar():
        datos_ficha = {
            "patologias": patologias_scrolled.get("1.0", tk.END).strip(),
            "operaciones": operaciones_scrolled.get("1.0", tk.END).strip(),
            "observaciones": observaciones_scrolled.get("1.0", tk.END).strip()
        }

        if id_paciente:
            guardar_ficha_medica(id_paciente, **datos_ficha)
            messagebox.showinfo("Éxito", "Ficha médica guardada correctamente.")
        else:
            if callback:
                callback(datos_ficha)
                messagebox.showinfo("Temporal", "Ficha médica guardada temporalmente.")
            else:
                messagebox.showwarning("Error", "No se puede guardar la ficha médica.")

        ventana_ficha.destroy()

    # Frame inferior para botones
    frame_botones = tk.Frame(ventana_ficha)
    frame_botones.pack(side="bottom", pady=15)

    tk.Button(frame_botones, text="Guardar",fg="green", command=guardar).pack(side="left", padx=10)
    tk.Button(frame_botones, text="Cerrar",fg="red", command=ventana_ficha.destroy).pack(side="left", padx=10)
