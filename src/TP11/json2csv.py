"""
Módulo json2csv.
Permite convertir archivos de formato JSON a CSV utilizando una estrategia de filtro.
Cumple con las convenciones PEP8 y PEP257.
"""

import argparse
import csv
import json
import sys
from typing import Any, TextIO


def convert_json_to_csv(
    input_stream: TextIO, output_stream: TextIO, delimiter: str = ","
) -> None:
    """
    Convierte datos en formato JSON desde un stream de entrada a un CSV en un stream de salida.

    Args:
        input_stream (TextIO): Flujo de entrada (archivo o stdin) con datos JSON.
        output_stream (TextIO): Flujo de salida (archivo o stdout) para el CSV.
        delimiter (str): Carácter separador para el CSV. Por defecto es coma (,).

    Raises:
        ValueError: Si el JSON no es una lista de diccionarios (formato tabular).
        json.JSONDecodeError: Si el contenido no es un JSON válido.
    """
    try:
        data: list[dict[str, Any]] = json.load(input_stream)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error al decodificar JSON: {e}") from e

    if not isinstance(data, list) or not all(isinstance(row, dict) for row in data):
        raise ValueError(
            "El JSON debe ser una lista de diccionarios para poder aplanarse a CSV."
        )

    if not data:
        # JSON vacío
        return

    # Extraer las cabeceras a partir de las claves del primer diccionario
    headers: list[str] = list(data[0].keys())

    writer = csv.DictWriter(output_stream, fieldnames=headers, delimiter=delimiter)
    writer.writeheader()
    writer.writerows(data)


def main() -> None:
    """Función principal que maneja los argumentos de la línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Convierte un archivo JSON a formato CSV."
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="Archivo JSON de entrada. Omita para usar stdin.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Archivo CSV de salida. Omita para usar stdout.",
    )
    parser.add_argument(
        "-d",
        "--delimiter",
        type=str,
        default=",",
        help="Delimitador del CSV (defecto: coma).",
    )

    args = parser.parse_args()

    # Manejo robusto de I/O
    in_file: TextIO = (
        open(args.input, "r", encoding="utf-8") if args.input else sys.stdin
    )  # noqa: SIM115
    out_file: TextIO = (
        open(args.output, "w", encoding="utf-8", newline="")
        if args.output
        else sys.stdout
    )  # noqa: SIM115

    try:
        convert_json_to_csv(in_file, out_file, args.delimiter)
    except (ValueError, OSError) as e:
        print(f"Error fatal durante la conversión: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        # Solo cerramos los archivos si no son los streams estándar
        if in_file is not sys.stdin:
            in_file.close()
        if out_file is not sys.stdout:
            out_file.close()


if __name__ == "__main__":
    main()
