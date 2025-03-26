from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from modelo import obtener_paciente_por_id, obtener_ficha_medica
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageOps

def hacer_bordes_redondeados(ruta_imagen, radio=25):
    """
    Aplica esquinas redondeadas a la imagen con el radio especificado.
    """
    img = Image.open(ruta_imagen).convert("RGBA")
    ancho, alto = img.size

    # Crear máscara con esquinas redondeadas
    mask = Image.new('L', (ancho, alto), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, ancho, alto], radius=radio, fill=255)

    # Aplicar la máscara
    img.putalpha(mask)

    output_path = "foto_redondeada.png"
    img.save(output_path, format="PNG")
    return output_path





def generar_informe_pdf(id_paciente):
    paciente = obtener_paciente_por_id(id_paciente)
    ficha = obtener_ficha_medica(id_paciente)

    if not paciente:
        print("Informe generado:", id_paciente)
        return

    nombre_archivo = f"informe_paciente_{id_paciente}.pdf"

    #  Elimina el archivo antes de crear el canvas
    try:
        if os.path.exists(nombre_archivo):
            os.remove(nombre_archivo)
    except PermissionError:
        print(f"El archivo {nombre_archivo} está abierto. Cierra el PDF y vuelve a intentarlo.")
        return

    c = canvas.Canvas(nombre_archivo, pagesize=A4)
    width, height = A4

    # LOGO
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo_clinica.png")
    if os.path.exists(logo_path):
        c.drawImage(logo_path, width / 2 - 6 * cm, height - 4 * cm, width=12 * cm, height=2.5 * cm, preserveAspectRatio=True)

    # TÍTULO
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height - 6.5 * cm, "INFORME CLÍNICO DEL PACIENTE")

    # DATOS PERSONALES
    cuadro_datos_x = 2 * cm
    cuadro_datos_y = height - 14 * cm
    cuadro_datos_w = 11 * cm
    cuadro_datos_h = 6 * cm
    c.setStrokeColor(colors.black)
    c.rect(cuadro_datos_x, cuadro_datos_y, cuadro_datos_w, cuadro_datos_h)

    # FOTO
    foto_path = paciente[6]
    if foto_path and os.path.exists(foto_path):
        try:
            foto_redonda = hacer_bordes_redondeados(foto_path, radio=25)
            c.drawImage(foto_redonda, cuadro_datos_x + cuadro_datos_w + 0.5 * cm, cuadro_datos_y, width=5.5 * cm, height=6 * cm, mask='auto')
        except Exception as e:
            print(f"Error al cargar la imagen con bordes redondeados: {e}")



    # Texto Datos
    c.setFont("Helvetica-Bold", 12)
    c.drawString(cuadro_datos_x + 0.5 * cm, cuadro_datos_y + cuadro_datos_h - 1 * cm, "DATOS PERSONALES")
    c.line(cuadro_datos_x + 0.5 * cm, cuadro_datos_y + cuadro_datos_h - 1.2 * cm, cuadro_datos_x + cuadro_datos_w - 0.5 * cm, cuadro_datos_y + cuadro_datos_h - 1.2 * cm)

    c.setFont("Helvetica", 11)
    texto_y = cuadro_datos_y + cuadro_datos_h - 2 * cm
    c.drawString(cuadro_datos_x + 0.7 * cm, texto_y, f"Nombre: {paciente[1]}")
    c.drawString(cuadro_datos_x + 0.7 * cm, texto_y - 0.8 * cm, f"Edad: {paciente[2]}")
    c.drawString(cuadro_datos_x + 0.7 * cm, texto_y - 1.6 * cm, f"Género: {paciente[3]}")
    c.drawString(cuadro_datos_x + 0.7 * cm, texto_y - 2.4 * cm, f"Email: {paciente[4]}")
    c.drawString(cuadro_datos_x + 0.7 * cm, texto_y - 3.2 * cm, f"Teléfono: {paciente[5]}")

    # FICHA MÉDICA
    cuadro_ficha_y = cuadro_datos_y - 10 * cm
    ficha_altura = 9 * cm
    c.rect(cuadro_datos_x, cuadro_ficha_y, width - 4 * cm, ficha_altura)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(cuadro_datos_x + 0.5 * cm, cuadro_ficha_y + ficha_altura - 1 * cm, "FICHA MÉDICA")
    c.line(cuadro_datos_x + 0.5 * cm, cuadro_ficha_y + ficha_altura - 1.2 * cm, width - 4.5 * cm, cuadro_ficha_y + ficha_altura - 1.2 * cm)

    patologias = ficha[2] if ficha else "No registradas"
    operaciones = ficha[3] if ficha else "No registradas"
    observaciones = ficha[4] if ficha else "No registradas"

    c.setFont("Helvetica", 11)
    texto_ficha_y = cuadro_ficha_y + ficha_altura - 2 * cm
    c.drawString(cuadro_datos_x + 0.7 * cm, texto_ficha_y, "Patologías:")
    c.drawString(cuadro_datos_x + 1.5 * cm, texto_ficha_y - 0.8 * cm, patologias)
    c.drawString(cuadro_datos_x + 0.7 * cm, texto_ficha_y - 2 * cm, "Operaciones:")
    c.drawString(cuadro_datos_x + 1.5 * cm, texto_ficha_y - 2.8 * cm, operaciones)
    c.drawString(cuadro_datos_x + 0.7 * cm, texto_ficha_y - 4 * cm, "Observaciones:")
    c.drawString(cuadro_datos_x + 1.5 * cm, texto_ficha_y - 4.8 * cm, observaciones)

    # PIE DE PÁGINA
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(colors.grey)
    c.drawCentredString(width / 2, 2 * cm, "Clínica SaludTotal - Informe generado automáticamente")

    fecha = datetime.now().strftime("%d/%m/%Y")
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawString(50, 700, f"Fecha de emisión: {fecha}")

    #  GUARDA EL PDF UNA SOLA VEZ
    c.save()
    print("Informe profesional generado:", nombre_archivo)
