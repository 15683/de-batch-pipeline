import subprocess
from pathlib import Path

from dagster import AssetExecutionContext, AssetIn, asset


@asset(
    group_name="transformation",
    ins={"duckdb_loaded": AssetIn("load_raw_data_to_duckdb")}
)
def run_dbt_staging_models(
    context: AssetExecutionContext,
    duckdb_loaded: dict
) -> dict:
    """Run dbt staging models."""

    dbt_project_dir = Path("transformation")

    context.log.info("Running dbt staging models...")

    result = subprocess.run(
        ["dbt", "run", "--select", "staging.*"],
        cwd=dbt_project_dir,
        capture_output=True,
        text=True
    )

    context.log.info(result.stdout)

    if result.returncode != 0:
        context.log.error(result.stderr)
        raise Exception("dbt staging models failed")

    context.log.info("✅ dbt staging models completed")
    return {"status": "success"}


@asset(
    group_name="transformation",
    ins={"staging_done": AssetIn("run_dbt_staging_models")}
)
def run_dbt_marts_models(
    context: AssetExecutionContext,
    staging_done: dict
) -> dict:
    """Run dbt marts models."""

    dbt_project_dir = Path("transformation")

    context.log.info("Running dbt marts models...")

    result = subprocess.run(
        ["dbt", "run", "--select", "marts.*"],
        cwd=dbt_project_dir,
        capture_output=True,
        text=True
    )

    context.log.info(result.stdout)

    if result.returncode != 0:
        context.log.error(result.stderr)
        raise Exception("dbt marts models failed")

    context.log.info("✅ dbt marts models completed")
    return {"status": "success"}
