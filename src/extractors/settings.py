from typing import Any
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field
from functools import lru_cache


class TransfermarktConfig(BaseSettings):
    SPIDER_MODULES: list[str] = ["transfermarkt"]
    NEWSPIDER_MODULE: list[str] = ["transfermarkt"]
    USER_AGENT: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    )
    ROBOTSTXT_OBEY: bool = True
    DOWNLOAD_DELAY: int = 1
    COOKIES_ENABLED: bool = False
    REQUEST_FINGERPRINTER_IMPLEMENTATION: str = "2.7"
    TWISTED_REACTOR: str = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
    FEED_EXPORT_ENCODING: str = "utf-8"
    ITEM_PIPELINES: dict[str, int] = Field(
        default_factory=lambda: {
            "transfermarkt.transfermarkt.pipelines.TransfermarktGCSPipeline": 300
        }
    )
    FEEDS: dict[str, Any] = Field(
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

    GCP_PROJECT: str
    GCP_CREDENTIALS_PATH: str


class Feeds(BaseModel):
    PATH: str = "gs://football-data-warehouse/raw/fbref/{season}/{name}.parquet"
    OVERWRITE: bool = True
    ENCODING: str = "utf-8"
    FORMAT: str = "parquet"


class FBRefSettings(BaseSettings):
    COLLECTOR_MODULES: list[str] = ["fbref"]
    FEEDS: Feeds = Field(default_factory=Feeds)

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
