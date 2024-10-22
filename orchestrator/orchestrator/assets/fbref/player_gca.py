import pandas as pd
from dagster import (AssetExecutionContext, MaterializeResult, MetadataValue,
                     asset)

from src.extractors.fbref import run_crawler

from ...constants import FbrefCollector, FbrefConfig


@asset(compute_kind="python", description="Player gca stats crawled from FBRef")
def player_gca(
    context: AssetExecutionContext, config: FbrefConfig
) -> MaterializeResult:
    context.log.info("Creating gca stats asset")

    run_crawler(FbrefCollector.GCA, config.season)

    context.log.info(f"Gca stats asset scraped for season {config.season}")

    output_path = f"data/raw/fbref/{config.season}/{FbrefCollector.GCA}.json.gz"
    df = pd.read_json(output_path, lines=True)

    return MaterializeResult(
        metadata={
            "num_records": len(df),
            "season": config.season,
            "preview": MetadataValue.md(df.head().to_markdown()),
        }
    )
