# Projeto ETL de Cotação do Dólar (USD/BRL) com Airflow, PostgreSQL e Docker

Este projeto implementa um pipeline **ETL completo** utilizando **Apache Airflow**, **PostgreSQL**, **Docker**, **Python** e um modelo de **Data Lake (Bronze → Silver → Gold)**.
O pipeline captura a cotação diária do dólar via **AwesomeAPI**, transforma os dados e os armazena de forma estruturada no banco de dados para consultas analíticas.

---

# Arquitetura do Projeto

```
API (AwesomeAPI)
        │
        ▼
[EXTRACT] → Bronze (JSON)
        │
        ▼
[TRANSFORM] → Silver (CSV)
        │
        ▼
[LOAD] → Gold (PostgreSQL)
        │
        ▼
Dashboard / Consultas
```

---

# 📁 Estrutura de Diretórios

```
etl_dolar/
│── dags/
│   └── etl_dolar.py
│── scripts/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
│── tests/
│   ├── test_extract.py
│   ├── test_transform.py
│   └── test_load.py
│── data/
│   ├── bronze/
│   ├── silver/
│── docker-compose.yml
│── .env
│── README.md
```

---

# Como Rodar o Projeto do Zero (VSCode + Docker)

## **1. Subir o PostgreSQL**

```bash
docker compose up -d postgres
```

Aguarde alguns segundos.

## **2. Inicializar o banco do Airflow**

```bash
docker compose run --rm airflow-webserver airflow db init
```

## **3. Criar usuário admin**

```bash
docker compose run --rm airflow-webserver airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
```

## **4. Subir todo o ambiente**

```bash
docker compose up -d
```

## **5. Acessar o Airflow**

Abra no navegador:

```
http://localhost:8080
```

Usuário: `admin`
Senha: `admin`

## **6. Executar o DAG**

No Airflow:

* Ative o DAG `etl_dolar`
* Clique em **Trigger DAG**
* Acompanhe pelo Graph View

## **7. Consultar os dados no PostgreSQL (via DBeaver)**

```sql
SELECT * FROM cotacao_dolar ORDER BY timestamp DESC LIMIT 20;
```

---

# Explicação dos Scripts

A seguir, uma explicação clara e profissional de cada parte do projeto.

---

# `scripts/extract.py` — Camada Bronze

Responsável por **extrair** os dados diretamente da AwesomeAPI.

### Funções principais:

* Chama a URL definida em `API_URL` (do `.env`)
* Baixa os últimos registros da cotação do dólar
* Salva o resultado em um arquivo JSON na pasta `data/bronze/`
* Retorna o caminho do arquivo bruto gerado

### Pontos importantes:

* Traz logs profissionais para acompanhar o processo
* Valida o status da API
* Cria o diretório Bronze caso não exista

---

# `scripts/transform.py` — Camada Silver

Responsável por **transformar** o JSON bruto em um dataset estruturado.

### Etapas:

* Lê o arquivo Bronze
* Converte em DataFrame
* Converte colunas numéricas corretamente
* Converte o timestamp UNIX para datetime
* Gera arquivo CSV na pasta `data/silver/`
* Retorna o caminho do CSV

Essa etapa implementa a **padronização dos dados**, como acontece em pipelines reais.

---

# `scripts/load.py` — Camada Gold (PostgreSQL)

Responsável por **carregar** o arquivo Silver dentro do banco PostgreSQL.

### O que faz:

* Lê o CSV Silver
* Conecta ao banco via SQLAlchemy
* Cria ou substitui a tabela `cotacao_dolar`
* Carrega todos os dados transformados
* Gera logs informativos

Essa é a camada **Gold**, onde ficam os dados limpos e prontos para análise.

---

# Testes Automatizados (`tests/`)

Os testes garantem que o pipeline funcione **mesmo sem rodar o Airflow**.

### `test_extract.py`

Valida:

* Se a API está funcional
* Se o arquivo Bronze é criado corretamente

### `test_transform.py`

Valida:

* Se a transformação cria o arquivo Silver
* Se o DataFrame é carregado corretamente

### `test_load.py`

Valida:

* Extração → Transformação → Carga
* Se o banco aceita os dados corretamente

Esses testes deixam o projeto com um nível **profissional**, ideal para portfólio.

---

# `.env` — Variáveis de Ambiente

Arquivo utilizado para separar configurações sensíveis:

```
API_URL=https://economia.awesomeapi.com.br/json/daily/USD-BRL/30
PG_CONN=postgresql+psycopg2://airflow:airflow@postgres:5432/airflow
```

O `docker-compose.yml` carrega automaticamente esse arquivo.

---

# `docker-compose.yml`

Esse arquivo define todo o ambiente:

* Container do PostgreSQL
* Containers do Airflow (webserver + scheduler)
* Volumes persistentes
* Montagem das pastas do projeto (dags, scripts, data)
* Carregamento automático do `.env`

É o coração da infraestrutura do projeto.

---

# `dags/etl_dolar.py`

Esse arquivo define o **DAG do Airflow**, com três tasks:

1. `extract` → roda `extract_dolar()`
2. `transform` → roda `transform_dolar()`
3. `load` → roda `load_dolar()`

Ele define:

* Agendamento diário (`@daily`)
* Data de início
* Sem catchup
* Dependências entre as tasks

---

# Resultado Final

Ao final da execução teremos:

### JSON bruto (Bronze)

### CSV organizado (Silver)

### Tabela `cotacao_dolar` no PostgreSQL (Gold)

Isso permite análises, dashboards e consultas SQL de forma estruturada.

---
