import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from informe import generar_informe_pdf
from modelo import obtener_pacientes
from crud import abrir_ventana_crud

root = tk.Tk()
root.title("Clínica SaludTotal - Gestión de Pacientes")
root.geometry("800x700")
root.resizable(False, False)

# Cargar logo
ruta_logo = os.path.join(os.path.dirname(__file__), "assets", "logo_clinica.png")
try:
    if os.path.exists(ruta_logo):
        logo_img = Image.open(ruta_logo).resize((450, 100), Image.Resampling.LANCZOS)
        logo_tk = ImageTk.PhotoImage(logo_img)
        tk.Label(root, image=logo_tk).pack(side="top", pady=5)
except Exception as e:
    print(f"Error cargando el logo: {e}")

style = ttk.Style(root)
style.configure("Treeview", rowheight=80)

tk.Label(root, text="Gestión de Pacientes", font=("Arial", 18, "bold")).pack(pady=5, side="top")

frame_buscar = tk.Frame(root)
frame_buscar.pack(side="top", pady=5)

tk.Label(frame_buscar, text="Buscar por nombre:").grid(row=0, column=0, padx=5)
entry_buscador = tk.Entry(frame_buscar, width=30)
entry_buscador.grid(row=0, column=1, padx=5)

def buscar_paciente():
    texto = entry_buscador.get().strip()
    actualizar_lista(filtro=texto)

tk.Button(frame_buscar, text="Buscar", command=buscar_paciente).grid(row=0, column=2, padx=5)

frame_tabla = tk.Frame(root)
frame_tabla.pack(side="top", padx=10, pady=10, fill="both", expand=True)

table_container = tk.Frame(frame_tabla)
table_container.pack(anchor="center")

scroll_y = tk.Scrollbar(table_container, orient="vertical")

tree = ttk.Treeview(
    table_container,
    columns=("ID", "Nombre", "Edad", "Género", "Email", "Teléfono"),
    show=("tree", "headings"),
    yscrollcommand=scroll_y.set,
    height=5
)
scroll_y.config(command=tree.yview)

tree.pack(side="left")
scroll_y.pack(side="left", fill="y")

tree.heading("#0", text="Foto")
tree.column("#0", width=100, anchor="center")
tree.heading("ID", text="ID")
tree.column("ID", width=30, anchor="center")
tree.heading("Nombre", text="Nombre")
tree.column("Nombre", width=100, anchor="w")
tree.heading("Edad", text="Edad")
tree.column("Edad", width=40, anchor="center")
tree.heading("Género", text="Género")
tree.column("Género", width=70, anchor="center")
tree.heading("Email", text="Email")
tree.column("Email", width=150, anchor="w")
tree.heading("Teléfono", text="Teléfono")
tree.column("Teléfono", width=80, anchor="center")

imagenes = {}

def cargar_imagen(ruta, size=(70,70)):
    try:
        img = Image.open(ruta).resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as ex:
        print(f"No se pudo cargar la imagen '{ruta}': {ex}")
        return None

def actualizar_lista(filtro=""):
    tree.delete(*tree.get_children())
    pacientes = obtener_pacientes()
    for paciente in pacientes:
        if len(paciente) < 7:
            continue
        id_pac, nombre, edad, genero, email, telefono, foto_ruta = paciente

        if filtro.lower() not in nombre.lower():
            continue

        if foto_ruta and os.path.exists(foto_ruta):
            img = cargar_imagen(foto_ruta)
        else:
            default_path = os.path.join(os.path.dirname(__file__), "assets", "fotos", "default.png")
            img = cargar_imagen(default_path) if os.path.exists(default_path) else None

        imagenes[id_pac] = img
        tree.insert(
            "",
            "end",
            text="",
            image=img,
            values=(id_pac, nombre, edad, genero, email, telefono)
        )

frame_botones = tk.Frame(root)
frame_botones.pack(side="bottom", pady=10)

def boton_nuevo():
    abrir_ventana_crud(None)

def boton_editar():
    sel = tree.selection()
    if sel:
        id_paciente = tree.item(sel, "values")[0]
        abrir_ventana_crud(int(id_paciente))

def boton_actualizar():
    actualizar_lista()

# ✅ Función final con generación y mensaje de éxito
def boton_generar_informe():
    sel = tree.selection()
    if sel:
        id_paciente = tree.item(sel, "values")[0]
        generar_informe_pdf(int(id_paciente))
        messagebox.showinfo("Informe Generado", "El informe PDF ha sido generado correctamente.")
    else:
        messagebox.showwarning("Atención", "Por favor selecciona un paciente para generar el informe.")

tk.Button(frame_botones, text="Añadir Paciente", command=boton_nuevo).grid(row=0, column=0, padx=5)
tk.Button(frame_botones, text="Editar Paciente", fg="orange", command=boton_editar).grid(row=0, column=1, padx=5)
tk.Button(frame_botones, text="Actualizar Lista", fg="green", command=boton_actualizar).grid(row=0, column=2, padx=5)
tk.Button(frame_botones, text="Generar Informe PDF", fg="blue", command=boton_generar_informe).grid(row=0, column=3, padx=5)

actualizar_lista()
root.mainloop()
