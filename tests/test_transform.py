from scripts.extract import extract_dolar
from scripts.transform import transform_dolar
import os

def test_transform_file_created():
    raw = extract_dolar()
    silver = transform_dolar(raw)
    assert os.path.exists(silver)
