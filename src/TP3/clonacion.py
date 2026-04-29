class Prototipo(object):
    def __init__(self, data):
        self.data = data
    def clone(self):
        return Prototipo(self.data)

# Verificación
original = Prototipo("Datos Base")
copia_1 = original.clone()
copia_2 = copia_1.clone() # Verificación: la copia genera otra copia

print(f"Datos copia 2: {copia_2.data}")
print(f"¿Son objetos diferentes?: {copia_1 is copia_2}") # Debe ser True