from dagster import asset


@asset
def example_raw_data():
    """Placeholder for raw data ingestion."""
    return {"status": "ready for implementation"}

raw_data_assets = [example_raw_data]
