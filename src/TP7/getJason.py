"""
copyright UADER-FCYT-IS2©2024 todos los derechos reservados
Módulo para recuperar tokens de un archivo JSON utilizando el patrón Singleton.
"""
# pylint: disable=invalid-name

import json
import sys


class TokenReader:
    """Clase Singleton para aislar la lectura de tokens del archivo JSON."""
    _instance = None
    jsonfile = 'sitedata.json'

    def __new__(cls):
        # Implementación del patrón Singleton: si no existe la instancia, la crea.
        if cls._instance is None:
            cls._instance = super(TokenReader, cls).__new__(cls)
        return cls._instance

    def get_token(self, jsonkey):
        """Recupera el token especificado manejando errores de forma controlada."""
        try:
            with open(self.jsonfile, 'r', encoding='utf-8') as myfile:
                data = myfile.read()

            obj = json.loads(data)

            if jsonkey in obj:
                return str(obj[jsonkey])
            return f"Error controlado: La clave '{jsonkey}' no existe en {self.jsonfile}."

        except FileNotFoundError:
            return f"Error controlado: No se encontró el archivo {self.jsonfile}."
        except json.JSONDecodeError:
            return f"Error controlado: El archivo {self.jsonfile} está corrupto."
        except Exception as e:  # pylint: disable=broad-except
            return f"Error controlado inesperado: {str(e)}"


def main():
    """Función principal para manejar los parámetros externos."""
    try:
        # Control del argumento -v para la versión
        if len(sys.argv) == 2 and sys.argv[1] == '-v':
            print("versión 1.1")
            sys.exit(0)

        # Asignación de la clave por defecto
        jsonkey = 'token1'

        # Validación de argumentos
        if len(sys.argv) > 2:
            print("Error controlado: Demasiados argumentos. Uso: py getJason.py [clave]")
            sys.exit(0)
        elif len(sys.argv) == 2:
            jsonkey = sys.argv[1]

        # Branching by abstraction: instanciamos la nueva clase para el proceso
        reader = TokenReader()
        resultado = reader.get_token(jsonkey)
        print(resultado)

    except Exception as e:  # pylint: disable=broad-except
        print(f"Error controlado en la ejecución del sistema: {str(e)}")


if __name__ == '__main__':
    main()