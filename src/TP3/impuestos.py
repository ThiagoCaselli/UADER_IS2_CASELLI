class CalculadorImpuestos(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CalculadorImpuestos, cls).__new__(cls)
        return cls._instance

    def calcular(self, importe):
        iva = importe * 0.21
        iibb = importe * 0.05
        muni = importe * 0.012
        return importe + iva + iibb + muni

# Prueba
calc = CalculadorImpuestos()
print(f"Total con impuestos (base 100): {calc.calcular(100)}")