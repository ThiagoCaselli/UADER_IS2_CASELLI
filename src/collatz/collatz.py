#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* collatz.py                                                               *
#* Calcula la conjetura de Collatz para números entre 1 y 10000            *
#* y grafica las iteraciones necesarias para converger                     *
#* IS2 TP1                                                                  *
#*-------------------------------------------------------------------------*
import matplotlib.pyplot as plt

def collatz_iteraciones(n):
    """
    Calcula cuántas iteraciones tarda el número n en llegar a 1
    aplicando la conjetura de Collatz:
      - Si n es par:    n = n / 2
      - Si n es impar:  n = 3n + 1
    """
    iteraciones = 0
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        iteraciones += 1
    return iteraciones

# Calcular iteraciones para cada número entre 1 y 10000
numeros = list(range(1, 10001))
iteraciones = [collatz_iteraciones(n) for n in numeros]

# Graficar resultados
plt.figure(figsize=(14, 6))
plt.plot(iteraciones, numeros, ',', markersize=1, color='steelblue')

# Etiquetas y título
plt.title("Conjetura de Collatz — Números del 1 al 10000")
plt.xlabel("Número de iteraciones para converger")
plt.ylabel("Número n de inicio")

plt.tight_layout()
plt.show()
