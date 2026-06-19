"""Genera docs/Entrega2.pdf a partir del contenido de la Etapa 2 del TP Integrador.

Uso:
    python docs/generar_entrega2.py
"""

import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

AZUL = colors.HexColor("#2563eb")
AZUL_OSCURO = colors.HexColor("#1e3a8a")
GRIS_TEXTO = colors.HexColor("#475569")
GRIS_SUAVE = colors.HexColor("#64748b")
GRIS_BORDE = colors.HexColor("#e2e8f0")
GRIS_FONDO = colors.HexColor("#f8fafc")
VERDE = colors.HexColor("#16a34a")
NEGRO = colors.HexColor("#0f172a")

RUTA_SALIDA = os.path.join(os.path.dirname(__file__), "Entrega2.pdf")

estilos = {
    "kicker": ParagraphStyle(
        "kicker", fontName="Helvetica-Bold", fontSize=8.5, textColor=AZUL,
        spaceAfter=4, leading=11,
    ),
    "titulo": ParagraphStyle(
        "titulo", fontName="Helvetica-Bold", fontSize=20, textColor=NEGRO,
        spaceAfter=2, leading=24,
    ),
    "subtitulo": ParagraphStyle(
        "subtitulo", fontName="Helvetica", fontSize=10.5, textColor=GRIS_SUAVE,
        spaceAfter=14, leading=14,
    ),
    "seccion": ParagraphStyle(
        "seccion", fontName="Helvetica-Bold", fontSize=12.5, textColor=NEGRO,
        spaceBefore=14, spaceAfter=8, leading=15,
    ),
    "subseccion": ParagraphStyle(
        "subseccion", fontName="Helvetica-Bold", fontSize=10.5, textColor=AZUL_OSCURO,
        spaceBefore=8, spaceAfter=4, leading=13,
    ),
    "cuerpo": ParagraphStyle(
        "cuerpo", fontName="Helvetica", fontSize=9.5, textColor=GRIS_TEXTO,
        leading=14, spaceAfter=6, alignment=TA_LEFT,
    ),
    "item_ok": ParagraphStyle(
        "item_ok", fontName="Helvetica", fontSize=9.5, textColor=GRIS_TEXTO,
        leading=13.5, spaceAfter=4, leftIndent=4,
    ),
    "card_nombre": ParagraphStyle(
        "card_nombre", fontName="Helvetica-Bold", fontSize=9.5, textColor=NEGRO, leading=12,
    ),
    "card_legajo": ParagraphStyle(
        "card_legajo", fontName="Helvetica", fontSize=8.5, textColor=GRIS_SUAVE, leading=11,
    ),
    "codigo": ParagraphStyle(
        "codigo", fontName="Courier", fontSize=8, textColor=AZUL_OSCURO, leading=11,
    ),
    "footer": ParagraphStyle(
        "footer", fontName="Helvetica", fontSize=7.5, textColor=GRIS_SUAVE,
    ),
}


def encabezado_seccion(numero, titulo):
    barra = Table([[""]], colWidths=[3], rowHeights=[16])
    barra.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), AZUL)]))
    texto = Paragraph(f'<font color="#94a3b8">{numero}</font>&nbsp;&nbsp;{titulo}', estilos["seccion"])
    tabla = Table([[barra, texto]], colWidths=[6, None])
    tabla.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (0, 0), 0),
                ("LEFTPADDING", (1, 0), (1, 0), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return tabla


def caja(contenido_flowables, color_fondo=GRIS_FONDO, borde=GRIS_BORDE, padding=10):
    tabla = Table([[contenido_flowables]], colWidths=[None])
    tabla.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), color_fondo),
                ("BOX", (0, 0), (-1, -1), 0.75, borde),
                ("LEFTPADDING", (0, 0), (-1, -1), padding),
                ("RIGHTPADDING", (0, 0), (-1, -1), padding),
                ("TOPPADDING", (0, 0), (-1, -1), padding),
                ("BOTTOMPADDING", (0, 0), (-1, -1), padding),
            ]
        )
    )
    return tabla


def item(texto, estado="check"):
    marca = {
        "check": '<font color="#16a34a">&#10003;</font>',
        "pendiente": '<font color="#d97706">&#9675;</font>',
    }[estado]
    return Paragraph(f"{marca}&nbsp;&nbsp;{texto}", estilos["item_ok"])


def construir_integrantes():
    datos = [
        ("Santoro, José Joaquín", "Legajo 33647"),
        ("Aramburu, Tomás", "Legajo 34650"),
        ("Pagotto, Ignacio", "Legajo 33605"),
        ("Leguizamón, Nicolás", "Legajo 33592"),
    ]
    celdas = []
    for nombre, legajo in datos:
        contenido = [Paragraph(nombre, estilos["card_nombre"]), Paragraph(legajo, estilos["card_legajo"])]
        celdas.append(caja(contenido, padding=8))

    filas = [[celdas[0], celdas[1]], [celdas[2], celdas[3]]]
    tabla = Table(filas, colWidths=[None, None], hAlign="LEFT")
    tabla.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return tabla


