import os

from dagster import Definitions, load_assets_from_modules
from dagster_dbt import DbtCliResource

from .assets import seeds, transfermarkt
from .assets.dbt import my_dbt_assets
from .assets.fbref import generate_fbref_stat_asset, player_wages
from .constants import FBREF_STATS_COLLECTORS
from .jobs import (fbref_raw_stats_assets, fbref_raw_stats_schedule,
                   transfermarkt_raw_assets, transfermarkt_raw_schedule)
from .project import dbt_project_dir
from .resources import S3PartitionedParquetIOManager

fbref_stat_assets = [
    generate_fbref_stat_asset(collector) for collector in FBREF_STATS_COLLECTORS
]
seed_assets = load_assets_from_modules([seeds])
transfermarkt_assets = load_assets_from_modules(
    [transfermarkt],
    group_name="transfermarkt",
)

STORAGE_OPTIONS = {
    "aws_secret_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
    "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
    "aws_region": "us-east-1",
}


RESOURCES = {
    "dbt": DbtCliResource(project_dir=dbt_project_dir),
    "parquet_io_manager": S3PartitionedParquetIOManager(
        s3_bucket="football-data-warehouse",
        storage_options=STORAGE_OPTIONS,
    ),
    # "warehouse_io_manager": S3DuckDBPartitionedIOManager(
    #     duckdb_path=str(dbt_project_dir / "duckdb" / "database.db"),
    #     s3_bucket="football-data-warehouse",
    #     storage_options=STORAGE_OPTIONS,
    # ),
}

defs = Definitions(
    assets=[
        *transfermarkt_assets,
        *fbref_stat_assets,
        player_wages,
        *seed_assets,
        my_dbt_assets,
    ],
    resources=RESOURCES,
    schedules=[fbref_raw_stats_schedule, transfermarkt_raw_schedule],
    jobs=[
        transfermarkt_raw_assets,
        fbref_raw_stats_assets,
    ],
)
