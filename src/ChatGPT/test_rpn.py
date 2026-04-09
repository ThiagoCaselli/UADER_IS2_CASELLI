import unittest
import math
import sys
from io import StringIO
from rpn import RPNCalculator, RPNError, main

class TestRPNCalculator(unittest.TestCase):
    def setUp(self):
        """Inicializa una instancia limpia antes de cada test."""
        self.calc = RPNCalculator()

    def test_basic_arithmetic(self):
        """Prueba operaciones básicas: +, -, *, /."""
        self.assertEqual(self.calc.evaluate("10 5 +"), 15.0)
        self.assertEqual(self.calc.evaluate("10 5 -"), 5.0)
        self.assertEqual(self.calc.evaluate("10 5 *"), 50.0)
        self.assertEqual(self.calc.evaluate("10 5 /"), 2.0)

    def test_stack_commands(self):
        """Prueba comandos de manipulación de pila: dup, swap, drop, clear."""
        self.assertEqual(self.calc.evaluate("3 dup +"), 6.0)
        self.assertEqual(self.calc.evaluate("10 2 swap /"), 0.2)
        self.assertEqual(self.calc.evaluate("10 20 drop"), 10.0)
        # Probar CLEAR: la pila queda vacía, por lo que evaluate lanza error al final
        with self.assertRaises(RPNError):
            self.calc.evaluate("10 clear")

    def test_scientific_and_constants(self):
        """Prueba constantes, funciones trigonométricas y exponenciales."""
        self.assertAlmostEqual(self.calc.evaluate("pi"), math.pi, places=5)
        self.assertAlmostEqual(self.calc.evaluate("phi"), (1 + 5**0.5) / 2, places=5)
        self.assertAlmostEqual(self.calc.evaluate("90 sin"), 1.0)
        self.assertAlmostEqual(self.calc.evaluate("0 cos"), 1.0)
        self.assertAlmostEqual(self.calc.evaluate("45 tg"), 1.0)
        self.assertEqual(self.calc.evaluate("100 log"), 2.0)
        self.assertEqual(self.calc.evaluate("2 ln"), math.log(2))
        self.assertEqual(self.calc.evaluate("4 sqrt"), 2.0)
        self.assertEqual(self.calc.evaluate("5 chs"), -5.0) 
        self.assertEqual(self.calc.evaluate("2 3 yx"), 8.0)
        self.assertEqual(self.calc.evaluate("1 exp"), math.e)
        self.assertEqual(self.calc.evaluate("2 10x"), 100.0)
        self.assertEqual(self.calc.evaluate("4 1/x"), 0.25)

    def test_memory_registers(self):
        """Prueba el almacenamiento (STO) y recuperación (RCL) de memoria."""
        self.assertEqual(self.calc.evaluate("42 sto05"), 42.0)
        self.assertEqual(self.calc.evaluate("rcl05"), 42.0)

    def test_main_and_errors(self):
        """Prueba la ejecución de main y casos de error (Consigna 14)."""
        # 1. Prueba de ejecución exitosa vía main
        sys.argv = ["rpn.py", "3", "4", "+"]
        output = StringIO()
        sys.stdout = output
        main()
        sys.stdout = sys.__stdout__
        self.assertEqual(output.getvalue().strip(), "7.0")

        # 2. División por cero
        with self.assertRaisesRegex(RPNError, "división por cero"):
            self.calc.evaluate("10 0 /")
        
        # 3. Token inválido
        with self.assertRaisesRegex(RPNError, "token inválido"):
            self.calc.evaluate("invalid_token")
            
        # 4. Pila insuficiente
        with self.assertRaisesRegex(RPNError, "pila insuficiente"):
            self.calc.evaluate("1 +")
            
        # 5. Registro de memoria inexistente (rcl99)
        # Validamos que lance RPNError (el mensaje puede variar por la modularización)
        with self.assertRaises(RPNError):
            self.calc.evaluate("rcl99")

    def test_coverage_additional_lines(self):
        """Cubre líneas adicionales de error para maximizar cobertura."""
        # Pila insuficiente para funciones unitarias
        with self.assertRaises(RPNError):
            self.calc.evaluate("sin")
        
        # Más de un elemento en la pila al finalizar
        with self.assertRaises(RPNError):
            self.calc.evaluate("10 20")
            
        # Entrada vacía en main no debe fallar
        sys.argv = ["rpn.py"]
        main()

if __name__ == "__main__":
    unittest.main()