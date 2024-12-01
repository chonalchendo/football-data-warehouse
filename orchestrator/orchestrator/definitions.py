from dagster import Definitions, load_assets_from_modules

from .assets import seeds, transfermarkt
from .assets.dbt import my_dbt_assets
from .assets.fbref import fbref_wage_asset, generate_fbref_stat_asset
from .constants import FBREF_STATS_COLLECTORS
from .jobs import (all_raw_assets_job, fbref_raw_stats_assets,
                   team_mapping_job, transfermarkt_raw_assets)
# from .project import dbt_project
from .resources import RESOURCES

# from dagster_dbt import DbtCliResource


fbref_stat_assets = [
    generate_fbref_stat_asset(collector) for collector in FBREF_STATS_COLLECTORS
]
seed_assets = load_assets_from_modules([seeds])
transfermarkt_assets = load_assets_from_modules(
    [transfermarkt], group_name="transfermarkt"
)


# RESOURCES = {
#     "dbt": DbtCliResource(project_dir=dbt_project),
# }

defs = Definitions(
    assets=[
        *transfermarkt_assets,
        *fbref_stat_assets,
        fbref_wage_asset,
        *seed_assets,
        my_dbt_assets,
    ],
    resources=RESOURCES,
    jobs=[
        team_mapping_job,
        transfermarkt_raw_assets,
        fbref_raw_stats_assets,
        all_raw_assets_job,
    ],
)
