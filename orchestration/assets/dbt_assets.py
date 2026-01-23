from dagster import asset


@asset
def example_dbt_asset():
    """Placeholder for dbt assets."""
    return {"status": "ready for implementation"}

dbt_assets = example_dbt_asset
