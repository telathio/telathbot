from typing import Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class MetadataCheckIPRequest(BaseModel):
    ip: Optional[str]
