from dagster import StaticPartitionsDefinition


SEASONS = ["2018", "2019", "2020", "2021", "2022", "2023", "2024"]
SEASON_PARTITIONS = StaticPartitionsDefinition(SEASONS)
