#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* factorial_OOP.py                                                         *
#* Calcula el factorial de un rango de números usando POO                  *
#* Dr.P.E.Colla (c) 2022 - Modificado para IS2 TP1                        *
#* Creative commons                                                         *
#*-------------------------------------------------------------------------*
import sys

class Factorial:
    """Clase que encapsula la lógica de cálculo de factorial."""

    def __init__(self):
        """Constructor de la clase Factorial."""
        pass

    def calcular(self, num):
        """Calcula el factorial de un número entero no negativo."""
        if num < 0:
            print("Factorial de un número negativo no existe")
            return 0
        elif num == 0:
            return 1
        else:
            fact = 1
            while num > 1:
                fact *= num
                num -= 1
            return fact

    def run(self, min, max):
        """Calcula e imprime los factoriales entre min y max inclusive."""
        for n in range(min, max + 1):
            print(f"Factorial {n}! es {self.calcular(n)}")


def procesar_rango(argumento):
    """
    Interpreta el argumento como número simple o rango (desde-hasta).
    Soporta:
      - "10"    -> factorial de 10
      - "4-8"   -> factoriales del 4 al 8
      - "-10"   -> factoriales del 1 al 10
      - "4-"    -> factoriales del 4 al 60
    """
    # Instancia de la clase Factorial
    f = Factorial()

    # Caso: rango sin límite inferior, ej: "-10"
    if argumento.startswith("-"):
        hasta = int(argumento[1:])
        f.run(1, hasta)

    # Caso: rango sin límite superior, ej: "4-"
    elif argumento.endswith("-"):
        desde = int(argumento[:-1])
        f.run(desde, 60)

    # Caso: rango completo, ej: "4-8"
    elif "-" in argumento:
        partes = argumento.split("-")
        f.run(int(partes[0]), int(partes[1]))

    # Caso: número simple, ej: "10"
    else:
        f.run(int(argumento), int(argumento))


# Si no se pasa argumento, solicitarlo al usuario
if len(sys.argv) < 2:
    argumento = input("Ingrese un número o rango (ej: 10, 4-8, -10, 4-): ")
else:
    argumento = sys.argv[1]

# Procesar el argumento recibido
procesar_rango(argumento)
