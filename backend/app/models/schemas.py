from pydantic import BaseModel


class ImagenProcesarResponse(BaseModel):
    imagen_original_base64: str
    imagen_digitalizada_base64: str
    ancho: int
    alto: int
    tamano_original_bytes: int
    tamano_digitalizado_bytes: int
    resolucion: int
    bits_por_canal: int
    comprimido: bool
