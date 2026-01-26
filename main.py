from dagster import Definitions

from orchestration.assets.dbt_transformations import (
    run_dbt_marts_models,
    run_dbt_staging_models,
)
from orchestration.assets.export_to_minio import (
    export_customers_to_minio,
    export_order_items_to_minio,
    export_orders_to_minio,
)

# Import all assets
from orchestration.assets.ingest_raw_data import (
    raw_customers_to_postgres,
    raw_order_items_to_postgres,
    raw_orders_to_postgres,
)
from orchestration.assets.load_to_duckdb import load_raw_data_to_duckdb
from orchestration.resources import duckdb_resource, minio_resource, postgres_resource

defs = Definitions(
    assets=[
        raw_customers_to_postgres,
        raw_orders_to_postgres,
        raw_order_items_to_postgres,
        export_customers_to_minio,
        export_orders_to_minio,
        export_order_items_to_minio,
        load_raw_data_to_duckdb,
        run_dbt_staging_models,
        run_dbt_marts_models,
    ],
    resources={
        "postgres": postgres_resource,
        "minio": minio_resource,
        "duckdb": duckdb_resource,
    },
)
