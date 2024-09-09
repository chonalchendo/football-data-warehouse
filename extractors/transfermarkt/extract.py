from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
from scrapy.crawler import CrawlerRunner, CrawlerProcess

from utils import read_config


def set_scrapy_settings() -> Settings:
    settings = get_project_settings()
    config = read_config()
    
    scrapy_settings: dict = config['transfermarkt_extract']['scrapy_config']

    settings.setdict(scrapy_settings)
    return settings


def run_spider(spider_name: str) -> None:
    settings = set_scrapy_settings()
    process = CrawlerProcess(settings)
    process.crawl(spider_name, leagues="bundesliga", seasons="2020")
    process.start()



if __name__ == '__main__':
    run_spider('clubs')
