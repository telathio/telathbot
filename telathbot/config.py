from functools import lru_cache
from pydantic import BaseSettings, AnyUrl, HttpUrl

@lru_cache()
def get_settings():
    return Settings()


class Settings(BaseSettings):
    # Xenforo
    xenforo_db_uri: AnyUrl
    xenforo_stop_reaction_id: int

    # Discord
    discord_webhook: HttpUrl

    # TelathBot
    telathbot_db_uri: AnyUrl

    class Config:
        env_file = ".env"
