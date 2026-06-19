from typing import Dict, List, Optional

from pydantic import BaseModel


class CodificarRequest(BaseModel):
    texto: str


class DecodificarRequest(BaseModel):
    codigo_binario: str
    codigos: Dict[str, str]


class DecodificarResponse(BaseModel):
    texto: str


class NodoArbolDTO(BaseModel):
    id: str
    frecuencia: int
    simbolo: Optional[str] = None
    izquierda: Optional["NodoArbolDTO"] = None
    derecha: Optional["NodoArbolDTO"] = None


NodoArbolDTO.model_rebuild()


class SimboloInfo(BaseModel):
    simbolo: str
    frecuencia: int
    codigo: str
    longitud: int


class CodificarResponse(BaseModel):
    metodo: str
    simbolos: List[SimboloInfo]
    arbol: Optional[NodoArbolDTO]
    codigo_binario: str
    texto_original: str
    bits_originales: int
    bits_codificados: int
    tasa_compresion: float
    longitud_promedio: float
    entropia: float


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
