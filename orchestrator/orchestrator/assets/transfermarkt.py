import pandas as pd
from dagster import (AssetExecutionContext, MaterializeResult, MetadataValue,
                     asset, Config)

from src.extractors.transfermarkt import run_spider


class TransfermarktConfig(Config):
    season: str


@asset(compute_kind="python", description="Club data crawled from Transfermarkt")
def clubs(context: AssetExecutionContext, config: TransfermarktConfig) -> None:
    context.log.info("Creating Clubs asset")

    run_spider("clubs", config.season)

    context.log.info(f"Clubs asset scraped for season {config.season}")


@asset(compute_kind="python", description="Squad data crawled from Transfermarkt")
def squads(context: AssetExecutionContext, config: TransfermarktConfig) -> MaterializeResult:
    context.log.info("Creating Squads asset")

    run_spider("squads", config.season)

    context.log.info(f"Squads asset scraped for season {config.season}")

    output_path = f"data/raw/transfermarkt/{config.season}/squads.json.gz"

    df = pd.read_json(output_path, lines=True)

    return MaterializeResult(
        metadata={
            "num_records": len(df),
            "season": config.season,
            "preview": MetadataValue.md(df.head().to_markdown()),
        }
    )
