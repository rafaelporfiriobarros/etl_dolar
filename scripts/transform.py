import pandas as pd
import json
import os

def transform_dolar(raw_file):
    print(f"[TRANSFORM] Lendo Bronze: {raw_file}")

    with open(raw_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    print(f"[TRANSFORM] Linhas carregadas: {len(df)}")

    numeric = ["high", "low", "pctChange", "bid", "ask"]
    df[numeric] = df[numeric].apply(pd.to_numeric, errors="coerce")

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

    os.makedirs("data/silver", exist_ok=True)
    silver_file = raw_file.replace("bronze", "silver").replace(".json", ".csv")

    df.to_csv(silver_file, index=False)
    print(f"[TRANSFORM] Silver salvo em: {silver_file}")

    return silver_file
