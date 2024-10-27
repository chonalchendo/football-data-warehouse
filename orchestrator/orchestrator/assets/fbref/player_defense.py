import polars as pl
from dagster import (AssetExecutionContext, MaterializeResult, MetadataValue,
                     asset)

from src.extractors.fbref import run_crawler

from ...constants import FbrefCollector, FbrefConfig


@asset(compute_kind="python", description="Player defensive stats crawled from FBRef")
def player_defense(
    context: AssetExecutionContext, config: FbrefConfig
) -> MaterializeResult:
    context.log.info("Creating Defensive Stats asset")

    run_crawler(FbrefCollector.DEFENSE, config.season)

    context.log.info(f"Defensive Stats asset scraped for season {config.season}")

    output_path = f"data/raw/fbref/{config.season}/{FbrefCollector.DEFENSE}.parquet"
    df = pl.read_parquet(output_path)

    return MaterializeResult(
        metadata={
            "num_records": df.shape[0],
            "season": config.season,
            "preview": MetadataValue.md(df.to_pandas().head().to_markdown()),
        }
    )
