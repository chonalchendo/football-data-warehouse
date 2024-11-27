import argparse

from fbref.fbref import NavigatorRunner, ParquetFeed

from .settings import get_config


def run_stats_crawler(collector: str, season: str) -> None:
    settings = get_config().fbref_extract
    feed = ParquetFeed(
        output_path=settings.FEEDS.PATH,
        format=settings.FEEDS.FORMAT,
    )
    runner = NavigatorRunner(feed=feed)
    runner.navigate(collector=collector, season=season)
    runner.start()


def run_wage_crawler(
    comp_id: int, comp_name: str, season: str, download_delay: int = 10
) -> None:
    settings = get_config().fbref_extract
    params = {"comp_id": comp_id, "comp_name": comp_name}
    feed = ParquetFeed(output_path=settings.FEEDS.PATH, format=settings.FEEDS.FORMAT)
    
    runner = NavigatorRunner(feed=feed, download_delay=download_delay)
    runner.navigate(collector="player_wages", params=params, season=season)
    runner.start()


if __name__ == "__main__":
    # arg_parser = argparse.ArgumentParser()
    # arg_parser.add_argument("--collector", type=str, required=True)
    # arg_parser.add_argument("--season", type=str, required=True)
    # args = arg_parser.parse_args()

    # run_stats_crawler(collector=args.collector, season=args.season)
    # settings = get_config().fbref_extract
    # comps = settings.COMPS

    # for comp, id in comps.items():
    #     run_wage_crawler(comp_id=id, comp_name=comp, season=2021)

    run_stats_crawler(collector='player_defense', season='2024')