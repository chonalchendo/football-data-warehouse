from prefect import flow

from foothouse.pref.tasks.transfermarkt import (
    run_transfermarkt_clubs_spider,
    run_transfermarkt_squads_spider,
)


@flow
def transfermarkt_flow(season: int):
    print("Running transfermarkt flow")
    run_transfermarkt_clubs_spider(season=season)
    run_transfermarkt_squads_spider(season=season)
