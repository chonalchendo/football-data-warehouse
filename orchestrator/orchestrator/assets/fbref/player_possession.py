import pandas as pd
from dagster import (AssetExecutionContext, MaterializeResult, MetadataValue,
                     asset)

from src.extractors.fbref import run_crawler

from ...constants import FbrefCollector, FbrefConfig


@asset(compute_kind="python", description="Player possession stats crawled from FBRef")
def player_possession(
    context: AssetExecutionContext, config: FbrefConfig
) -> MaterializeResult:
    context.log.info("Creating possession stats asset")

    run_crawler(FbrefCollector.POSSESSION, config.season)

    context.log.info(f"Possession stats asset scraped for season {config.season}")

    output_path = f"data/raw/fbref/{config.season}/{FbrefCollector.POSSESSION}.json.gz"
    df = pd.read_json(output_path, lines=True)

    return MaterializeResult(
        metadata={
            "num_records": len(df),
            "season": config.season,
            "preview": MetadataValue.md(df.head().to_markdown()),
        }
    )
