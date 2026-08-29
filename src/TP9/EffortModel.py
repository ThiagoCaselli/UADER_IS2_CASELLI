
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
#* EffortModel
#* Programa para procesar modelos lineales mediante correlación por cuadrados mínimos
#* 
#* UADER - FCyT
#* Ingeniería de Software II
#*
#* Dr. Pedro E. Colla
#* copyright (c) 2023,2024
#*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
import numpy as np
import pandas as pd
import argparse
import statsmodels.api as sm
import sys
import os
import matplotlib.pyplot as plt
#*------------------------------------------------------------------------------------------------
#* Almacena dataset histórico
#*------------------------------------------------------------------------------------------------
data = {
    'LOC': [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000],
    'Esfuerzo': [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
}

#*------------------------------------------------------------------------------------------------
#* Inicialización del programa
#*------------------------------------------------------------------------------------------------
version="7.0"
linear=False
exponential=False
os.system('clear')
#*------------------------------------------------------------------------------------------------
#* Procesa argumentos
#*------------------------------------------------------------------------------------------------
# Construct the argument parser
ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument("-v", "--version",required=False,help="version",action="store_true")
ap.add_argument("-x", "--exponential", required=False,help="Exponential model",action="store_true")
ap.add_argument("-l", "--linear", required=False,help="Linear model",action="store_true")
args = vars(ap.parse_args())

if args['version'] == True:
   print("Program %s version %s" % (sys.argv[0],version))
   sys.exit(0)

if args['linear'] == True:
   print("Program %s version %s" % (sys.argv[0],version))
   print("Linear correlation model selected")
   linear=True

if args['exponential'] == True:
   print("Program %s version %s" % (sys.argv[0],version))
   print("Exponential correlation model selected")
   exponential=True

if linear==False and exponential==False:
   print("Program %s version %s" % (sys.argv[0],version))
   print("Debe indicar modelo lineal (-l) o exponencial (-x) o ambos")

#*-----------------------------------------------------------------------------------------------
#* Definir dataset y procesar corrlación entre LOC (complejidad) y Esfuerzo (PM)
#*-----------------------------------------------------------------------------------------------
df = pd.DataFrame(data)
correlation = df['LOC'].corr(df['Esfuerzo'])

#*------------------------------------------------------------------------------------------------
#* Procesa modelo lineal, usa numpy polyfit()
#*------------------------------------------------------------------------------------------------

if linear==True:

   a, b = np.polyfit(df['LOC'], df['Esfuerzo'], 1)
   R = np.corrcoef(df['LOC'], df['Esfuerzo'], 1)
   R2=R*R
   r_value=R2[1][0]

   print("Modelo lineal E=%.6f + %.6f*LOC)" % (b,a))
   print("El R-squared=%.4f (lineal)" % (r_value))

   lbl=("modelo lineal (R-Sq=%.2f)" % (r_value))
   plt.plot(df['LOC'], a*df['LOC']+b,label=lbl,color='red')

#*------------------------------------------------------------------------------------------------
#* procesa modelo exponencial utiliza OLS fit()
#*------------------------------------------------------------------------------------------------
if exponential==True:
   df['logEsfuerzo']=np.log(df['Esfuerzo'])
   df['logLOC']=np.log(df['LOC'])

   X = df['logLOC']
   Y = df['logEsfuerzo']
   X = sm.add_constant(X)  # Añadir una constante para el intercepto

   mx= sm.OLS(Y, X).fit()
   print(mx.summary())

   k=np.exp(mx.params['const'])
   b=mx.params['logLOC']

   print("Modelo exponencial E=%.6f*(LOC^%.6f)" % (k,b))
   print("El R-squared=%.2f (exponencial)" % (mx.rsquared))

   lbl=("modelo exponencial (R-Sq=%.2f)" % (mx.rsquared))
   plt.plot(df['LOC'], k*(df['LOC']**b),label=lbl,color='green')

#*------------------------------------------------------------------------------------------------
#* Hace plot del dataset histórico
#*------------------------------------------------------------------------------------------------

plt.scatter(df['LOC'], df['Esfuerzo'], label='Datos históricos')
plt.xlabel('Complejidad [LOC]')
plt.ylabel('Esfuerzo (persona-mes)')
plt.legend()
# --- Resolución Punto 9.c ---
loc_nuevo = 200
# Usamos la misma fórmula exponencial de la consola:
esfuerzo_nuevo = 0.000368 * (loc_nuevo ** 1.207561)
print(f"--> El esfuerzo estimado para {loc_nuevo} LOC es: {esfuerzo_nuevo:.2f} PM")

# Agregamos el punto al gráfico en color rojo y más grande para que se note
plt.scatter(loc_nuevo, esfuerzo_nuevo, color='red', s=100, zorder=5, label='Proyecto 200 LOC')
# Actualizamos la leyenda
plt.legend()
plt.show()

