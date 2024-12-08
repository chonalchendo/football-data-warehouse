import time

import polars as pl
from dagster import AssetExecutionContext, asset

from src.extractors.fbref import run_stats_crawler, run_wage_crawler
from src.extractors.settings import get_config

from ..partitions import SEASON_PARTITIONS


def generate_fbref_stat_asset(collector: str):
    @asset(
        name=collector,
        key_prefix=["raw", "fbref"],
        group_name="fbref",
        compute_kind="python",
        description=f"{collector} stats crawled from Fbref",
        partitions_def=SEASON_PARTITIONS,
        metadata={"group": "fbref", "folder": "raw"},
        io_manager_key="parquet_io_manager",
    )
    def _asset(context: AssetExecutionContext) -> pl.DataFrame:
        season = context.partition_key

        context.log.info(f"Creating {collector} asset for season {season}")
        time.sleep(5)
        run_stats_crawler(collector, season)

        context.log.info(f"Keeper stats asset scraped for season {season}")

        output_path = f"data/raw/fbref/{season}/{collector}.parquet"
        return pl.read_parquet(output_path)

    return _asset


@asset(
    name="player_wages",
    key_prefix=["raw", "fbref"],
    group_name="fbref",
    compute_kind="python",
    description="Player wages crawled from Fbref",
    partitions_def=SEASON_PARTITIONS,
    metadata={"group": "fbref", "folder": "raw"},
    io_manager_key="parquet_io_manager",
)
def player_wages(context: AssetExecutionContext) -> pl.DataFrame:
    season = context.partition_key

    context.log.info(f"Creating fbref wage asset for season {season}")

    settings = get_config().fbref_extract
    comps = settings.COMPS

    for comp, id in comps.items():
        context.log.info(
            f"Collecting wage data for: league - {comp} & season - {season}"
        )
        run_wage_crawler(comp_id=id, comp_name=comp, season=season)

    output_path = f"data/raw/fbref/{season}/player_wage*.parquet"
    return pl.read_parquet(output_path)
