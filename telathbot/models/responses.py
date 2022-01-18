from pydantic import BaseModel  # pylint: disable=no-name-in-module


class HealthResponse(BaseModel):
    version: str


class AppDataCheckIPResponse(BaseModel):
    changed: bool
    webhook_status: bool
