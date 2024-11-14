import argparse

from fbref.fbref import NavigatorRunner, ParquetFeed

from .settings import get_config


def run_crawler(collector: str, season: str) -> None:
    settings = get_config().fbref_extract
    feed = ParquetFeed(
        output_path=settings.FEEDS.PATH,
        format=settings.FEEDS.FORMAT,
    )
    runner = NavigatorRunner(feed=feed)
    runner.navigate(collector=collector, season=season)
    runner.start()


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--collector", type=str, required=True)
    arg_parser.add_argument("--season", type=str, required=True)
    args = arg_parser.parse_args()

    run_crawler(collector=args.collector, season=args.season)
