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
