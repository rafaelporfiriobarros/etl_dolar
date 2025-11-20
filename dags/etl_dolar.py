from airflow.decorators import dag, task
from datetime import datetime

from scripts.extract import extract_dolar
from scripts.transform import transform_dolar
from scripts.load import load_dolar

@dag(
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["etl", "dolar", "awesomeapi"]
)
def etl_dolar():

    @task
    def extract():
        return extract_dolar()

    @task
    def transform(raw_file):
        return transform_dolar(raw_file)

    @task
    def load(clean_file):
        load_dolar(clean_file)

    raw = extract()
    clean = transform(raw)
    load(clean)

etl_dolar()

