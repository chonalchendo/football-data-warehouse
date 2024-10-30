import polars as pl
from dagster import (AssetExecutionContext, MaterializeResult, MetadataValue,
                     asset)

from src.extractors.fbref import run_crawler

from ..constants import FbrefConfig



def generate_fbref_asset(collector: str):
    @asset(
        name=collector, 
        compute_kind="python", 
        description=f"{collector} stats crawled from FBRef",
        group_name='fbref'
    )
    def _asset(
        context: AssetExecutionContext, config: FbrefConfig
    ) -> MaterializeResult:
        context.log.info("Creating keeper stats asset")

        run_crawler(collector, config.season)

        context.log.info(f"Keeper stats asset scraped for season {config.season}")

        output_path = f"data/raw/fbref/{config.season}/{collector}.json.gz"
        df = pl.read_ndjson(output_path)

        return MaterializeResult(
            metadata={
                "num_records": len(df),
                "season": config.season,
                "preview": MetadataValue.md(df.to_pandas().head().to_markdown()),
            }
        )   

    return _asset

