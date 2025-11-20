import pandas as pd
from sqlalchemy import create_engine
import os

def load_dolar(silver_file):
    print("[LOAD] Iniciando carregamento no PostgreSQL...")

    df = pd.read_csv(silver_file)
    print(f"[LOAD] Linhas carregadas do Silver: {len(df)}")

    engine = create_engine(os.getenv("PG_CONN"))

    df.to_sql("cotacao_dolar", engine, if_exists="replace", index=False)

    print("[LOAD] Dados inseridos com sucesso na tabela cotacao_dolar!")
