from __future__ import annotations
from collections.abc import Iterable, Iterator

class IteradorCaracteres(Iterator):
    """Iterador concreto adaptado para recorrer caracteres"""
    def __init__(self, coleccion: ColeccionCadena, inverso: bool = False) -> None:
        self._coleccion = coleccion
        self._inverso = inverso
        self._posicion = len(coleccion._lista_caracteres) - 1 if inverso else 0

    def __next__(self):
        try:
            valor = self._coleccion._lista_caracteres[self._posicion]
            self._posicion += -1 if self._inverso else 1
        except IndexError:
            raise StopIteration()
        return valor


class ColeccionCadena(Iterable):
    """Colección concreta que almacena el texto como lista de caracteres"""
    def __init__(self, texto: str) -> None:
        self._lista_caracteres = list(texto)

    def __iter__(self) -> IteradorCaracteres:
        return IteradorCaracteres(self, False)

    def obtener_iterador_inverso(self) -> IteradorCaracteres:
        return IteradorCaracteres(self, True)


if __name__ == "__main__":
    texto = "UADER-FCYT"
    coleccion = ColeccionCadena(texto)

    print("--- PUNTO 2: Iterador sobre Cadena ---")
    print(f"Texto original: {texto}\n")

    print("Recorrido directo:")
    print(" -> ".join(coleccion))
    print("")

    print("Recorrido inverso:")
    print(" -> ".join(coleccion.obtener_iterador_inverso()))