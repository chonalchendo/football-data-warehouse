import pandas as pd
from dagster import (AssetExecutionContext, MaterializeResult, MetadataValue,
                     asset, Config)

from src.extractors.fbref import run_crawler


class FbrefConfig(Config):
    season: str


@asset(compute_kind="python", description="Player defensive stats crawled from FBRef")
def player_defense(context: AssetExecutionContext, config: FbrefConfig) -> MaterializeResult:
    context.log.info("Creating Defensive Stats asset")

    run_crawler("player_defense", config.season)

    context.log.info(f"Defensive Stats asset scraped for season {config.season}")

    output_path = f"data/raw/fbref/{config.season}/player_defense.json.gz"
    df = pd.read_json(output_path, lines=True)

    return MaterializeResult(
        metadata={
            "num_records": len(df),
            "season": config.season,
            "preview": MetadataValue.md(df.head().to_markdown()),
        }
    )


