# Ejercicio 5: Patrón Builder para un Avión
class Avion:
    def __init__(self):
        self.body = None
        self.turbinas = 0
        self.alas = 0
        self.tren_aterrizaje = None

    # Este método define cómo se verá el objeto al usar print()
    def __str__(self):
        return (
            f"\n" + "="*30 + "\n"
            f"   DETALLES DEL AVIÓN\n"
            f"  " + "-"*26 + "\n"
            f"  • Cuerpo: {self.body}\n"
            f"  • Turbinas: {self.turbinas}\n"
            f"  • Alas: {self.alas}\n"
            f"  • Tren de Aterrizaje: {self.tren_aterrizaje}\n"
            f"  " + "="*30
        )

class AvionBuilder:
    def __init__(self):
        self.avion = Avion()

    def configurar_body(self, tipo):
        self.avion.body = tipo
        return self

    def agregar_turbinas(self, cantidad):
        self.avion.turbinas = cantidad
        return self

    def agregar_alas(self, cantidad):
        self.avion.alas = cantidad
        return self

    def configurar_tren(self, tipo):
        self.avion.tren_aterrizaje = tipo
        return self

    def build(self):
        return self.avion

# Uso del Builder
if __name__ == "__main__":
    builder = AvionBuilder()
    
    # Construcción paso a paso según la consigna [cite: 209]
    avion_nuevo = (builder
                   .configurar_body("Fuselaje de combate")
                   .agregar_turbinas(2)
                   .agregar_alas(2)
                   .configurar_tren("Tren de aterrizaje simple")
                   .build())
    
    print(avion_nuevo)