from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

from utils import read_config


def set_scrapy_settings() -> Settings:
    settings = get_project_settings()
    config = read_config()

    scrapy_settings: dict = config["transfermarkt_extract"]["scrapy_config"]

    settings.setdict(scrapy_settings)
    return settings


def run_spider(crawler: str, season: str) -> None:
    settings = set_scrapy_settings()
    process = CrawlerProcess(settings)
    process.crawl(crawler, season=season)
    process.start()
