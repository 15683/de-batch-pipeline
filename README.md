# 🚀 Olist E-commerce Data Pipeline

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Dagster](https://img.shields.io/badge/Dagster-1.6+-orange.svg)](https://dagster.io/)
[![DuckDB](https://img.shields.io/badge/DuckDB-0.10+-yellow.svg)](https://duckdb.org/)
[![dbt](https://img.shields.io/badge/dbt-1.7+-red.svg)](https://www.getdbt.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> Production-grade batch data engineering pipeline for processing Brazilian e-commerce data using modern data stack

## 🎯 Overview

This project implements a **Medallion Architecture** (Bronze → Silver → Gold) data pipeline for processing e-commerce transaction data from [Olist Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). 

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Data Sources                            │
│          CSV Files (Customers, Orders, Items)               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                 Bronze Layer (Raw Data)                     │
│  ┌──────────────┐         ┌────────────────┐              │
│  │  PostgreSQL  │────────→│  MinIO/S3      │              │
│  │  (Staging)   │         │  (Parquet)     │              │
│  └──────────────┘         └────────────────┘              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              Silver Layer (Cleaned Data)                    │
│  ┌──────────────────────────────────────┐                  │
│  │         DuckDB Warehouse             │                  │
│  │  • raw schema (loaded from Parquet)  │                  │
│  │  • staging schema (dbt views)        │                  │
│  └──────────────────────────────────────┘                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│             Gold Layer (Analytics)                          │
│  ┌──────────────────────────────────────┐                  │
│  │       DuckDB Analytics Marts         │                  │
│  │  • fct_orders (fact table)           │                  │
│  │  • dim_customers (dimension)         │                  │
│  │  • daily_sales_summary               │                  │
│  │  • top_customers                     │                  │
│  └──────────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Orchestration** | [Dagster 1.6+](https://dagster.io/) | Workflow orchestration and monitoring |
| **Data Processing** | [Polars 0.20+](https://www.pola.rs/) | Fast DataFrame operations |
| **Analytics DB** | [DuckDB 0.10+](https://duckdb.org/) | OLAP database for analytics |
| **Transformation** | [dbt 1.7+](https://www.getdbt.com/) | SQL-based data transformations |
| **Object Storage** | [MinIO](https://min.io/) | S3-compatible object storage |
| **Staging DB** | [PostgreSQL 15](https://www.postgresql.org/) | Relational database for raw data |
| **Containerization** | [Docker](https://www.docker.com/) | Container orchestration |
| **File Format** | [Apache Parquet](https://parquet.apache.org/) | Columnar storage format |

## 🚀 Quick Start

### Prerequisites

- **Docker**
- **Python 3.11+**
- **8GB+ RAM**
- **Git**

### Installation

1️⃣ **Clone the repository**

```bash
git clone https://github.com/yourusername/de-batch-pipeline.git
cd de-batch-pipeline
```

2️⃣ **Create environment file**

```bash
cat > .env << 'EOF'
# PostgreSQL
POSTGRES_USER=dagster
POSTGRES_PASSWORD=dagster_password
POSTGRES_DB=dagster

# MinIO
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin

# DuckDB
DUCKDB_THREADS=2
DUCKDB_MEMORY_LIMIT=1GB

# Polars
POLARS_MAX_THREADS=2
EOF
```

3️⃣ **Add your data files**

Place your CSV files in `data/seeds/`:
- `olist_customers_dataset.csv`
- `olist_orders_dataset.csv`
- `olist_order_items_dataset.csv`

4️⃣ **Start the pipeline**

```bash
# Using Docker
docker compose up -d --build
```

5️⃣ **Access Dagster UI**

Open [http://localhost:3000](http://localhost:3000)

6️⃣ **Materialize assets**

In Dagster UI:
- Navigate to **Assets**
- Click **Materialize all**
- Monitor execution in real-time

## 📁 Project Structure

```
de-batch-pipeline/
├── 📂 orchestration/              # Dagster assets and resources
│   ├── assets/
│   │   ├── ingest_raw_data.py     # CSV → PostgreSQL
│   │   ├── export_to_minio.py     # PostgreSQL → MinIO
│   │   ├── load_to_duckdb.py      # MinIO → DuckDB
│   │   └── dbt_transformations.py # dbt model execution
│   └── resources.py               # Database connections
│
├── 📂 transformation/              # dbt project
│   ├── models/
│   │   ├── staging/               # Silver layer (cleaned data)
│   │   │   ├── stg_customers.sql
│   │   │   ├── stg_orders.sql
│   │   │   └── stg_order_items.sql
│   │   └── marts/                 # Gold layer (analytics)
│   │       ├── core/
│   │       │   ├── fct_orders.sql
│   │       │   └── dim_customers.sql
│   │       └── analytics/
│   │           ├── daily_sales_summary.sql
│   │           └── top_customers.sql
│   ├── dbt_project.yml
│   └── profiles.yml
│
├── 📂 data/
│   ├── seeds/                     # Input CSV files
│   └── warehouse.duckdb           # DuckDB database (generated)
│
├── 📂 dagster_home/
│   └── dagster.yaml               # Dagster configuration
│
├── 📂 docker/
│   └── dagster/
│       └── Dockerfile             # Dagster container
│
├── docker-compose.yaml            # Service orchestration
├── main.py                        # Dagster definitions
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🔄 Data Flow

### Pipeline Stages

#### 1️⃣ **Ingestion** (CSV → PostgreSQL)
```python
Assets: raw_customers_to_postgres, raw_orders_to_postgres, raw_order_items_to_postgres
```
- Reads CSV files with Polars
- Bulk loads into PostgreSQL
- Provides transactional safety

#### 2️⃣ **Export** (PostgreSQL → MinIO)
```python
Assets: export_customers_to_minio, export_orders_to_minio, export_order_items_to_minio
```
- Extracts data from PostgreSQL
- Converts to Parquet format (10-100x compression)
- Stores in MinIO S3-compatible storage

#### 3️⃣ **Warehouse Load** (MinIO → DuckDB)
```python
Asset: load_raw_data_to_duckdb
```
- Reads Parquet files from MinIO via S3 protocol
- Creates tables in DuckDB `raw` schema
- Enables high-performance analytics

#### 4️⃣ **Transformation** (dbt)
```python
Assets: run_dbt_staging_models, run_dbt_marts_models
```
- **Staging**: Data cleaning and standardization
- **Marts**: Business-logic transformations and aggregations

### Asset Dependency Graph

```
raw_customers_to_postgres ─────┐
                                ├──→ export_customers_to_minio ─┐
                                │                                │
raw_orders_to_postgres ────────┤                                │
                                ├──→ export_orders_to_minio ────┼──→ load_raw_data_to_duckdb
                                │                                │         ↓
raw_order_items_to_postgres ───┤                                │    run_dbt_staging_models
                                └──→ export_order_items_to_minio┘         ↓
                                                                     run_dbt_marts_models
```

## 💻 Usage

### Running the Full Pipeline

**Via Dagster UI:**
1. Open [http://localhost:3000](http://localhost:3000)
2. Navigate to **Assets** → **View all assets**
3. Click **Materialize all**
4. Monitor progress in real-time

**Via CLI:**
```bash
# Materialize all assets
docker exec de_pipeline_dagster_web dagster asset materialize --select "*"

# Materialize specific asset group
docker exec de_pipeline_dagster_web dagster asset materialize --select "tag:group=ingestion"
```

### Querying Analytics

**Connect to DuckDB:**
```bash
docker exec -it de_pipeline_dagster_web python
```

```python
import duckdb

conn = duckdb.connect('/opt/dagster/app/data/warehouse.duckdb')

# Daily sales summary
conn.execute("""
    SELECT * FROM marts.daily_sales_summary 
    ORDER BY order_purchase_date DESC 
    LIMIT 10
""").df()

# Top customers
conn.execute("""
    SELECT * FROM marts.top_customers 
    LIMIT 20
""").df()
```

### Accessing Data

**MinIO Console:**
- URL: [http://localhost:9001](http://localhost:9001)
- Username: `minioadmin`
- Password: `minioadmin`

**PostgreSQL:**
```bash
docker exec -it de_pipeline_postgres psql -U dagster -d postgres

# List tables
\dt

# Query data
SELECT COUNT(*) FROM olist_orders_dataset;
```

## 🔧 Troubleshooting

### Issue: Assets won't materialize

**Solution:**
```bash
# Check Dagster logs
docker logs de_pipeline_dagster_web --tail 100

# Reload definitions
# In Dagster UI: Click "Reload definitions"

# Restart Dagster
docker restart de_pipeline_dagster_web de_pipeline_dagster_daemon
```

### Issue: PostgreSQL connection errors

**Solution:**
```bash
# Verify PostgreSQL is healthy
docker exec de_pipeline_postgres pg_isready -U dagster

# Check logs
docker logs de_pipeline_postgres

# Restart if needed
docker restart de_pipeline_postgres
```

### Issue: DuckDB file locked

**Solution:**
```bash
# Stop all containers
docker compose down

# Remove DuckDB file
rm data/warehouse.duckdb*

# Restart
docker compose up -d
```

### Issue: Port already in use

**Solution:**
```bash
# Check what's using port 3000
lsof -i :3000

# Stop the process or change port in docker-compose.yaml
```

## 👨‍💻 Development

### Local Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests (if available)
pytest
```

### Adding New Assets

1. Create asset in `orchestration/assets/`
2. Import in `main.py`
3. Add to `Definitions` object
4. Reload definitions in Dagster UI

### Modifying dbt Models

```bash
# Enter Dagster container
docker exec -it de_pipeline_dagster_web bash

# Run specific dbt model
cd transformation
dbt run --select model_name

# Run tests
dbt test
```

## 🤝 Contributing

The project was created for educational purposes and inspired by modern data engineering best practices. Contributions are welcome!

## 📄 License

[LICENSE](LICENSE)
