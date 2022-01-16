# type: ignore
# Ignore until mypy fixes Py3.10 case support
from typing import List
from fastapi import APIRouter
from telathbot.config import get_settings
from telathbot.databases.mysql import get_post_reactions
from telathbot.models.reaction import PostReaction


SAFETYTOOLS_ROUTER = APIRouter(prefix="/safetytools", tags=["safetytools"])


@SAFETYTOOLS_ROUTER.get("/{type}", response_model=List[PostReaction])
async def get_safetytool_reactions(type: str) -> List[PostReaction]:
    config = get_settings()

    if type.lower() == "red":
        return await get_post_reactions(0, config.xenforo_stop_reaction_id)
    else:
        return []
