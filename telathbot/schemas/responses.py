# pylint: disable=too-few-public-methods
from pydantic import BaseModel  # pylint: disable=no-name-in-module


class HealthResponse(BaseModel):
    version: str
