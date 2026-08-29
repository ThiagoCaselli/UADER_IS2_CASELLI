import numpy as np
import matplotlib.pyplot as plt

# 1. Cálculo y gráfico del Esfuerzo (E) basado en Tamaño (S)
# Se crea un rango de valores para S desde 0 hasta 10000
S = np.linspace(0, 10000, 500)
E = 8 * (S ** 0.95)

plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.plot(S, E, color='blue')
plt.title('Esfuerzo vs Tamaño')
plt.xlabel('Tamaño de Proyecto (S)')
plt.ylabel('Esfuerzo (E)')

# 2. Cálculo y gráfico del Tiempo (td) basado en Esfuerzo (E)
# Se crea un rango de valores para E desde 1 hasta 500
E_val = np.linspace(1, 500, 500)
td = 2.4 * (E_val ** 0.33)

plt.subplot(1, 2, 2)
plt.plot(E_val, td, color='red')
plt.title('Tiempo vs Esfuerzo')
plt.xlabel('Esfuerzo (E)')
plt.ylabel('Tiempo calendario (td)')
plt.tight_layout()
plt.show()