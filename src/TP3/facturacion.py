from abc import ABC, abstractmethod

# Interfaz del Producto: Define la operación que todas las facturas deben implementar 
class Factura(ABC):
    @abstractmethod
    def generar_detalle(self, importe: float) -> str:
        pass

# Productos Concretos: Implementan la lógica según la condición impositiva 
class FacturaResponsable(Factura):
    def generar_detalle(self, importe: float) -> str:
        return f"Factura Tipo A (Responsable Inscripto) - Total: ${importe}"

class FacturaNoInscripto(Factura):
    def generar_detalle(self, importe: float) -> str:
        return f"Factura Tipo B (Consumidor Final/No Inscripto) - Total: ${importe}"

class FacturaExento(Factura):
    def generar_detalle(self, importe: float) -> str:
        return f"Factura Tipo C (Exento) - Total: ${importe}"

# El Factory: Centraliza la creación de los objetos sin acoplar el código cliente 
class FacturaFactory:
    @staticmethod
    def crear_factura(condicion: str) -> Factura:
        opciones = {
            "IVA Responsable": FacturaResponsable(),
            "IVA No Inscripto": FacturaNoInscripto(),
            "IVA Exento": FacturaExento()
        }
        return opciones.get(condicion, FacturaNoInscripto()) # Por defecto devuelve No Inscripto

# Código Cliente
if __name__ == "__main__":
    importe_total = 1500.0
    # Ejemplo de uso según la consigna 
    mi_factura = FacturaFactory.crear_factura("IVA Exento")
    print(mi_factura.generar_detalle(importe_total))