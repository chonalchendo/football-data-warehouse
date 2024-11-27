import polars as pl
from dagster import (
    AssetExecutionContext,
    MaterializeResult,
    MetadataValue,
    asset,
)

from src.extractors.transfermarkt import run_clubs_spider, run_squads_spider
from ..partitions import SEASON_PARTITIONS


@asset(
    compute_kind="python",
    description="Club data crawled from Transfermarkt",
    partitions_def=SEASON_PARTITIONS,
)
def clubs(context: AssetExecutionContext) -> None:
    season = context.partition_key
    context.log.info(f"Creating Clubs asset for season {season}")

    run_clubs_spider("clubs", season)

    context.log.info(f"Clubs asset scraped for season {season}")


@asset(
    compute_kind="python",
    description="Squad data crawled from Transfermarkt",
    partitions_def=SEASON_PARTITIONS,
)
def squads(context: AssetExecutionContext) -> MaterializeResult:
    season = context.partition_key
    context.log.info(f"Creating Squads asset for season {season}")

    run_squads_spider("squads", season)

    context.log.info(f"Squads asset scraped for season {season}")

    output_path = f"data/raw/transfermarkt/{season}/squads.parquet"
    df = pl.read_parquet(output_path)

    return MaterializeResult(
        metadata={
            "records": len(df),
            "season": season,
            "preview": MetadataValue.md(df.to_pandas().head().to_markdown()),
        }
    )
