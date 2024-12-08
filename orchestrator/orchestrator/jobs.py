from dagster import (AssetSelection, RunRequest, define_asset_job,
                     in_process_executor, multi_or_in_process_executor,
                     schedule)

from .constants import CURRENT_SEASON

# team_mapping_job = define_asset_job(
#     name="team_mapping_job",
#     selection=["squads", "player_defense", "team_mapping_asset"],
#     executor_def=in_process_executor,
# )


transfermarkt_raw_assets = define_asset_job(
    name="transfermarkt_raw_assets",
    selection=AssetSelection.key_prefixes("raw", "transfermarkt"),
    executor_def=multi_or_in_process_executor,
)

fbref_raw_stats_assets = define_asset_job(
    name="fbref_raw_stats_assets",
    selection=AssetSelection.key_prefixes("raw", "fbref"),
    executor_def=in_process_executor,
)


@schedule(cron_schedule="0 4 * * TUE,FRI", job=transfermarkt_raw_assets)
def transfermarkt_raw_schedule():
    yield RunRequest(partition_key=CURRENT_SEASON)


@schedule(cron_schedule="0 4 * * TUE,FRI", job=fbref_raw_stats_assets)
def fbref_raw_stats_schedule():
    yield RunRequest(partition_key=CURRENT_SEASON)
