from dagster import Definitions, load_assets_from_modules
from dagster_dbt import DbtCliResource

from .assets import seeds, transfermarkt
from .assets.dbt import my_dbt_assets
from .assets.fbref import generate_fbref_stat_asset, fbref_wage_asset
from .constants import FBREF_STATS_COLLECTORS
from .project import dbt_project
from .jobs import team_mapping_job, transfermarkt_raw_assets, fbref_raw_stats_assets

fbref_stat_assets = [
    generate_fbref_stat_asset(collector) for collector in FBREF_STATS_COLLECTORS
]
seed_assets = load_assets_from_modules([seeds])
transfermarkt_assets = load_assets_from_modules(
    [transfermarkt], group_name="transfermarkt"
)

dbt_local_resource = DbtCliResource(project_dir=dbt_project, target="local")


RESOURCES = {
    "dbt": DbtCliResource(project_dir=dbt_project),
}

defs = Definitions(
    assets=[
        *transfermarkt_assets,
        *fbref_stat_assets,
        fbref_wage_asset,
        *seed_assets,
        my_dbt_assets,
    ],
    resources=RESOURCES,
    jobs=[team_mapping_job, transfermarkt_raw_assets, fbref_raw_stats_assets],
)
