from dagster import ConfigurableResource


class PostgresResource(ConfigurableResource):
    """PostgreSQL connection resource."""
    host: str = "postgres"
    port: int = 5432
    user: str = "dagster"
    password: str = "dagster_password"
    database: str = "dagster"

class MinioResource(ConfigurableResource):
    """MinIO object storage resource."""
    endpoint: str = "minio:9000"
    access_key: str = "minioadmin"
    secret_key: str = "minioadmin"

class DuckDBResource(ConfigurableResource):
    """DuckDB database resource."""
    database_path: str = "data/warehouse.duckdb"

# Resource instances
postgres_resource = PostgresResource()
minio_resource = MinioResource()
duckdb_resource = DuckDBResource()
