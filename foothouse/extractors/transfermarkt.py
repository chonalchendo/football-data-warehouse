from pathlib import Path

import polars as pl
from rich import print
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

from foothouse.extractors.settings import get_config


def set_scrapy_settings() -> Settings:
    settings = get_project_settings()
    config = get_config()

    scrapy_settings = config.transfermarkt_extract.model_dump(exclude=None)

    print(scrapy_settings)

    settings.setdict(scrapy_settings)
    return settings


def run_clubs_spider(crawler: str, season: str) -> None:
    settings = set_scrapy_settings()
    process = CrawlerProcess(settings)

    process.crawl(crawler, season=season, leagues="all")
    process.start()


def run_squads_spider(crawler: str, season: str) -> None:
    settings = set_scrapy_settings()
    process = CrawlerProcess(settings)

    clubs_path = Path(f"data/raw/transfermarkt/{season}/clubs.parquet").resolve()
    clubs_df = pl.read_parquet(clubs_path, use_pyarrow=True)

    clubs = clubs_df.to_dicts()

    process.crawl(crawler, season=season, clubs=clubs)
    process.start()
