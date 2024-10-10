from dagster import Definitions, define_asset_job

from .assets.transfermarkt import squads

transfermarkt_job = define_asset_job(name='transfermarkt', selection='squads')

defs = Definitions(
        assets=[squads],
        jobs=[transfermarkt_job],
)
