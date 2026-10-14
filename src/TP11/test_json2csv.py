import io
import sys
from unittest.mock import patch

import pytest

from json2csv import convert_json_to_csv, main


def test_convert_json_to_csv_success():
    """Prueba la conversión exitosa de una lista válida."""
    json_data = '[{"nombre": "Thiago", "edad": 21}]'
    in_stream = io.StringIO(json_data)
    out_stream = io.StringIO()
    convert_json_to_csv(in_stream, out_stream)
    resultado = out_stream.getvalue()
    assert "nombre,edad" in resultado
    assert "Thiago,21" in resultado


def test_convert_json_to_csv_invalid_format():
    """Prueba que lance error si no es una lista de diccionarios."""
    with pytest.raises(ValueError, match="lista de diccionarios"):
        convert_json_to_csv(io.StringIO('{"nombre": "Thiago"}'), io.StringIO())


def test_convert_json_to_csv_empty_list():
    """Prueba que maneje correctamente un JSON vacío."""
    out_stream = io.StringIO()
    convert_json_to_csv(io.StringIO("[]"), out_stream)
    assert out_stream.getvalue() == ""


def test_convert_json_to_csv_decode_error():
    """Prueba que maneje texto que no es JSON válido."""
    with pytest.raises(ValueError, match="Error al decodificar JSON"):
        convert_json_to_csv(io.StringIO("esto no es un json"), io.StringIO())


def test_main_with_files(tmp_path):
    """Prueba la función main simulando archivos reales de entrada y salida."""
    input_file = tmp_path / "input.json"
    output_file = tmp_path / "output.csv"
    input_file.write_text('[{"id": 1, "val": "A"}]', encoding="utf-8")

    # Simulamos los argumentos de la consola: python json2csv.py -i input.json -o output.csv
    with patch("sys.argv", ["json2csv", "-i", str(input_file), "-o", str(output_file)]):
        main()

    resultado = output_file.read_text(encoding="utf-8")
    assert "id,val" in resultado
    assert "1,A" in resultado


@patch("sys.stdin", io.StringIO('[{"user": "Gael"}]'))
@patch("sys.stdout", new_callable=io.StringIO)
def test_main_stdin_stdout(mock_stdout):
    """Prueba la función main usando entrada y salida estándar (sin archivos)."""
    with patch("sys.argv", ["json2csv"]):
        main()
    assert "user" in mock_stdout.getvalue()
    assert "Gael" in mock_stdout.getvalue()


def test_main_invalid_json_sys_exit(tmp_path):
    """Prueba que el programa se cierre con código de error 1 si el JSON es inválido."""
    input_file = tmp_path / "bad.json"
    input_file.write_text("data corrupta", encoding="utf-8")

    with patch("sys.argv", ["json2csv", "-i", str(input_file)]):
        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 1
