"""
copyright UADER-FCYT-IS2©2024 todos los derechos reservados
Módulo re-ingeniado para automatizar pagos balanceados utilizando
patrones Singleton, Chain of Responsibility e Iterator.
"""
# pylint: disable=invalid-name, too-few-public-methods

import json
import sys
from abc import ABC, abstractmethod


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
            return f"No existe clave '{jsonkey}'"

        except FileNotFoundError:
            return "Archivo no encontrado"
        except json.JSONDecodeError:
            return "Archivo corrupto"
        except Exception as e:  # pylint: disable=broad-except
            return f"Error inesperado: {str(e)}"


class Pago:
    """Representa una solicitud de pago."""
    def __init__(self, numero_pedido, monto):
        self.numero_pedido = numero_pedido
        self.monto = monto
        self.completado = False


class ManejadorCuenta(ABC):
    """
    Clase base abstracta para la cadena de comando (Chain of Responsibility).
    Maneja los nodos de la cadena para autorizar pagos.
    """
    def __init__(self, token_name, saldo_inicial):
        self.token_name = token_name
        self.saldo = saldo_inicial
        self._siguiente = None

    def set_siguiente(self, siguiente):
        """Define el siguiente manejador en la cadena y lo retorna."""
        self._siguiente = siguiente
        return siguiente

    @abstractmethod
    def procesar_pago(self, pago, registro):
        """Procesa el pago o lo delega al siguiente manejador de la cadena."""


class CuentaBancaria(ManejadorCuenta):
    """Manejador concreto que representa una cuenta bancaria específica."""

    def procesar_pago(self, pago, registro):
        # Si el pago no está completo y hay saldo, lo procesamos aquí.
        if not pago.completado and self.saldo >= pago.monto:
            self.saldo -= pago.monto
            pago.completado = True
            
            # Extraemos la clave del banco usando el Singleton
            token_val = TokenReader().get_token(self.token_name)
            
            resultado = (f"Pedido: {pago.numero_pedido:02d} | "
                         f"Monto: ${pago.monto} | "
                         f"Token: {self.token_name} ({token_val}) | "
                         f"Saldo Restante: ${self.saldo}")
            
            registro.agregar_pago(resultado)
            print(f"[APROBADO] {resultado}")

        # Si no hay saldo, pero hay una cuenta siguiente en la cadena, delegamos.
        elif self._siguiente:
            self._siguiente.procesar_pago(pago, registro)
        
        # Si llegamos al final de la cadena sin procesarlo, el pago falla.
        else:
            fallo = (f"Pedido: {pago.numero_pedido:02d} | "
                     f"RECHAZADO por saldo insuficiente en todas las cuentas "
                     f"(Monto solicitado: ${pago.monto})")
            registro.agregar_pago(fallo)
            print(f"[DENEGADO] {fallo}")


class IteradorPagos:
    """Patrón Iterator para recorrer los pagos registrados de forma segura."""
    def __init__(self, lista_pagos):
        self._pagos = lista_pagos
        self._indice = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._indice < len(self._pagos):
            pago = self._pagos[self._indice]
            self._indice += 1
            return pago
        raise StopIteration


class RegistroPagos:
    """Colección de operaciones que puede ser iterada cronológicamente."""
    def __init__(self):
        self._pagos = []

    def agregar_pago(self, detalle):
        """Añade un string con el detalle de la operación al registro."""
        self._pagos.append(detalle)

    def __iter__(self):
        """Retorna la instancia del iterador para esta colección."""
        return IteradorPagos(self._pagos)


def main():
    """Función principal para la simulación de pagos automáticos."""
    # Control del argumento -v para la versión actualizada (1.2)
    if len(sys.argv) == 2 and sys.argv[1] == '-v':
        print("versión 1.2")
        sys.exit(0)

    # 1. Configuración inicial de cuentas y saldos
    cuenta1 = CuentaBancaria('token1', 1000)
    cuenta2 = CuentaBancaria('token2', 2000)

    # 2. Instanciación del registro para el iterador
    registro = RegistroPagos()

    # 3. Generación de los pedidos de prueba ($500 c/u)
    # 7 pedidos requerirían $3500, pero solo hay $3000 en total. El último debe fallar.
    pedidos = [Pago(i, 500) for i in range(1, 8)]

    # Variable para controlar el ruteo alternativo (balanceo)
    turno_cuenta1 = True

    print("--- INICIANDO PROCESAMIENTO DE PAGOS ---")
    for pedido in pedidos:
        # Re-armamos la cadena de mando dinámicamente según de quién es el turno
        if turno_cuenta1:
            cuenta1.set_siguiente(cuenta2)
            cuenta2.set_siguiente(None)
            cuenta1.procesar_pago(pedido, registro)
        else:
            cuenta2.set_siguiente(cuenta1)
            cuenta1.set_siguiente(None)
            cuenta2.procesar_pago(pedido, registro)

        # Alternar el turno para el siguiente pedido
        turno_cuenta1 = not turno_cuenta1

    # 4. Listado cronológico utilizando el patrón Iterator
    print("\n--- LISTADO CRONOLÓGICO DE PAGOS (Patrón Iterator) ---")
    for detalle in registro:
        print(detalle)


if __name__ == '__main__':
    main()