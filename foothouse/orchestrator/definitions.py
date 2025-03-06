import os

from dagster import Definitions, load_assets_from_modules
from dagster_dbt import DbtCliResource

from .assets import seeds, transfermarkt
from .assets.dbt import (
    export_dbt_models_to_s3,
    export_fbref_models_to_s3,
    my_dbt_assets,
)
from .assets.fbref import generate_fbref_stat_asset, player_wages
from .constants import FBREF_STATS_COLLECTORS
from .jobs import (
    fbref_stats_job,
    fbref_stats_schedule,
    transfermarkt_raw_assets,
    transfermarkt_raw_schedule,
)
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
}

defs = Definitions(
    assets=[
        *transfermarkt_assets,
        *fbref_stat_assets,
        player_wages,
        *seed_assets,
        my_dbt_assets,
        export_dbt_models_to_s3,
        export_fbref_models_to_s3,
    ],
    resources=RESOURCES,
    schedules=[fbref_stats_schedule, transfermarkt_raw_schedule],
    jobs=[transfermarkt_raw_assets, fbref_stats_job],
)
