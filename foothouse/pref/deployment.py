from prefect import flow

SOURCE_REPO = "https://github.com/chonalchendo/football-data-warehouse.git"
SEASON = 2024

if __name__ == "__main__":
    flow.from_source(
        source=SOURCE_REPO,
        entrypoint="foothouse/pref/flows.py:transfermarkt_flow",
    ).deploy(
        name="transfermarkt-crawler",
        parameters=dict(season=SEASON),
        work_pool_name="my-work-pool",
        cron="0 4 * * TUE,FRI",
    )
