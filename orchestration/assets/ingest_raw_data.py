from pathlib import Path

import polars as pl
import psycopg2
from dagster import AssetExecutionContext, asset
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


@asset(group_name="ingestion")
def raw_customers_to_postgres(context: AssetExecutionContext) -> dict:
    """Load customers CSV into PostgreSQL."""

    csv_path = Path("data/seeds/olist_customers_dataset.csv")
    context.log.info(f"Reading CSV from {csv_path}")

    # Read with Polars for fast processing
    df = pl.read_csv(csv_path)
    context.log.info(f"Loaded {len(df)} customers")

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host="postgres",
        port=5432,
        user="dagster",
        password="dagster_password",
        database="postgres"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    # Create table
    cursor.execute("""
        DROP TABLE IF EXISTS olist_customers_dataset CASCADE;
        CREATE TABLE olist_customers_dataset (
            customer_id VARCHAR(100) PRIMARY KEY,
            customer_unique_id VARCHAR(100),
            customer_zip_code_prefix VARCHAR(10),
            customer_city VARCHAR(100),
            customer_state VARCHAR(2)
        );
    """)

    # Bulk insert
    from io import StringIO
    buffer = StringIO()
    df.write_csv(buffer)
    buffer.seek(0)

    cursor.copy_expert(
        "COPY olist_customers_dataset FROM STDIN WITH CSV HEADER",
        buffer
    )

    cursor.close()
    conn.close()

    context.log.info("✅ Customers loaded to PostgreSQL")
    return {"rows_loaded": len(df)}


@asset(group_name="ingestion")
def raw_orders_to_postgres(context: AssetExecutionContext) -> dict:
    """Load orders CSV into PostgreSQL."""

    csv_path = Path("data/seeds/olist_orders_dataset.csv")
    df = pl.read_csv(csv_path)
    context.log.info(f"Loaded {len(df)} orders")

    conn = psycopg2.connect(
        host="postgres",
        port=5432,
        user="dagster",
        password="dagster_password",
        database="postgres"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    cursor.execute("""
        DROP TABLE IF EXISTS olist_orders_dataset CASCADE;
        CREATE TABLE olist_orders_dataset (
            order_id VARCHAR(100) PRIMARY KEY,
            customer_id VARCHAR(100),
            order_status VARCHAR(50),
            order_purchase_timestamp TIMESTAMP,
            order_approved_at TIMESTAMP,
            order_delivered_carrier_date TIMESTAMP,
            order_delivered_customer_date TIMESTAMP,
            order_estimated_delivery_date TIMESTAMP
        );
    """)

    # Bulk insert
    from io import StringIO
    buffer = StringIO()
    df.write_csv(buffer)
    buffer.seek(0)

    cursor.copy_expert(
        "COPY olist_orders_dataset FROM STDIN WITH CSV HEADER",
        buffer
    )

    cursor.close()
    conn.close()

    context.log.info("✅ Orders loaded to PostgreSQL")
    return {"rows_loaded": len(df)}


@asset(group_name="ingestion")
def raw_order_items_to_postgres(context: AssetExecutionContext) -> dict:
    """Load order items CSV into PostgreSQL."""

    csv_path = Path("data/seeds/olist_order_items_dataset.csv")
    df = pl.read_csv(csv_path)
    context.log.info(f"Loaded {len(df)} order items")

    conn = psycopg2.connect(
        host="postgres",
        port=5432,
        user="dagster",
        password="dagster_password",
        database="postgres"
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    cursor.execute("""
        DROP TABLE IF EXISTS olist_order_items_dataset CASCADE;
        CREATE TABLE olist_order_items_dataset (
            order_id VARCHAR(100),
            order_item_id INTEGER,
            product_id VARCHAR(100),
            seller_id VARCHAR(100),
            shipping_limit_date TIMESTAMP,
            price DECIMAL(10,2),
            freight_value DECIMAL(10,2),
            PRIMARY KEY (order_id, order_item_id)
        );
    """)

    # Bulk insert
    from io import StringIO
    buffer = StringIO()
    df.write_csv(buffer)
    buffer.seek(0)

    cursor.copy_expert(
        "COPY olist_order_items_dataset FROM STDIN WITH CSV HEADER",
        buffer
    )

    cursor.close()
    conn.close()

    context.log.info("✅ Order items loaded to PostgreSQL")
    return {"rows_loaded": len(df)}
