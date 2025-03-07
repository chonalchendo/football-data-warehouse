from prefect import task

from foothouse.extractors.transfermarkt import run_squads_spider


@task(name="Transfermarkt Squads Crawler", log_prints=True)
def run_transfermarkt_squads_spider(season: int) -> None:
    print("Running transfermarkt squads spider")
    run_squads_spider(crawler="squads", season=season)


@task(name="Transfermarkt Clubs Crawler", log_prints=True)
def run_transfermarkt_clubs_spider(season: int, log_prints=True) -> None:
    print("Running transfermarkt clubs spider")
    run_clubs_spider(crawler="clubs", season=season)
