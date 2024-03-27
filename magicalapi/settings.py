from typing import Literal

from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    MagicalAPI library settings

    this settings can overriden by environment variables if defined.
    all of env variables should start with `MAG_` prefix.

    also the env variables are case insensitive, so the MAG_EXAMPLE, mag_example, MAG_example
    are equal.

    for example : `MAG_REQUEST_TIMEOUT`

    """

    api_key: str | None = None
    base_url: HttpUrl = "https://gw.magicalapi.com"
    retry_201_delay: int = 2  # seconds
    request_timeout: int = 15  # seconds
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] | None = None
    logging_format: str = "{asctime} [{levelname}] - {name} : {message}"

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="mag_", case_sensitive=False
    )


settings = Settings()
settings.base_url = str(settings.base_url)
