class Numero:
    def __init__(self, valor):
        self.valor = valor
    def render(self):
        return self.valor

class SumarDos(Numero):
    def __init__(self, wrapped):
        self._wrapped = wrapped
    def render(self):
        return self._wrapped.render() + 2

class MultiplicarPorDos(Numero):
    def __init__(self, wrapped):
        self._wrapped = wrapped
    def render(self):
        return self._wrapped.render() * 2

class DividirPorTres(Numero):
    def __init__(self, wrapped):
        self._wrapped = wrapped
    def render(self):
        return self._wrapped.render() / 3

# Test
base = Numero(10)
decorado = DividirPorTres(MultiplicarPorDos(SumarDos(base)))

print(f"Valor base: {base.render()}")
print(f"Resultado decorado: {decorado.render()}") # ((10 + 2) * 2) / 3 = 8