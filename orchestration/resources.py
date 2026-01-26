import duckdb
import psycopg2
from dagster import ConfigurableResource
from minio import Minio


class PostgresResource(ConfigurableResource):
    """PostgreSQL connection resource."""
    host: str = "postgres"
    port: int = 5432
    user: str = "dagster"
    password: str = "dagster_password"
    database: str = "postgres"

    def get_connection(self):
        """Get PostgreSQL connection."""
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )


class MinioResource(ConfigurableResource):
    """MinIO object storage resource."""
    endpoint: str = "minio:9000"
    access_key: str = "minioadmin"
    secret_key: str = "minioadmin"
    secure: bool = False

    def get_client(self):
        """Get MinIO client."""
        return Minio(
            self.endpoint,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=self.secure
        )


class DuckDBResource(ConfigurableResource):
    """DuckDB database resource."""
    database_path: str = "data/warehouse.duckdb"

    def get_connection(self):
        """Get DuckDB connection."""
        return duckdb.connect(self.database_path)


# Resource instances
postgres_resource = PostgresResource()
minio_resource = MinioResource()
duckdb_resource = DuckDBResource()
