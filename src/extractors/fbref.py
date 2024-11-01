import argparse

from fbref.fbref import NavigatorRunner, Settings

from utils import read_config


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
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--collector", type=str, required=True)
    arg_parser.add_argument("--season", type=str, required=True)
    args = arg_parser.parse_args()

    run_crawler(collector=args.collector, season=args.season)
