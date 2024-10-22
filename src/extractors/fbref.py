from utils import read_config

from fbref.fbref import NavigatorRunner, Settings 


def get_crawler_settings() -> Settings:
    config = read_config()

    settings = Settings()
    crawler_settings: dict = config["fbref_extract"]["custom_config"]

    settings.setdict(crawler_settings)
    return settings

def run_crawler(collector: str, season: str) -> None:
    settings = get_crawler_settings()
    runner = NavigatorRunner(settings)
    runner.navigate(collector=collector, season=season)
    runner.start()

if __name__ == "__main__":
    settings = get_crawler_settings()

    run_crawler(collector='player_passing', season='2021')

