from typing import List

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class PostReaction(BaseModel):
    post_id: int
    thread_id: int
    username: str
    reactions: dict
    reaction_users: List[dict]
