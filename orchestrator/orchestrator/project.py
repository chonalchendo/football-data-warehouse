import os
from pathlib import Path

from dagster_dbt import DbtProject

default_path = (Path(__file__).parent.parent.parent).resolve()

root_path = os.environ.get("ROOT_PATH", default_path)
relative_path = os.path.join(root_path, "dbt")

dbt_project = DbtProject(
    project_dir=relative_path,
)
dbt_project.prepare_if_dev()
