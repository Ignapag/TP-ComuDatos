import heapq
import itertools
from typing import Dict, Optional

from app.services.arbol import NodoArbol


def calcular_frecuencias(texto: str) -> Dict[str, int]:
    frecuencias: Dict[str, int] = {}
    for caracter in texto:
        frecuencias[caracter] = frecuencias.get(caracter, 0) + 1
    return frecuencias


def construir_arbol_huffman(frecuencias: Dict[str, int]) -> NodoArbol:
    contador = itertools.count()
    heap = []
    for simbolo, freq in frecuencias.items():
        nodo = NodoArbol(frecuencia=freq, simbolo=simbolo, id=f"h{next(contador)}")
        heapq.heappush(heap, (freq, nodo.id, nodo))

    if len(heap) == 1:
        _, _, unico = heap[0]
        return NodoArbol(frecuencia=unico.frecuencia, izquierda=unico, id=f"h{next(contador)}")

    while len(heap) > 1:
        freq_a, _, nodo_a = heapq.heappop(heap)
        freq_b, _, nodo_b = heapq.heappop(heap)
        nuevo = NodoArbol(
            frecuencia=freq_a + freq_b,
            izquierda=nodo_a,
            derecha=nodo_b,
            id=f"h{next(contador)}",
        )
        heapq.heappush(heap, (nuevo.frecuencia, nuevo.id, nuevo))

    return heap[0][2]


def generar_codigos(
    nodo: Optional[NodoArbol], prefijo: str = "", codigos: Optional[Dict[str, str]] = None
) -> Dict[str, str]:
    if codigos is None:
        codigos = {}
    if nodo is None:
        return codigos
    if nodo.simbolo is not None:
        codigos[nodo.simbolo] = prefijo or "0"
        return codigos
    generar_codigos(nodo.izquierda, prefijo + "0", codigos)
    generar_codigos(nodo.derecha, prefijo + "1", codigos)
    return codigos
