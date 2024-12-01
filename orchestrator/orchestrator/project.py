import os
from pathlib import Path

# from dagster_dbt import DbtProject
from dagster_dbt import DbtCliResource

dbt_project_dir = (Path(__file__).joinpath("../..", "dbt")).resolve()

dbt = DbtCliResource(
    project_dir=os.fspath(dbt_project_dir),
    profiles_dir=os.fspath(dbt_project_dir),
)


def get_dbt_manifest_path() -> Path:
    if os.getenv("DAGSTER_DBT_PARSE_PROJECT_ON_LOAD"):
        dbt_parse_invocation = dbt.cli(["parse"], manifest={}).wait()
        dbt_manifest_path = dbt_parse_invocation.target_path.joinpath("manifest.json")
    else:
        dbt_manifest_path = dbt_project_dir.joinpath("target", "manifest.json")
    return dbt_manifest_path


# root_path = os.environ.get("ROOT_PATH", default_path)
# relative_path = os.path.join(root_path, "dbt")

# def get_manifest_path() -> Path:
#     if os.getenv("DAGSTER_DBT_PARSE_PROJECT_ON_LOAD"):
#         dbt_parse_invocation = dbt.cli(["parse"], manifest={}).wait()
#         dbt_manifest_path = dbt_parse_invocation.target_path.joinpath("manifest.json")
#     else:
#         dbt_manifest_path = dbt_project_dir.joinpath("target", "manifest.json")
#     return dbt_manifest_path
# dbt_project = DbtProject(
#     project_dir=dbt_project_dir,
# )
# dbt_project.prepare_if_dev()
