import itertools
from typing import Dict, List, Tuple

from app.services.arbol import NodoArbol


def calcular_frecuencias(texto: str) -> Dict[str, int]:
    frecuencias: Dict[str, int] = {}
    for caracter in texto:
        frecuencias[caracter] = frecuencias.get(caracter, 0) + 1
    return frecuencias


def _mejor_division(simbolos: List[Tuple[str, int]]) -> int:
    """Devuelve el índice de corte que minimiza la diferencia de frecuencias entre ambos grupos."""
    total = sum(freq for _, freq in simbolos)
    acumulado = 0
    mejor_indice = 1
    mejor_diferencia = float("inf")
    for i in range(1, len(simbolos)):
        acumulado += simbolos[i - 1][1]
        diferencia = abs((total - acumulado) - acumulado)
        if diferencia < mejor_diferencia:
            mejor_diferencia = diferencia
            mejor_indice = i
    return mejor_indice


def _construir(
    simbolos: List[Tuple[str, int]], contador: itertools.count, codigos: Dict[str, str], prefijo: str
) -> NodoArbol:
    frecuencia_total = sum(freq for _, freq in simbolos)
    nodo_id = f"sf{next(contador)}"

    if len(simbolos) == 1:
        simbolo, freq = simbolos[0]
        codigos[simbolo] = prefijo or "0"
        return NodoArbol(frecuencia=freq, simbolo=simbolo, id=nodo_id)

    indice = _mejor_division(simbolos)
    izquierda = _construir(simbolos[:indice], contador, codigos, prefijo + "0")
    derecha = _construir(simbolos[indice:], contador, codigos, prefijo + "1")
    return NodoArbol(frecuencia=frecuencia_total, izquierda=izquierda, derecha=derecha, id=nodo_id)


def construir_shannon_fano(frecuencias: Dict[str, int]) -> Tuple[NodoArbol, Dict[str, str]]:
    simbolos = sorted(frecuencias.items(), key=lambda par: (-par[1], par[0]))
    contador = itertools.count()
    codigos: Dict[str, str] = {}

    if len(simbolos) == 1:
        simbolo, freq = simbolos[0]
        codigos[simbolo] = "0"
        return NodoArbol(frecuencia=freq, simbolo=simbolo, id="sf0"), codigos

    raiz = _construir(simbolos, contador, codigos, "")
    return raiz, codigos