def construir_pie(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(GRIS_SUAVE)
    canvas.drawString(20 * mm, 12 * mm, "Entrega 2 — Implementación y demostración")
    canvas.drawRightString(190 * mm, 12 * mm, str(doc.page))
    canvas.restoreState()


def main():
    doc = BaseDocTemplate(
        RUTA_SALIDA,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )
    marco = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    plantilla = PageTemplate(id="todas", frames=[marco], onPage=construir_pie)
    doc.addPageTemplates([plantilla])

    flujo = []

    flujo.append(Paragraph("UNIVERSIDAD TECNOLÓGICA NACIONAL · FACULTAD REGIONAL LA PLATA", estilos["kicker"]))
    flujo.append(Paragraph("Trabajo Práctico Integrador — Etapa 2", estilos["titulo"]))
    flujo.append(
        Paragraph(
            "Implementación y demostración · Comunicación de Datos 2025 · Comisión S33", estilos["subtitulo"]
        )
    )

    flujo.append(encabezado_seccion("00", "Integrantes del grupo"))
    flujo.append(Spacer(1, 6))
    flujo.append(construir_integrantes())

    flujo.append(encabezado_seccion("01", "Resumen de la entrega"))
    flujo.append(
        Paragraph(
            "A partir de la arquitectura y los mockups definidos en la Etapa 1, se desarrolló la aplicación "
            "completa: un front-end en React que consume una API REST construida con FastAPI. El back-end "
            "implementa el muestreo y la cuantización de imágenes (Pillow). Esta entrega incluye el código "
            "fuente completo, el instrumento de ejecución para que la cátedra pueda probar el desarrollo, y "
            "el enlace al video demostrativo.",
            estilos["cuerpo"],
        )
    )

    flujo.append(encabezado_seccion("02", "Funcionalidades implementadas"))
    flujo.append(Paragraph("Propuesta 3 — Digitalización de imágenes", estilos["subseccion"]))
    for texto in [
        "Carga de imágenes en alta resolución desde el navegador.",
        "Muestreo con distintos niveles de resolución (100×100, 500×500, 1000×1000), manteniendo la relación de aspecto.",
        "Reducción de profundidad de color a 1, 8 o 24 bits por canal.",
        "Comparación visual lado a lado: imagen original vs. digitalizada.",
        "Compresión del resultado (JPEG con calidad reducida) e indicador de tamaño de archivo (original vs. digitalizado, con % de reducción).",
    ]:
        flujo.append(item(texto))

    flujo.append(encabezado_seccion("03", "Código fuente"))
    flujo.append(
        Paragraph(
            "El código fuente completo se encuentra organizado en dos proyectos independientes dentro del "
            "repositorio, separando claramente front-end y back-end, y dentro de cada componente, separando "
            "JS/JSX de CSS:",
            estilos["cuerpo"],
        )
    )
    estructura = (
        "backend/app/main.py · routers/imagen.py\n"
        "backend/app/services/imagen_service.py\n"
        "backend/app/models/schemas.py\n"
        "frontend/src/App.jsx + App.css\n"
        "frontend/src/components/ImagenDigitalizador/*.jsx + *.css\n"
        "frontend/src/api/client.js\n"
        "frontend/src/styles/index.css + shared.css"
    )
    flujo.append(caja(Paragraph(estructura.replace("\n", "<br/>"), estilos["codigo"])))
    flujo.append(Spacer(1, 6))
    flujo.append(
        Paragraph(
            "Repositorio público de GitHub: <b>[COMPLETAR CON EL LINK AL REPOSITORIO]</b>",
            estilos["cuerpo"],
        )
    )

    flujo.append(encabezado_seccion("04", "Instrumento de ejecución"))
    flujo.append(
        Paragraph(
            "Para que la cátedra pueda testear el desarrollo de forma local, el repositorio incluye un "
            "<b>README.md</b> con las instrucciones detalladas. En resumen:",
            estilos["cuerpo"],
        )
    )
    flujo.append(Paragraph("Back-end (FastAPI):", estilos["subseccion"]))
    flujo.append(
        caja(
            Paragraph(
                "cd backend<br/>python -m venv venv<br/>venv\\Scripts\\activate&nbsp;&nbsp;"
                "(Windows) / source venv/bin/activate&nbsp;&nbsp;(Linux/Mac)<br/>"
                "pip install -r requirements.txt<br/>"
                "uvicorn app.main:app --reload --port 8000",
                estilos["codigo"],
            )
        )
    )
    flujo.append(Spacer(1, 6))
    flujo.append(Paragraph("Front-end (React + Vite):", estilos["subseccion"]))
    flujo.append(
        caja(
            Paragraph(
                "cd frontend<br/>npm install<br/>npm run dev",
                estilos["codigo"],
            )
        )
    )
    flujo.append(Spacer(1, 6))
    flujo.append(
        Paragraph(
            "El front-end queda disponible en http://localhost:5173 y el back-end (con documentación "
            "interactiva Swagger) en http://localhost:8000/docs. Requisitos: Python 3.10+ y Node.js 18+.",
            estilos["cuerpo"],
        )
    )

    flujo.append(encabezado_seccion("05", "Evidencia de funcionamiento"))
    flujo.append(
        Paragraph(
            "Pruebas realizadas sobre la API durante el desarrollo: para la digitalización de imágenes se "
            "probó una imagen de 800×600 px (2.7 KB); muestreada a 100×100 con 8 bits por canal y compresión "
            "activada, el resultado ocupó 1.3 KB.",
            estilos["cuerpo"],
        )
    )

    flujo.append(encabezado_seccion("06", "Video demostrativo"))
    flujo.append(
        Paragraph(
            "Enlace al video (máximo 6 minutos) que muestra el uso de las funcionalidades desarrolladas: "
            "<b>[COMPLETAR CON EL LINK AL VIDEO]</b>",
            estilos["cuerpo"],
        )
    )

    doc.build(flujo)
    print(f"PDF generado en: {RUTA_SALIDA}")


if __name__ == "__main__":
    main()
