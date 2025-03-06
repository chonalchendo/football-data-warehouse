from functools import lru_cache
from typing import Any

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class TransfermarktConfig(BaseSettings):
    SPIDER_MODULES: list[str] = ["transfermarkt"]
    NEWSPIDER_MODULE: list[str] = ["transfermarkt"]
    ROBOTSTXT_OBEY: bool = True
    DOWNLOAD_DELAY: int = 1
    COOKIES_ENABLED: bool = False
    REQUEST_FINGERPRINTER_IMPLEMENTATION: str = "2.7"
    TWISTED_REACTOR: str = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
    FEED_EXPORT_ENCODING: str = "utf-8"
    ITEM_PIPELINES: dict[str, int] = Field(
        default_factory=lambda: {
            "transfermarkt.transfermarkt.pipelines.TransfermarktParquetPipeline": 300
        }
    )
    FEEDS: dict[str, Any] = Field(
        default_factory=lambda: {
            "data/raw/transfermarkt/{season}/{name}.parquet": {"format": "parquet"}
        }
    )
    GCS_FEEDS: dict[str, Any] = Field(
        default_factory=lambda: {
            "gs://football-data-warehouse/raw/transfermarkt/{season}/{name}.parquet": {
                "format": "parquet"
            }
        }
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=True,
    )

    USER_AGENT: str
    GCP_PROJECT: str
    GCP_CREDENTIALS_PATH: str


class Feeds(BaseModel):
    PATH: str = "data/raw/fbref/{season}/{name}.parquet"
    OVERWRITE: bool = True
    ENCODING: str = "utf-8"
    FORMAT: str = "parquet"


class FBRefSettings(BaseSettings):
    COLLECTOR_MODULES: list[str] = ["fbref"]
    FEEDS: Feeds = Field(default_factory=Feeds)
    COMPS: dict[str, int] = {
        "Premier-League": 9,
        "Serie-A": 11,
        "La-Liga": 12,
        "Bundesliga": 20,
        "Ligue-1": 13,
    }

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=True,
    )

    GCP_PROJECT: str
    GCP_CREDENTIALS_PATH: str


class ScraperConfig(BaseSettings):
    transfermarkt_extract: TransfermarktConfig = Field(
        default_factory=TransfermarktConfig
    )
    fbref_extract: FBRefSettings = Field(default_factory=FBRefSettings)


@lru_cache()
def get_config() -> ScraperConfig:
    return ScraperConfig()
