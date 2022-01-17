from typing import List

from fastapi import APIRouter

from telathbot.config import get_settings
from telathbot.databases.mysql import get_post_reactions
from telathbot.schemas.reaction import PostReaction

SAFETYTOOLS_ROUTER = APIRouter(prefix="/safetytools", tags=["safetytools"])

from enum import Enum


class SafetyToolsLevels(str, Enum):
    red = "red"
    yellow = "yellow"
    green = "green"


@SAFETYTOOLS_ROUTER.get("/uses/{level}", response_model=List[PostReaction])
async def get_safetytool_reactions(
    level: SafetyToolsLevels, last_post_id: int = 0
) -> List[PostReaction]:
    """
    Search for uses of Safety Tools usage.
    """
    config = get_settings()

    if level.lower() == "red":
        return await get_post_reactions(last_post_id, config.xenforo_stop_reaction_id)
    else:
        return []
