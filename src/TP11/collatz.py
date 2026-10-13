# Calculando el número de iteraciones del algoritmo de Collatz
def collatz(num):
    # Validación de requerimientos de límite y tipo
    if not isinstance(num, int):
        raise ValueError("Debe ser un número entero.")
    if num <= 0:
        raise ValueError("El número debe ser positivo.")
    if num > 1999:
        raise ValueError("Límite superado. Máximo 1999.")

    iteraciones = 0
    while num != 1:
        if num % 2 == 0:
            num = num // 2
        else:
            num = 3 * num + 1
        iteraciones += 1

    return iteraciones


# Comprobando los resultados y aceptando ingreso por teclado
if __name__ == "__main__":
    try:
        entrada = input("Ingrese un número entero positivo (máx 1999): ")
        i = int(entrada)
        total_iter = collatz(i)
        print("El número de partida es %d" % i)
        print("El número de iteraciones para %d es %d" % (i, total_iter))
    except ValueError as e:
        print("Error de validación:", e)
