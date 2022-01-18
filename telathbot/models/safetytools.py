# pylint: disable=too-few-public-methods
from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module

from telathbot.enums import SafetyToolsLevels
from telathbot.models.validators import PyObjectId


class SafetyToolsUse(BaseModel):
    object_id: Optional[PyObjectId] = Field(alias="_id")
    level: SafetyToolsLevels
    post_id: int
    thread_id: int
    post_user: str
    reaction_users: list[str]
    position: int
    notified: bool = False
    date_observed: datetime = datetime.utcnow()

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
