import polars as pl
from pathlib import Path

from dagster import (AssetExecutionContext, MaterializeResult, MetadataValue,
                     asset)

from src.extractors.seeds import get_fifa_codes, get_continent_name


@asset(compute_kind="python", description="FIFA country codes")
def fifa_country_catalogue(context: AssetExecutionContext) -> MaterializeResult:
    context.log.info("Creating FIFA country codes asset")

    seeds_path = (
        Path(__file__).parent.parent.parent.parent
        / "data"
        / "fifa_country_catalogue.parquet"
    ).resolve()

    if not seeds_path.exists():
        seeds_path.parent.mkdir(parents=True, exist_ok=True)

    codes = get_fifa_codes()

    data = []

    for code, name in codes.items():
        context.log.info(f"Getting continent name for {name}")
        continent_name = get_continent_name(name)
        country_dict = {"code": code, "name": name, "continent": continent_name}
        data.append(country_dict)
        

    df = pl.DataFrame(data)

    context.log.info(f"Writing FIFA country codes to {seeds_path}")
    df.write_parquet(seeds_path)

    return MaterializeResult(
        metadata={
            "num_records": df.shape[0],
            "preview": MetadataValue.md(df.to_pandas().head().to_markdown()),
        }
    )


