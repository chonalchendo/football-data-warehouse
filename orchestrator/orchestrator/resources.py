import os


def get_gcs_storage_options() -> dict[str, str]:
    return {"google_service_account": os.environ.get("GCP_CREDENTIALS_PATH")}
