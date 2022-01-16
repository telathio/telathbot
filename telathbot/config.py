# pylint: disable=no-name-in-module, too-few-public-methods
import logging
import fastapi_plugins
from pydantic import AnyUrl, HttpUrl


class DefaultSettings(fastapi_plugins.LoggingSettings):
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
    logging_level: int = logging.DEBUG
    logging_style: fastapi_plugins.LoggingStyle = fastapi_plugins.LoggingStyle.logtxt

    class Config:
        env_file = ".env"


@fastapi_plugins.registered_configuration_docker
class DockerSettings(DefaultSettings):
    pass


@fastapi_plugins.registered_configuration_local
class LocalSettings(DefaultSettings):
    pass


@fastapi_plugins.registered_configuration_test
class TestSettings(DefaultSettings):
    pass
