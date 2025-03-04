from pathlib import Path

from dagster_dbt import DbtProject

dbt_project_dir = (Path(__file__).joinpath("../../..", "dbt")).resolve()

dbt_project = DbtProject(
    project_dir=dbt_project_dir,
)
dbt_project.prepare_if_dev()
