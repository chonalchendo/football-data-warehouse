from pathlib import Path

import polars as pl
from dagster import (AssetExecutionContext, MaterializeResult, MetadataValue,
                     asset)

from src.extractors.seeds import (create_team_name_mapping, get_continent_name,
                                  get_fifa_codes)

from ..constants import FBREF_LEAGUES, TMARKET_LEAGUES


@asset(compute_kind="python", description="FIFA country codes", group_name="fbref")
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


@asset(
    compute_kind="python",
    description="Team mapping from fbref to transfermarkt",
    group_name="fbref",
    deps=["player_defense", "squads"],
)
def team_mapping_asset(context: AssetExecutionContext) -> MaterializeResult:
    context.log.info("Creating team mapping for fbref assets")

    data_path = Path("data").resolve()

    seeds_path = data_path / "team_mapping.parquet"

    fbref_path = data_path / "raw" / "fbref" / "*" / "player_defense.parquet"
    tmarket_path = data_path / "raw" / "transfermarkt" / "*" / "squads.parquet"

    fbref_df = pl.read_parquet(fbref_path)
    tmarket_df = pl.read_parquet(tmarket_path)

    def league_partition_team_mapping(fbref_league, tmarket_league) -> pl.DataFrame:
        subset_fbref = fbref_df.filter(pl.col("comp") == fbref_league)
        subset_tmarket = tmarket_df.filter(pl.col("league") == tmarket_league)

        fbref_squads = subset_fbref["squad"].unique().to_list()
        tmarket_squads = subset_tmarket["squad"].unique().to_list()

        return create_team_name_mapping(
            source_names=fbref_squads, target_names=tmarket_squads
        )

    mapping_df = pl.concat(
        [
            league_partition_team_mapping(
                fbref_league=fbref_league, tmarket_league=tmarket_league
            )
            for fbref_league, tmarket_league in zip(FBREF_LEAGUES, TMARKET_LEAGUES)
        ]
    )

    mapping_df.write_parquet(seeds_path)

    return MaterializeResult(
        metadata={
            "records": mapping_df.shape[0],
            "preview": MetadataValue.md(mapping_df.to_pandas().head().to_markdown()),
        }
    )
