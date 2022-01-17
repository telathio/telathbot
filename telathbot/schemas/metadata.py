# pylint: disable=too-few-public-methods
from typing import Optional

from bson import ObjectId
from pydantic import (  # pylint: disable=no-name-in-module
    BaseModel,
    Field,
    IPvAnyAddress,
)

from telathbot.schemas.validators import PyObjectId


class MetadataSchema(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    type: str
    appVersion: str
    lastPostId: int
    lastPublicIp: IPvAnyAddress

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
