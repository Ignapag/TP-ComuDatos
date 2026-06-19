from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.models.schemas import ImagenProcesarResponse
from app.services.imagen_service import procesar_imagen

router = APIRouter()

RESOLUCIONES_VALIDAS = {100, 500, 1000}
BITS_VALIDOS = {1, 8, 24}


@router.post("/procesar", response_model=ImagenProcesarResponse)
async def procesar(
    archivo: UploadFile = File(...),
    resolucion: int = Form(...),
    bits_por_canal: int = Form(...),
    comprimir: bool = Form(False),
):
    if resolucion not in RESOLUCIONES_VALIDAS:
        raise HTTPException(status_code=400, detail="Resolución inválida. Use 100, 500 o 1000")
    if bits_por_canal not in BITS_VALIDOS:
        raise HTTPException(status_code=400, detail="Bits por canal inválido. Use 1, 8 o 24")

    contenido = await archivo.read()
    if not contenido:
        raise HTTPException(status_code=400, detail="El archivo está vacío")

    try:
        return procesar_imagen(contenido, resolucion, bits_por_canal, comprimir)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"No se pudo procesar la imagen: {exc}") from exc
