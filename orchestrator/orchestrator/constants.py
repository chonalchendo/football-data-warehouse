CURRENT_SEASON = "2024"

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


TMARKET_LEAGUES = ["premier-league", "la-liga", "bundesliga", "serie-a", "ligue-1"]
FBREF_LEAGUES = ["Premier League", "La Liga", "Bundesliga", "Serie A", "Ligue 1"]


class Assets:
    RAW_TRANSFERMARKT: list[str] = ["raw", "transfermarkt"]
    RAW_FBREF: list[str] = ["raw", "fbref"]
    RAW_ALL: list[str] = ["raw"]
