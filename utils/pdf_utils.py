# utils/pdf_utils.py
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from reportlab.platypus import Image
from reportlab.lib.units import cm
from datetime import datetime

def generar_pdf(titulo, encabezados, filas):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    styles = getSampleStyleSheet()
    elementos = []

    logo_path = "docs/imgs/SF_LOGO.png" 

    try:
        logo = Image(logo_path)
        logo.drawHeight = 2.5*cm
        logo.drawWidth = 5.5*cm
        elementos.append(logo)
    except:
        pass


    # Título
    titulo_style = styles["Title"]
    elementos.append(Paragraph(titulo, titulo_style))
    elementos.append(Spacer(1, 20))

    # Tabla
    data = [encabezados] + filas
    tabla = Table(data)
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))

    elementos.append(tabla)
    doc.build(elementos)

    buffer.seek(0)
    return buffer
