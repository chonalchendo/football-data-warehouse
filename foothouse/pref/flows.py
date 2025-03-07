from prefect import flow, task

from foothouse.extractors.transfermarkt import run_clubs_spider, run_squads_spider


@flow(name="Transfermarkt Flow", log_prints=True)
def transfermarkt_flow(season: int):
    print("Running transfermarkt squads spider")
    run_clubs_spider(crawler="squads", season=season)


# @task(name="Transfermarkt Squads Crawler", log_prints=True)
# def run_transfermarkt_squads_spider(season: int) -> None:
#     print("Running transfermarkt squads spider")
#     run_squads_spider(crawler="squads", season=season)
#
#
# @task(name="Transfermarkt Clubs Crawler", log_prints=True)
# def run_transfermarkt_clubs_spider(season: int) -> None:
#     print("Running transfermarkt clubs spider")
#     run_clubs_spider(crawler="clubs", season=season)


# if __name__ == "__main__":
#     transfermarkt_flow(2024)
