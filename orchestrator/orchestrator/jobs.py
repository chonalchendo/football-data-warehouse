from dagster import define_asset_job, in_process_executor

from .constants import FBREF_STATS_COLLECTORS

team_mapping_job = define_asset_job(
    name="team_mapping_job",
    selection=["squads", "player_defense", "team_mapping_asset"],
    executor_def=in_process_executor,
)

transfermarkt_raw_assets = define_asset_job(
    name="transfermarkt_raw_assets",
    selection=["squads"],
    # executor_def=in_process_executor,
)

fbref_raw_stats_assets = define_asset_job(
    name="fbref_raw_stats_assets",
    selection=FBREF_STATS_COLLECTORS,
    executor_def=in_process_executor,
)

all_raw_assets_job = define_asset_job(
    name="all_raw_assets_job",
    selection=FBREF_STATS_COLLECTORS + ["squads"],
    executor_def=in_process_executor,
)
