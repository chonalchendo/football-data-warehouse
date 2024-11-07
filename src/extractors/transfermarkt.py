from rich import print
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

from .settings import get_config


def set_scrapy_settings() -> Settings:
    settings = get_project_settings()
    config = get_config()

    scrapy_settings = config.transfermarkt_extract.model_dump(exclude=None)

    print(scrapy_settings)

    settings.setdict(scrapy_settings)
    return settings


def run_spider(crawler: str, season: str) -> None:
    settings = set_scrapy_settings()
    process = CrawlerProcess(settings)
    process.crawl(crawler, season=season)
    process.start()


if __name__ == "__main__":
    run_spider("squads", "2021")
