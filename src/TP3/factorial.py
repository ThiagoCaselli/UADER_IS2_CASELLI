class Factorial(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Factorial, cls).__new__(cls)
        return cls._instance

    def calcular(self, n):
        if n < 0: return "Error"
        f = 1
        for i in range(1, n + 1):
            f *= i
        return f

# Verificación
f1 = Factorial()
f2 = Factorial()
print(f"¿Misma instancia?: {f1 is f2}")
print(f"Factorial de 5: {f1.calcular(5)}")