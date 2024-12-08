from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets

from ..project import dbt_project


@dbt_assets(
    manifest=dbt_project.manifest_path,
    # io_manager_key="warehouse_io_manager",
)
def my_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
