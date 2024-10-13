from dagster import Definitions
from dagster_dbt import DbtCliResource

from .assets.dbt import my_dbt_assets
from .assets.transfermarkt import squads
from .project import dbt_project

resources = {
    "dbt": DbtCliResource(project_dir=dbt_project),
}

defs = Definitions(
    assets=[squads, my_dbt_assets],
    resources=resources,
)
