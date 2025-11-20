from scripts.extract import extract_dolar
from scripts.transform import transform_dolar
from scripts.load import load_dolar
import pandas as pd

def test_load():
    raw = extract_dolar()
    silver = transform_dolar(raw)
    load_dolar(silver)
    assert True
