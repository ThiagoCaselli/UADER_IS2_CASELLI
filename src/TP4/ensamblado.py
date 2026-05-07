class Pieza: # LeafElement
    def __init__(self, nombre):
        self.nombre = nombre
    def showDetails(self):
        print(f"\t\t- Pieza: {self.nombre}")

class Ensamblado: # CompositeElement
    def __init__(self, nombre):
        self.nombre = nombre
        self.hijos = []
    def add(self, hijo):
        self.hijos.append(hijo)
    def showDetails(self, nivel=0):
        tab = "\t" * nivel
        print(f"{tab}+ Ensamblado: {self.nombre}")
        for hijo in self.hijos:
            if isinstance(hijo, Ensamblado):
                hijo.showDetails(nivel + 1)
            else:
                hijo.showDetails()

# Construcción
producto = Ensamblado("Producto Principal")
for i in range(1, 4):
    sub = Ensamblado(f"Sub-conjunto {i}")
    for j in range(1, 5):
        sub.add(Pieza(f"P{i}.{j}"))
    producto.add(sub)

# Mostrar inicial
producto.showDetails()

# Agregar sub-conjunto opcional
opcional = Ensamblado("Sub-conjunto Opcional")
for k in range(1, 5):
    opcional.add(Pieza(f"P_Opt.{k}"))
producto.add(opcional)

print("\n--- Con sub-conjunto opcional agregado ---")
producto.showDetails()