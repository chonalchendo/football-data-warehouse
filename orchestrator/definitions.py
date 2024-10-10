from dagster import Definitions

from .assets.transfermarkt import clubs, squads


defs = Definitions(
        assets=[clubs, squads],
)
