import polars as pl
from dagster import AssetExecutionContext, MaterializeResult, MetadataValue, asset

from src.extractors.fbref import run_crawler

from ..constants import season_partitions


def generate_fbref_asset(collector: str):
    @asset(
        name=collector,
        compute_kind="python",
        description=f"{collector} stats crawled from FBRef",
        group_name="fbref",
        partitions_def=season_partitions,
    )
    def _asset(context: AssetExecutionContext) -> MaterializeResult:

        season = context.partition_key

        context.log.info(f"Creating {collector} asset for season {season}")

        run_crawler(collector, season)

        context.log.info(f"Keeper stats asset scraped for season {season}")

        output_path = f"data/raw/fbref/{season}/{collector}.parquet"
        df = pl.read_parquet(output_path)

        return MaterializeResult(
            metadata={
                "num_records": len(df),
                "season": season,
                "preview": MetadataValue.md(df.to_pandas().head().to_markdown()),
            }
        )

    return _asset
