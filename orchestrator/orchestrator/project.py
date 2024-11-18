from pathlib import Path

from dagster_dbt import DbtProject

relative_path = (Path(__file__).parent.parent.parent / "dbt").resolve()

dbt_project = DbtProject(
    project_dir=relative_path,
)
dbt_project.prepare_if_dev()
