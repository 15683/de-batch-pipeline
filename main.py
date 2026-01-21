from dagster import Definitions

from orchestration.assets.dbt_assets import dbt_assets
from orchestration.assets.raw_ingest import raw_data_assets
from orchestration.resources import duckdb_resource, minio_resource, postgres_resource

defs = Definitions(
    assets=[
        *raw_data_assets,
        dbt_assets,
    ],
    resources={
        "postgres": postgres_resource,
        "minio": minio_resource,
        "duckdb": duckdb_resource,
    },
)
