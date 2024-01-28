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

    base_url: HttpUrl = "https://gw.magicalapi.com"
    retry_201_delay: int = 2  # seconds
    request_timeout : int = 15 # seconds

    model_config = SettingsConfigDict(env_prefix="MAG_", case_sensitive=False)


settings = Settings()