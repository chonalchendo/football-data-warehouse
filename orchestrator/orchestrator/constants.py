from dagster import StaticPartitionsDefinition


FBREF_STATS_COLLECTORS = [
    "player_defense",
    "player_misc",
    "player_passing",
    "player_possession",
    "player_shooting",
    "player_keeper",
    "player_keeper_adv",
    "player_playing_time",
    "player_standard_stats",
    "player_passing_type",
    "player_gca",
]


SEASONS = ["2018", "2019", "2020", "2021", "2022", "2023"]
SEASON_PARTITIONS = StaticPartitionsDefinition(SEASONS)
