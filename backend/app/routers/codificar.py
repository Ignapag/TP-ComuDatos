import math
from typing import Dict

from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    CodificarRequest,
    CodificarResponse,
    DecodificarRequest,
    DecodificarResponse,
    SimboloInfo,
)
from app.services import huffman, shannon_fano

router = APIRouter()


def _calcular_metricas(texto: str, frecuencias: Dict[str, int], codigos: Dict[str, str]):
    total_caracteres = len(texto)
    bits_originales = total_caracteres * 8
    bits_codificados = sum(len(codigos[c]) for c in texto)

    tasa_compresion = 0.0
    if bits_originales > 0:
        tasa_compresion = round((1 - bits_codificados / bits_originales) * 100, 2)

    longitud_promedio = 0.0
    if total_caracteres > 0:
        longitud_promedio = round(
            sum(frecuencias[s] * len(codigos[s]) for s in frecuencias) / total_caracteres, 3
        )

    entropia = 0.0
    if total_caracteres > 0:
        for freq in frecuencias.values():
            p = freq / total_caracteres
            entropia -= p * math.log2(p)
        entropia = round(entropia, 3)

    return bits_originales, bits_codificados, tasa_compresion, longitud_promedio, entropia


def _construir_simbolos(frecuencias: Dict[str, int], codigos: Dict[str, str]):
    return sorted(
        (
            SimboloInfo(simbolo=s, frecuencia=f, codigo=codigos[s], longitud=len(codigos[s]))
            for s, f in frecuencias.items()
        ),
        key=lambda info: (-info.frecuencia, info.simbolo),
    )


@router.post("/huffman", response_model=CodificarResponse)
def codificar_huffman(payload: CodificarRequest):
    texto = payload.texto
    if not texto:
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío")

    frecuencias = huffman.calcular_frecuencias(texto)
    arbol = huffman.construir_arbol_huffman(frecuencias)
    codigos = huffman.generar_codigos(arbol)

    bits_originales, bits_codificados, tasa, longitud_prom, entropia = _calcular_metricas(
        texto, frecuencias, codigos
    )

    return CodificarResponse(
        metodo="huffman",
        simbolos=_construir_simbolos(frecuencias, codigos),
        arbol=arbol.a_dict(),
        codigo_binario="".join(codigos[c] for c in texto),
        texto_original=texto,
        bits_originales=bits_originales,
        bits_codificados=bits_codificados,
        tasa_compresion=tasa,
        longitud_promedio=longitud_prom,
        entropia=entropia,
    )


@router.post("/shannon-fano", response_model=CodificarResponse)
def codificar_shannon_fano(payload: CodificarRequest):
    texto = payload.texto
    if not texto:
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío")

    frecuencias = shannon_fano.calcular_frecuencias(texto)
    arbol, codigos = shannon_fano.construir_shannon_fano(frecuencias)

    bits_originales, bits_codificados, tasa, longitud_prom, entropia = _calcular_metricas(
        texto, frecuencias, codigos
    )

    return CodificarResponse(
        metodo="shannon-fano",
        simbolos=_construir_simbolos(frecuencias, codigos),
        arbol=arbol.a_dict(),
        codigo_binario="".join(codigos[c] for c in texto),
        texto_original=texto,
        bits_originales=bits_originales,
        bits_codificados=bits_codificados,
        tasa_compresion=tasa,
        longitud_promedio=longitud_prom,
        entropia=entropia,
    )


@router.post("/decodificar", response_model=DecodificarResponse)
def decodificar(payload: DecodificarRequest):
    codigos_invertidos = {codigo: simbolo for simbolo, codigo in payload.codigos.items()}
    texto = []
    buffer = ""
    for bit in payload.codigo_binario:
        buffer += bit
        if buffer in codigos_invertidos:
            texto.append(codigos_invertidos[buffer])
            buffer = ""
    if buffer:
        raise HTTPException(status_code=400, detail="Código binario inválido o incompleto")
    return DecodificarResponse(texto="".join(texto))
