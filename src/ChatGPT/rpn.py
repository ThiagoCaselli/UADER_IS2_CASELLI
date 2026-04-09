"""
Módulo rpn: Implementación de una calculadora de Notación Polaca Inversa (RPN).
Este módulo contiene la lógica para procesar operaciones aritméticas, funciones
científicas, constantes y manejo de memoria a través de una pila.
Diseñado para cumplir con estándares de alta calidad y baja complejidad.
"""

import math
import operator
import sys


class RPNError(Exception):
    """
    Excepción de dominio para errores específicos del evaluador RPN.
    Provee una base para diferenciar errores lógicos de errores de Python.
    """


class RPNCalculator:  # pylint: disable=too-few-public-methods
    """
    Motor de cálculo para Notación Polaca Inversa.
    Mantiene el estado de la pila y provee métodos para procesar tokens.
    Implementa modularidad extrema para reducir la complejidad ciclomática.
    """

    def __init__(self):
        """
        Inicializa la pila, los registros de memoria y diccionarios de ops.
        La configuración inicial asegura un entorno limpio para cada instancia.
        """
        # Pila de operandos en memoria dinámica para cálculos intermedios.
        self.stack = []
        # 10 registros de memoria (00 a 09) para almacenamiento persistente.
        self.memory = {f"{i:02d}": 0.0 for i in range(10)}
        # Constantes matemáticas base requeridas por la especificación.
        self.constants = {"pi": math.pi, "phi": (1 + math.sqrt(5)) / 2}
        # Tabla de despacho para funciones de un solo operando (unitarias).
        self.unary_ops = {
            "sqrt": math.sqrt,
            "log": math.log10,
            "ln": math.log,
            "exp": math.exp,
            "10x": lambda x: 10**x,
            "1/x": lambda x: 1 / x,
            "chs": lambda x: -x,
            "sin": lambda x: math.sin(math.radians(x)),
            "cos": lambda x: math.cos(math.radians(x)),
            "tg": lambda x: math.tan(math.radians(x)),
            "asin": lambda x: math.degrees(math.asin(x)),
            "acos": lambda x: math.degrees(math.acos(x)),
            "atg": lambda x: math.degrees(math.atan(x)),
        }
        # Tabla de despacho para operaciones aritméticas binarias básicas.
        self.binary_ops = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
            "yx": operator.pow,
        }

    def _check_const(self, token):
        """
        Verifica si el token es una constante matemática definida.
        Si coincide con pi o phi, apila el valor correspondiente.
        """
        if token in self.constants:
            self.stack.append(self.constants[token])
            return True
        return False

    def _check_unary(self, token):
        """
        Ejecuta operaciones unarias validando el estado de la pila.
        Lanza IndexError si no hay elementos suficientes para la operación.
        """
        if token in self.unary_ops:
            if not self.stack:
                raise IndexError
            self.stack.append(self.unary_ops[token](self.stack.pop()))
            return True
        return False

    def _check_binary(self, token):
        """
        Ejecuta operaciones binarias validando el estado de la pila.
        Requiere exactamente dos operandos para procesar la instrucción.
        """
        if token in self.binary_ops:
            if len(self.stack) < 2:
                raise IndexError
            val_b, val_a = self.stack.pop(), self.stack.pop()
            self.stack.append(self.binary_ops[token](val_a, val_b))
            return True
        return False

    def _check_stack(self, token):
        """
        Procesa comandos de manipulación directa de la pila de datos.
        Incluye funciones de duplicación, intercambio, descarte y limpieza.
        """
        cmds = ("dup", "swap", "drop", "clear")
        if token in cmds:
            self._run_stack_logic(token)
            return True
        return False

    def _run_stack_logic(self, token):
        """
        Lógica interna detallada para comandos dup, swap, drop y clear.
        Centraliza la manipulación del puntero de la lista para mayor claridad.
        """
        if token == "dup":
            if not self.stack:
                raise IndexError
            self.stack.append(self.stack[-1])
        elif token == "swap":
            if len(self.stack) < 2:
                raise IndexError
            self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]
        elif token == "drop":
            if not self.stack:
                raise IndexError
            self.stack.pop()
        else:  # comando clear
            self.stack.clear()

    def _check_mem(self, token):
        """
        Procesa comandos de interacción con los registros de memoria STO/RCL.
        Permite persistir valores a lo largo de múltiples operaciones del motor.
        """
        if token.startswith("sto"):
            if not self.stack:
                raise IndexError
            self.memory[token[3:]] = self.stack[-1]
            return True
        if token.startswith("rcl"):
            self.stack.append(self.memory[token[3:]])
            return True
        return False

    def _execute_token(self, token):
        """
        Despacho modularizado para procesar cada token individualmente.
        Intenta mapear el token contra comandos conocidos antes de tratarlo como número.
        """
        # Se recorren los verificadores modulares para minimizar rutas de decisión.
        for check in [
            self._check_const,
            self._check_unary,
            self._check_binary,
            self._check_stack,
            self._check_mem,
        ]:
            if check(token):
                return True
        # Si el token no es una instrucción, se evalúa como operando numérico.
        try:
            self.stack.append(float(token))
            return True
        except ValueError:
            return False

    def evaluate(self, expression):
        """
        Procesa una expresión completa y valida el resultado final único.
        Gestiona el ciclo de vida de la evaluación y captura errores lógicos.
        """
        self.stack.clear()
        for token in expression.lower().split():
            try:
                if not self._execute_token(token):
                    raise RPNError("token inválido")  #
            except IndexError as exc:
                raise RPNError("pila insuficiente") from exc  #
            except ZeroDivisionError as exc:
                raise RPNError("división por cero") from exc  #
            except Exception as exc:
                if isinstance(exc, RPNError):
                    raise exc
                raise RPNError(str(exc)) from exc  #
        # El programa debe finalizar exactamente con un elemento residual en pila.
        if len(self.stack) != 1:
            raise RPNError("pila insuficiente")
        return self.stack.pop()


def main():
    """
    Entrada principal para aceptar argumentos o lectura desde stdin.
    Provee la interfaz de usuario para interactuar con la lógica del motor.
    """
    calc = RPNCalculator()
    # Combina argumentos de línea de comandos o lee de la entrada estándar directa.
    inp = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else sys.stdin.read()
    if inp.strip():
        try:
            # Evaluación e impresión del resultado formateado en la consola de salida.
            print(calc.evaluate(inp))
        except RPNError as err:
            # Muestra el mensaje de error descriptivo capturado de la excepción.
            print(f"Error: {err}")


if __name__ == "__main__":
    main()
