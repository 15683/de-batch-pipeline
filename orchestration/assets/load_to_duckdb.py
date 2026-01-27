
import duckdb
from dagster import AssetExecutionContext, AssetIn, asset


@asset(
    group_name="warehouse",
    ins={
        "customers_parquet": AssetIn("export_customers_to_minio"),
        "orders_parquet": AssetIn("export_orders_to_minio"),
        "items_parquet": AssetIn("export_order_items_to_minio"),
    }
)
def load_raw_data_to_duckdb(
    context: AssetExecutionContext,
    customers_parquet: dict,
    orders_parquet: dict,
    items_parquet: dict
) -> dict:
    """Load Parquet files from MinIO into DuckDB."""

    db_path = "data/warehouse.duckdb"
    conn = duckdb.connect(db_path)

    # Install and load extensions
    conn.execute("INSTALL httpfs;")
    conn.execute("LOAD httpfs;")

    # Configure MinIO access
    conn.execute("""
        SET s3_region='us-east-1';
        SET s3_endpoint='minio:9000';
        SET s3_access_key_id='minioadmin';
        SET s3_secret_access_key='minioadmin';
        SET s3_use_ssl=false;
        SET s3_url_style='path';
    """)

    # Create schema
    conn.execute("CREATE SCHEMA IF NOT EXISTS raw;")

    # Load customers
    context.log.info("Loading customers to DuckDB...")
    conn.execute("""
        CREATE OR REPLACE TABLE raw.olist_customers_dataset AS
        SELECT * FROM read_parquet('s3://olist-data/raw/customers.parquet');
    """)

    # Load orders
    context.log.info("Loading orders to DuckDB...")
    conn.execute("""
        CREATE OR REPLACE TABLE raw.olist_orders_dataset AS
        SELECT * FROM read_parquet('s3://olist-data/raw/orders.parquet');
    """)

    # Load order items
    context.log.info("Loading order items to DuckDB...")
    conn.execute("""
        CREATE OR REPLACE TABLE raw.olist_order_items_dataset AS
        SELECT * FROM read_parquet('s3://olist-data/raw/order_items.parquet');
    """)

    # Get row counts
    customers_count = conn.execute("SELECT COUNT(*) FROM raw.olist_customers_dataset").fetchone()[0]
    orders_count = conn.execute("SELECT COUNT(*) FROM raw.olist_orders_dataset").fetchone()[0]
    items_count = conn.execute("SELECT COUNT(*) FROM raw.olist_order_items_dataset").fetchone()[0]

    conn.close()

    context.log.info(f"✅ Loaded to DuckDB: {customers_count} customers, {orders_count} orders, {items_count} items")

    return {
        "customers": customers_count,
        "orders": orders_count,
        "order_items": items_count
    }
