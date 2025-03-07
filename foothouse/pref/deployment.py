from prefect import flow
from pydantic_settings import BaseSettings

from foothouse.utils import read_requirements

# SOURCE_REPO = "https://github.com/chonalchendo/football-data-warehouse.git"


class DeployConfig(BaseSettings):
    SOURCE_REPO: str = (
        "https://github.com/chonalchendo/football-data-warehouse/tree/development.git"
    )
    SEASON: int = 2024
    PARAMETERS: dict = dict(season=SEASON)
    DEPLOY_NAME: str = "transfermarkt-crawler"
    ENTRYPOINT: str = "foothouse/pref/flows.py:transfermarkt_flow"
    CRON: str = "0 4 * * TUE,FRI"
    JOB_VARIABLES: dict = {"pip_packages": read_requirements()}
    WORK_POOL_NAME: str = "my-work-pool"


if __name__ == "__main__":
    flow.from_source(
        source=DeployConfig.SOURCE_REPO,
        entrypoint=DeployConfig.ENTRYPOINT,
    ).deploy(
        name=DeployConfig.DEPLOY_NAME,
        parameters=DeployConfig.PARAMETERS,
        work_pool_name=DeployConfig.WORK_POOL_NAME,
        cron=DeployConfig.CRON,
        job_variables=DeployConfig.JOB_VARIABLES,
    )
