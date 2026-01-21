# de-batch-pipeline

Batch data engineering pipeline using Dagster, DuckDB, dbt, and Polars.

## Tech Stack

- **Orchestration**: Dagster
- **Data Processing**: DuckDB, Polars
- **Transformation**: dbt
- **Storage**: PostgreSQL (metadata), MinIO (object storage)
- **Containerization**: Finch/Docker

## Prerequisites

- Python 3.11+
- Finch or Docker
- 8GB+ RAM recommended

## Local Development Setup

### 1. Clone repository
```bash
git clone https://github.com/15683/de-batch-pipeline.git
cd de-batch-pipeline
