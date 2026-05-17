class Sujeto:
    """Representa al objeto que es observado"""
    def __init__(self):
        self._observadores = []

    def notificar(self):
        for observador in self._observadores:
            observador.actualizar(self)

    def adjuntar(self, observador):
        if observador not in self._observadores:
            self._observadores.append(observador)


class ExpositorId(Sujeto):
    """Monitorea y expone los IDs emitidos en el sistema"""
    def __init__(self):
        Sujeto.__init__(self)
        self._id_emitido = ''

    @property
    def id_emitido(self):
        return self._id_emitido

    @id_emitido.setter
    def id_emitido(self, valor):
        self._id_emitido = valor
        self.notificar()


# Implementación de las 4 clases observadoras con IDs específicos de 4 caracteres
class ObservadorAlfa:
    def actualizar(self, sujeto):
        if sujeto.id_emitido == "ALFA":
            print(f"   -> [Coincidencia] ObservadorAlfa reconoció su ID 'ALFA'")

class ObservadorBeta:
    def actualizar(self, sujeto):
        if sujeto.id_emitido == "BETA":
            print(f"   -> [Coincidencia] ObservadorBeta reconoció su ID 'BETA'")

class ObservadorGamma:
    def actualizar(self, sujeto):
        if sujeto.id_emitido == "GAMA":
            print(f"   -> [Coincidencia] ObservadorGamma reconoció su ID 'GAMA'")

class ObservadorDelta:
    def actualizar(self, sujeto):
        if sujeto.id_emitido == "DELT":
            print(f"   -> [Coincidencia] ObservadorDelta reconoció su ID 'DELT'")


if __name__ == "__main__":
    expositor = ExpositorId()

    expositor.adjuntar(ObservadorAlfa())
    expositor.adjuntar(ObservadorBeta())
    expositor.adjuntar(ObservadorGamma())
    expositor.adjuntar(ObservadorDelta())

    # Emitimos 8 IDs: 4 que coinciden (ALFA, BETA, GAMA, DELT) y 4 arbitrarios
    emisiones = ["ALFA", "TEST", "BETA", "TEMP", "GAMA", "FAIL", "DELT", "FINN"]

    print("--- PUNTO 3: Patrón Observador ---")
    for mid in emisiones:
        print(f"Exponiendo ID en el sistema: '{mid}'")
        expositor.id_emitido = mid