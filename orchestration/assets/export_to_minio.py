from io import BytesIO
from pathlib import Path

import polars as pl
import psycopg2
from dagster import AssetExecutionContext, AssetIn, asset
from minio import Minio


@asset(
    group_name="export",
    ins={"raw_customers": AssetIn("raw_customers_to_postgres")}
)
def export_customers_to_minio(
    context: AssetExecutionContext,
    raw_customers: dict
) -> dict:
    """Export customers from PostgreSQL to MinIO as Parquet."""

    connection_uri = "postgresql://dagster:dagster_password@postgres:5432/postgres"

    df = pl.read_database_uri(
        query="SELECT * FROM olist_customers_dataset",
        uri=connection_uri,
        engine="connectorx"
    )

    context.log.info(f"Exporting {len(df)} customers to MinIO")

    # Convert to Parquet
    buffer = BytesIO()
    df.write_parquet(buffer)
    buffer.seek(0)

    # Upload to MinIO
    minio_client = Minio(
        "minio:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )

    bucket_name = "olist-data"

    # Create bucket if not exists
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)
        context.log.info(f"Created bucket: {bucket_name}")

    # Upload
    minio_client.put_object(
        bucket_name,
        "raw/customers.parquet",
        buffer,
        length=buffer.getbuffer().nbytes,
        content_type="application/octet-stream"
    )

    context.log.info("✅ Customers exported to MinIO")
    return {"rows_exported": len(df), "file": "raw/customers.parquet"}


@asset(
    group_name="export",
    ins={"raw_orders": AssetIn("raw_orders_to_postgres")}
)
def export_orders_to_minio(
    context: AssetExecutionContext,
    raw_orders: dict
) -> dict:
    """Export orders from PostgreSQL to MinIO as Parquet."""

    connection_uri = "postgresql://dagster:dagster_password@postgres:5432/postgres"

    df = pl.read_database_uri(
        query="SELECT * FROM olist_orders_dataset",
        uri=connection_uri,
        engine="connectorx"
    )

    context.log.info(f"Exporting {len(df)} orders to MinIO")

    buffer = BytesIO()
    df.write_parquet(buffer)
    buffer.seek(0)

    minio_client = Minio(
        "minio:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )

    bucket_name = "olist-data"
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)

    minio_client.put_object(
        bucket_name,
        "raw/orders.parquet",
        buffer,
        length=buffer.getbuffer().nbytes,
        content_type="application/octet-stream"
    )

    context.log.info("✅ Orders exported to MinIO")
    return {"rows_exported": len(df), "file": "raw/orders.parquet"}


@asset(
    group_name="export",
    ins={"raw_items": AssetIn("raw_order_items_to_postgres")}
)
def export_order_items_to_minio(
    context: AssetExecutionContext,
    raw_items: dict
) -> dict:
    """Export order items from PostgreSQL to MinIO as Parquet."""

    connection_uri = "postgresql://dagster:dagster_password@postgres:5432/postgres"

    df = pl.read_database_uri(
        query="SELECT * FROM olist_order_items_dataset",
        uri=connection_uri,
        engine="connectorx"
    )

    context.log.info(f"Exporting {len(df)} order items to MinIO")

    buffer = BytesIO()
    df.write_parquet(buffer)
    buffer.seek(0)

    minio_client = Minio(
        "minio:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )

    bucket_name = "olist-data"
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)

    minio_client.put_object(
        bucket_name,
        "raw/order_items.parquet",
        buffer,
        length=buffer.getbuffer().nbytes,
        content_type="application/octet-stream"
    )

    context.log.info("✅ Order items exported to MinIO")
    return {"rows_exported": len(df), "file": "raw/order_items.parquet"}
