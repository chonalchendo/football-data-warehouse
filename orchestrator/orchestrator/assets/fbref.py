import polars as pl
from dagster import (
    AssetExecutionContext,
    MaterializeResult,
    MetadataValue,
    asset,
)

from src.extractors.fbref import run_stats_crawler, run_wage_crawler
from src.extractors.settings import get_config

from ..constants import SEASON_PARTITIONS


def generate_fbref_stat_asset(collector: str):
    @asset(
        name=collector,
        compute_kind="python",
        description=f"{collector} stats crawled from Fbref",
        group_name="fbref",
        partitions_def=SEASON_PARTITIONS,
    )
    def _asset(context: AssetExecutionContext) -> MaterializeResult:
        season = context.partition_key

        context.log.info(f"Creating {collector} asset for season {season}")

        run_stats_crawler(collector, season)

        context.log.info(f"Keeper stats asset scraped for season {season}")

        output_path = f"data/raw/fbref/{season}/{collector}.parquet"
        df = pl.read_parquet(output_path)

        return MaterializeResult(
            metadata={
                "records": len(df),
                "season": season,
                "preview": MetadataValue.md(df.to_pandas().head().to_markdown()),
            }
        )

    return _asset


@asset(
    name="player_wages",
    compute_kind="python",
    description="Player wages crawled from Fbref",
    partitions_def=SEASON_PARTITIONS,
    group_name="fbref",
)
def fbref_wage_asset(context: AssetExecutionContext) -> MaterializeResult:
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
    df = pl.read_parquet(output_path)

    return MaterializeResult(
        metadata={
            "records": len(df),
            "season": season,
            "preview": MetadataValue.md(df.to_pandas().head().to_markdown()),
        }
    )
