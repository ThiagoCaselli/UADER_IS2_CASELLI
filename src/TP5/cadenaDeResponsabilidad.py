class ManejadorAbstracto(object):
    """Clase padre de todos los manejadores concretos"""
    def __init__(self, siguiente):
        self._siguiente = siguiente

    def manejar(self, solicitud):
        procesado = self.procesar_solicitud(solicitud)
        if not procesado and self._siguiente:
            self._siguiente.manejar(solicitud)

    def procesar_solicitud(self, solicitud):
        raise NotImplementedError('¡Primero debés implementar este método!')


class ManejadorPrimos(ManejadorAbstracto):
    """Consume números primos"""
    def _es_primo(self, n):
        if n < 2: return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0: return False
        return True

    def procesar_solicitud(self, solicitud):
        if self._es_primo(solicitud):
            print(f"Este es {self.__class__.__name__} procesando la solicitud '{solicitud}' (Primo)")
            return True
        return False


class ManejadorPares(ManejadorAbstracto):
    """Consume números pares"""
    def procesar_solicitud(self, solicitud):
        if solicitud % 2 == 0:
            print(f"Este es {self.__class__.__name__} procesando la solicitud '{solicitud}' (Par)")
            return True
        return False


class ManejadorPorDefecto(ManejadorAbstracto):
    """Atrapa los números que nadie pudo consumir"""
    def procesar_solicitud(self, solicitud):
        print(f"Este es {self.__class__.__name__} avisando que la solicitud '{solicitud}' NO fue consumida.")
        return True


if __name__ == "__main__":
    # Construimos la cadena: Primos -> Pares -> Por Defecto
    cadena = ManejadorPrimos(ManejadorPares(ManejadorPorDefecto(None)))

    print("--- PUNTO 1: Cadena de Responsabilidad (1 al 100) ---")
    for numero in range(1, 101):
        cadena.manejar(numero)