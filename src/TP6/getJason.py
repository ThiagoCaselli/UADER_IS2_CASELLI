import json
import sys

# Definimos el archivo de origen de forma fija
jsonfile = 'sitedata.json'

# Definimos la clave por defecto
jsonkey = 'token1'

# Si el usuario escribe un argumento en la consola, actualizamos la clave
if len(sys.argv) > 1:
    jsonkey = sys.argv[1]

try:
    # Abrimos el archivo en modo lectura
    with open(jsonfile, 'r') as myfile:
        data = myfile.read()
    
    # Convertimos el texto del archivo a un objeto de Python
    obj = json.loads(data)
    
    # Verificamos si la clave existe en el archivo y la mostramos
    if jsonkey in obj:
        print(str(obj[jsonkey]))
    else:
        print(f"Error: La clave '{jsonkey}' no existe en {jsonfile}.")

except FileNotFoundError:
    print(f"Error: No se encontró el archivo {jsonfile}. Asegurate de que esté en la misma carpeta.")