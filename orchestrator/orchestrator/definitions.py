from dagster import Definitions, load_assets_from_modules
from dagster_dbt import DbtCliResource

from .assets import seeds, transfermarkt
from .assets.dbt import my_dbt_assets
from .assets.fbref import generate_fbref_asset
from .constants import fbrefcollectors
from .project import dbt_project

fbref_assets = [generate_fbref_asset(collector) for collector in fbrefcollectors]
seed_assets = load_assets_from_modules([seeds], group_name="seeds")
transfermarkt_assets = load_assets_from_modules(
    [transfermarkt], group_name="transfermarkt"
)

resources = {
    "dbt": DbtCliResource(project_dir=dbt_project),
}

defs = Definitions(
    assets=[*transfermarkt_assets, *fbref_assets, *seed_assets, my_dbt_assets],
    resources=resources,
)
