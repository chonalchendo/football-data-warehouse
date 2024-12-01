from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets

from ..project import get_dbt_manifest_path

# from ..project import dbt_project


@dbt_assets(manifest=get_dbt_manifest_path())
def my_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
