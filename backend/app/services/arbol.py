from dataclasses import dataclass
from typing import Optional


@dataclass
class NodoArbol:
    """Nodo binario compartido por Huffman y Shannon-Fano para construir el árbol de códigos."""

    frecuencia: int
    id: str
    simbolo: Optional[str] = None
    izquierda: Optional["NodoArbol"] = None
    derecha: Optional["NodoArbol"] = None

    def a_dict(self) -> dict:
        return {
            "id": self.id,
            "frecuencia": self.frecuencia,
            "simbolo": self.simbolo,
            "izquierda": self.izquierda.a_dict() if self.izquierda else None,
            "derecha": self.derecha.a_dict() if self.derecha else None,
        }
