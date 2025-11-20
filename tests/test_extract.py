from scripts.extract import extract_dolar
import os

def test_extract_file_created():
    file = extract_dolar()
    assert os.path.exists(file)
