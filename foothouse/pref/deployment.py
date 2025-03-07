from prefect import flow
from pydantic_settings import BaseSettings

from foothouse.utils import read_requirements

SOURCE_REPO: str = "https://github.com/chonalchendo/football-data-warehouse.git"
ENTRYPOINT: str = "foothouse/pref/flows.py:transfermarkt_flow"
SEASON: int = 2024
PARAMETERS: dict = dict(season=SEASON)
DEPLOY_NAME: str = "transfermarkt-crawler"
CRON: str = "0 4 * * TUE,FRI"
JOB_VARIABLES: dict = {"pip_packages": read_requirements()}
WORK_POOL_NAME: str = "my-work-pool"


if __name__ == "__main__":
    flow.from_source(
        source=SOURCE_REPO,
        entrypoint=ENTRYPOINT,
    ).deploy(
        name=DEPLOY_NAME,
        parameters=PARAMETERS,
        work_pool_name=WORK_POOL_NAME,
        cron=CRON,
        job_variables=JOB_VARIABLES,
    )
