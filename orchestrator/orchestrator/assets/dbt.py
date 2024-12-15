import os

import duckdb
import s3fs
from dagster import AssetExecutionContext, asset
from dagster_dbt import DbtCliResource, dbt_assets, get_asset_key_for_model

from ..constants import FBREF_STATS_COLLECTORS
from ..project import dbt_project


@dbt_assets(
    manifest=dbt_project.manifest_path,
)
def my_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


fbref_models = ["__".join(["stg_fbref", model]) for model in FBREF_STATS_COLLECTORS]

# get fbref dbt models
fbref_stat_models = [
    get_asset_key_for_model([my_dbt_assets], model) for model in fbref_models
]


@asset(
    name="export_fbref_models_to_s3",
    description="Export fbref models to S3 bucket",
    compute_kind="python",
    key_prefix=["export", "fbref"],
    deps=fbref_stat_models,
    group_name="export",
)
def export_fbref_models_to_s3(context: AssetExecutionContext) -> None:
    context.log.info("Exporting fbref models to S3")
    s3_bucket = "s3://football-data-warehouse"
    fs = s3fs.S3FileSystem(
        key=os.getenv("AWS_ACCESS_KEY_ID"), secret=os.getenv("AWS_SECRET_ACCESS_KEY")
    )

    conn = duckdb.connect(str(dbt_project.project_dir / "duckdb" / "database.db"))
    tables: list[str] = [
        table[0]
        for table in conn.sql("show tables").fetchall()
        if "stg_fbref" in table[0] and "player_wage" not in table[0]
    ]

    for table in tables:
        source = table.split("_")[1]
        new_table_name = table.split("__")[1]
        path = f"{s3_bucket}/staging/{source}/{new_table_name}.parquet"
        data = conn.sql(f"select * from {table}").pl()
        with fs.open(path, "wb") as f:
            context.log.info(f"Writing {table} to {path}")
            data.write_parquet(f)


@asset(
    name="export_dbt_models_to_s3",
    description="Export dbt models to S3 bucket",
    compute_kind="python",
    key_prefix=["export"],
    deps=[my_dbt_assets],
    group_name="export",
)
def export_dbt_models_to_s3(context: AssetExecutionContext) -> None:
    context.log.info("Exporting dbt models to S3")
    conn = duckdb.connect(str(dbt_project.project_dir / "duckdb" / "database.db"))

    tables: list[str] = [table[0] for table in conn.sql("show tables").fetchall()]

    s3_bucket = "s3://football-data-warehouse"
    fs = s3fs.S3FileSystem(
        key=os.getenv("AWS_ACCESS_KEY_ID"),
        secret=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    for table in tables:
        if table.startswith("stg_"):
            source = table.split("_")[1]
            new_table_name = table.split("__")[1]
            path = f"{s3_bucket}/staging/{source}/{new_table_name}.parquet"
        else:
            path = f"{s3_bucket}/curated/{table}.parquet"

        data = conn.sql(f"select * from {table}").pl()
        with fs.open(path, "wb") as f:
            context.log.info(f"Writing {table} to {path}")
            data.write_parquet(f)
