# pylint: disable=too-few-public-methods
from functools import lru_cache
from pydantic import AnyUrl, HttpUrl, BaseSettings  # pylint: disable=no-name-in-module,


@lru_cache()
def get_settings():
    return Settings()


class Settings(BaseSettings):
    api_name: str = str(__name__)

    # Xenforo
    xenforo_db_host: str
    xenforo_db_port: int = 3306
    xenforo_db_user: str
    xenforo_db_password: str
    xenforo_db_name: str
    xenforo_stop_reaction_id: int

    # Discord
    discord_webhook: HttpUrl

    # TelathBot
    telathbot_db_url: AnyUrl

    class Config:
        env_file = ".env"
