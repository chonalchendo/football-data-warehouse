from dagster import Config


class FbrefConfig(Config):
    season: str


class FbrefCollector:
    DEFENSE = "player_defense"
    KEEPER = "player_keeper"
    KEEPER_ADVANCED = "player_keeper_adv"
    PASSING = "player_passing"
    PASSING_TYPE = "player_passing_type"
    POSSESSION = "player_possession"
    PLAYING_TIME = "player_playing_time"
    SHOOTING = "player_shooting"
    STANDARD = "player_standard"
    GCA = "player_gca"
    MISC = "player_misc"



