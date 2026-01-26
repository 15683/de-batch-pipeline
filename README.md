# de-batch-pipeline

Batch data engineering pipeline using Dagster, DuckDB, dbt, and Polars.

# Olist E-commerce Data Pipeline Guide

## Architecture

```
CSV Files (Raw Data)
    ↓
PostgreSQL (Staging)
    ↓
Polars (Data Cleaning)
    ↓
MinIO (Parquet Storage)
    ↓
DuckDB (Analytics Warehouse)
    ↓
dbt (Transformations)
    ↓
Dagster (Orchestration & Monitoring)

## Tech Stack

- **Orchestration**: Dagster
- **Data Processing**: DuckDB, Polars
- **Transformation**: dbt
- **Storage**: PostgreSQL (metadata), MinIO (object storage)
- **Containerization**: Docker

## Prerequisites

- Python 3.11+
- Docker
- 8GB+ RAM recommended

## Local Development Setup

### 1. Clone repository
```bash
git clone https://github.com/15683/de-batch-pipeline.git
cd de-batch-pipeline
