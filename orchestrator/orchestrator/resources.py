import os

from dagster_dbt import DbtCliResource

from .project import dbt_project_dir

# def get_gcs_storage_options() -> dict[str, str]:
#     return {"google_service_account": os.environ.get("GCP_CREDENTIALS_PATH")}


RESOURCES = {
    "dbt": DbtCliResource(project_dir=os.fspath(dbt_project_dir)),
}
