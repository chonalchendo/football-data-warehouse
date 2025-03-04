from dagster import (AssetSelection, RunRequest, define_asset_job,
                     in_process_executor, multi_or_in_process_executor,
                     schedule)

from foothouse.orchestrator.constants import CURRENT_SEASON

transfermarkt_raw_assets = define_asset_job(
    name="transfermarkt_raw_assets",
    selection=AssetSelection.key_prefixes("raw", "transfermarkt"),
    executor_def=multi_or_in_process_executor,
)

fbref_stats_job = define_asset_job(
    name="fbref_stats_job",
    selection=AssetSelection.key_prefixes(
        ["raw", "fbref"], ["staging", "fbref"], ["export", "fbref"]
    ),
    executor_def=in_process_executor,
)


@schedule(cron_schedule="0 4 * * TUE,FRI", job=transfermarkt_raw_assets)
def transfermarkt_raw_schedule():
    yield RunRequest(partition_key=CURRENT_SEASON)


@schedule(cron_schedule="0 4 * * FRI", job=fbref_stats_job)
def fbref_stats_schedule():
    yield RunRequest(partition_key=CURRENT_SEASON)
