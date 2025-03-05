import polars as pl
from dagster import AssetExecutionContext, asset

from foothouse.extractors.transfermarkt import run_clubs_spider, run_squads_spider
from foothouse.orchestrator.partitions import SEASON_PARTITIONS


@asset(
    name="clubs",
    key_prefix=["raw", "transfermarkt"],
    compute_kind="python",
    description="Club data crawled from Transfermarkt",
    partitions_def=SEASON_PARTITIONS,
    metadata={"group": "transfermarkt", "folder": "raw"},
    io_manager_key="parquet_io_manager",
)
def clubs(context: AssetExecutionContext) -> pl.DataFrame:
    season = context.partition_key
    context.log.info(f"Creating Clubs asset for season {season}")

    run_clubs_spider("clubs", season)

    context.log.info(f"Clubs asset scraped for season {season}")

    output_path = f"data/raw/transfermarkt/{season}/clubs.parquet"
    return pl.read_parquet(output_path)


@asset(
    name="squads",
    key_prefix=["raw", "transfermarkt"],
    compute_kind="python",
    description="Squad data crawled from Transfermarkt",
    partitions_def=SEASON_PARTITIONS,
    metadata={"group": "transfermarkt", "folder": "raw"},
    io_manager_key="parquet_io_manager",
)
def squads(context: AssetExecutionContext) -> pl.DataFrame:
    season = context.partition_key
    context.log.info(f"Creating Squads asset for season {season}")

    run_squads_spider("squads", season)

    context.log.info(f"Squads asset scraped for season {season}")

    output_path = f"data/raw/transfermarkt/{season}/squads.parquet"
    return pl.read_parquet(output_path)
