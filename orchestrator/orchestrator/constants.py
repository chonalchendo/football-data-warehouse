from dagster import Config


class FbrefConfig(Config):
    season: str


fbrefcollectors = [
    'player_defense',
    'player_misc',
    'player_passing',
    'player_possession',
    'player_shooting',
    'player_keeper',
    'player_keeper_adv',
    'player_playing_time',
    'player_standard_stats',
    'player_passing_type',
    'player_gca'
]

