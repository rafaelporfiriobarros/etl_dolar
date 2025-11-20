import requests
import json
from datetime import datetime
import os

def extract_dolar():
    print("[EXTRACT] Iniciando extração...")

    url = os.getenv("API_URL")

    try:
        response = requests.get(url, timeout=10)
    except Exception as e:
        raise Exception(f"[EXTRACT] Erro ao chamar a API: {e}")

    print(f"[EXTRACT] Status da API: {response.status_code}")

    if response.status_code != 200:
        raise Exception(
            f"[EXTRACT] Erro na API AwesomeAPI: {response.status_code} - {response.text[:200]}"
        )

    data = response.json()

    os.makedirs("data/bronze", exist_ok=True)
    filename = f"data/bronze/usd_brl_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"[EXTRACT] Arquivo Bronze criado: {filename}")

    return filename
