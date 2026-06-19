import base64
import io
from typing import Tuple

from PIL import Image


def _redimensionar_muestreo(imagen: Image.Image, resolucion: int) -> Image.Image:
    """Reduce la imagen a una grilla de muestreo de NxN manteniendo la relación de aspecto."""
    ancho, alto = imagen.size
    if ancho >= alto:
        nuevo_ancho = resolucion
        nuevo_alto = max(1, round(resolucion * alto / ancho))
    else:
        nuevo_alto = resolucion
        nuevo_ancho = max(1, round(resolucion * ancho / alto))
    return imagen.resize((nuevo_ancho, nuevo_alto), Image.NEAREST)


def _cuantizar_bits(imagen: Image.Image, bits_por_canal: int) -> Image.Image:
    """Reduce la profundidad de color de la imagen según los bits por canal solicitados."""
    if bits_por_canal >= 24:
        return imagen.convert("RGB")
    if bits_por_canal <= 1:
        return imagen.convert("1").convert("RGB")
    if bits_por_canal == 8:
        return imagen.convert("P", palette=Image.ADAPTIVE, colors=256).convert("RGB")

    niveles = max(2, 2 ** bits_por_canal)
    factor = 255 / (niveles - 1)
    tabla_canal = [int(round(round(valor / factor) * factor)) for valor in range(256)]
    tabla = tabla_canal * 3
    return imagen.convert("RGB").point(tabla)


def _imagen_a_base64(imagen: Image.Image, formato: str, comprimido: bool) -> Tuple[str, int]:
    buffer = io.BytesIO()
    if formato == "JPEG":
        calidad = 60 if comprimido else 95
        imagen.convert("RGB").save(buffer, format="JPEG", quality=calidad, optimize=True)
    else:
        nivel = 9 if comprimido else 1
        imagen.save(buffer, format="PNG", optimize=comprimido, compress_level=nivel)
    datos = buffer.getvalue()
    return base64.b64encode(datos).decode("ascii"), len(datos)


def procesar_imagen(
    contenido: bytes,
    resolucion: int,
    bits_por_canal: int,
    comprimir: bool,
) -> dict:
    imagen_original = Image.open(io.BytesIO(contenido))
    imagen_original.load()

    tamano_original_bytes = len(contenido)
    original_b64, _ = _imagen_a_base64(imagen_original, "PNG", False)

    muestreada = _redimensionar_muestreo(imagen_original, resolucion)
    digitalizada = _cuantizar_bits(muestreada, bits_por_canal)

    formato_salida = "JPEG" if comprimir else "PNG"
    digitalizada_b64, tamano_digitalizado_bytes = _imagen_a_base64(digitalizada, formato_salida, comprimir)

    return {
        "imagen_original_base64": f"data:image/png;base64,{original_b64}",
        "imagen_digitalizada_base64": f"data:image/{formato_salida.lower()};base64,{digitalizada_b64}",
        "ancho": digitalizada.size[0],
        "alto": digitalizada.size[1],
        "tamano_original_bytes": tamano_original_bytes,
        "tamano_digitalizado_bytes": tamano_digitalizado_bytes,
        "resolucion": resolucion,
        "bits_por_canal": bits_por_canal,
        "comprimido": comprimir,
    }
