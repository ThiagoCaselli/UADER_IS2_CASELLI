from abc import ABC, abstractmethod

class Hamburguesa(ABC):
    @abstractmethod
    def entregar(self): pass

class Mostrador(Hamburguesa):
    def entregar(self): return "Entrega en Mostrador"

class Retiro(Hamburguesa):
    def entregar(self): return "Retiro por Cliente"

class Delivery(Hamburguesa):
    def entregar(self): return "Envío por Delivery"

class HamburguesaFactory:
    @staticmethod
    def crear(metodo):
        if metodo == "mostrador": return Mostrador()
        if metodo == "retiro": return Retiro()
        if metodo == "delivery": return Delivery()

# Uso
pedido = HamburguesaFactory.crear("delivery")
print(pedido.entregar())