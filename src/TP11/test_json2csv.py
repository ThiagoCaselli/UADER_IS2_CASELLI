import io
import pytest
import json
from json2csv import convert_json_to_csv

def test_convert_json_to_csv_success():
    # Simula un archivo JSON de entrada
    json_data = '[{"nombre": "Thiago", "edad": 21}, {"nombre": "Gael", "edad": 20}]'
    in_stream = io.StringIO(json_data)
    out_stream = io.StringIO()

    # Ejecuta la función
    convert_json_to_csv(in_stream, out_stream)

    # Verifica la salida
    result = out_stream.getvalue()
    assert "nombre,edad" in result
    assert "Thiago,21" in result

def test_convert_json_to_csv_invalid_format():
    # JSON que no es una lista de diccionarios
    json_data = '{"nombre": "Thiago"}'
    in_stream = io.StringIO(json_data)
    out_stream = io.StringIO()

    with pytest.raises(ValueError, match="lista de diccionarios"):
        convert_json_to_csv(in_stream, out_stream)