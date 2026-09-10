from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

import os
from datetime import datetime


def generar_pdf(venta, detalles):

    carpeta = "app/static/comprobantes"

    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    tipo = venta.tipo_documento.upper()

    nombre_pdf = f"{tipo}_{venta.id}.pdf"

    ruta = os.path.join(carpeta, nombre_pdf)

    pdf = canvas.Canvas(
        ruta,
        pagesize=letter
    )

    width, height = letter

    # ===== HEADER =====

    pdf.setFillColor(colors.black)
    pdf.rect(0, 740, width, 60, fill=1)

    pdf.setFillColor(colors.gold)

    pdf.setFont(
        "Helvetica-Bold",
        24
    )

    pdf.drawCentredString(
        width / 2,
        765,
        "LICORERÍA TAYTA SHANTI"
    )

    # ===== TIPO =====

    pdf.setFillColor(colors.black)

    pdf.setFont(
        "Helvetica-Bold",
        18
    )

    comprobante = (
        "BOLETA ELECTRÓNICA"
        if tipo == "DNI"
        else
        "FACTURA ELECTRÓNICA"
    )

    pdf.drawString(
        50,
        700,
        comprobante
    )

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.drawString(
        50,
        680,
        f"N°: {venta.id}"
    )

    pdf.drawString(
        180,
        680,
        f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )

    # ===== CLIENTE =====

    pdf.setFillColor(colors.gold)

    pdf.rect(
        50,
        630,
        500,
        25,
        fill=1
    )

    pdf.setFillColor(colors.black)

    pdf.setFont(
        "Helvetica-Bold",
        13
    )

    pdf.drawString(
        60,
        638,
        "DATOS DEL CLIENTE"
    )

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.drawString(
        60,
        610,
        f"Cliente: {venta.nombre_completo}"
    )

    pdf.drawString(
        60,
        590,
        f"Documento: {venta.numero_documento}"
    )

    pdf.drawString(
        60,
        570,
        f"Teléfono: {venta.telefono}"
    )

    pdf.drawString(
        60,
        550,
        f"Dirección: {venta.direccion}"
    )

    # ===== TABLA =====

    pdf.setFillColor(colors.black)

    pdf.rect(
        50,
        500,
        500,
        30,
        fill=1
    )

    pdf.setFillColor(colors.white)

    pdf.setFont(
        "Helvetica-Bold",
        11
    )

    pdf.drawString(60, 510, "Producto")
    pdf.drawString(320, 510, "Cantidad")
    pdf.drawString(450, 510, "Subtotal")

    # ===== PRODUCTOS =====

    y = 470

    pdf.setFillColor(colors.black)

    pdf.setFont(
        "Helvetica",
        11
    )

    for item in detalles:

        subtotal = item.precio * item.cantidad

        pdf.drawString(
            60,
            y,
            item.producto
        )

        pdf.drawString(
            340,
            y,
            f"x{item.cantidad}"
        )

        pdf.drawString(
            450,
            y,
            f"S/ {subtotal}"
        )

        y -= 25

    # ===== TOTAL =====

    pdf.setFillColor(colors.gold)

    pdf.rect(
        320,
        y - 20,
        230,
        40,
        fill=1
    )

    pdf.setFillColor(colors.black)

    pdf.setFont(
        "Helvetica-Bold",
        18
    )

    pdf.drawString(
        350,
        y - 5,
        f"TOTAL: S/ {venta.total}"
    )

    # ===== FOOTER =====

    pdf.setFont(
        "Helvetica",
        10
    )

    pdf.drawCentredString(
        width / 2,
        40,
        "Gracias por su compra 🍃"
    )

    pdf.save()

    return nombre_pdf