# Implementación (API/Trenes)
class Tren5mts:
    def producir(self, espesor, ancho):
        print(f"Produciendo lámina de {espesor}\" x {ancho}m en tren de 5 mts")

class Tren10mts:
    def producir(self, espesor, ancho):
        print(f"Produciendo lámina de {espesor}\" x {ancho}m en tren de 10 mts")

# Abstracción
class LaminaAcero:
    def __init__(self, tren_laminador):
        self._espesor = 0.5
        self._ancho = 1.5
        self._tren = tren_laminador

    def producir_lamina(self):
        self._tren.producir(self._espesor, self._ancho)

# Test
lamina1 = LaminaAcero(Tren5mts())
lamina1.producir_lamina()

lamina2 = LaminaAcero(Tren10mts())
lamina2.producir_lamina()