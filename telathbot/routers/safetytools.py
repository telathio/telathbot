from curses import meta
from datetime import datetime
from typing import List

from fastapi import APIRouter

from telathbot.config import get_settings
from telathbot.databases.mysql import get_latest_post_id, get_post_reactions
from telathbot.discord import send_safetytools_notification
from telathbot.enums import SafetyToolsLevels
from telathbot.models import Metadata, SafetyToolsUse
from telathbot.schemas.reaction import PostReaction

SAFETYTOOLS_ROUTER = APIRouter(prefix="/safetytools", tags=["safetytools"])


@SAFETYTOOLS_ROUTER.get("/uses/{level}", response_model=List[PostReaction])
async def get_safetytool_reactions(
    level: SafetyToolsLevels,
    last_post_id: int = 0,
    notify: bool = False,
    persist: bool = False,
) -> List[PostReaction]:
    """
    Search for uses of Safety Tools usage.
    """
    config = get_settings()
    scrape_time = datetime.utcnow()

    metadata = await Metadata.find_one({"type": "metadata"})

    # Run database queries
    if last_post_id:
        start_post_id = last_post_id
    else:
        start_post_id = metadata.lastPostId

    if level.lower() == "red":
        safetytool_uses = await get_post_reactions(
            start_post_id, config.xenforo_stop_reaction_id
        )
    else:
        safetytool_uses = []

    new_latest_post_id = await get_latest_post_id()
    metadata.update({"lastPostId": new_latest_post_id})
    await metadata.commit()

    # Handle notifications and persistence.
    for use in safetytool_uses:
        reaction_users = [
            x["username"]
            for x in use.reaction_users
            if x["reaction_id"] == config.xenforo_stop_reaction_id
        ]

        if notify:
            webhook_sent = send_safetytools_notification(
                level=SafetyToolsLevels.RED,
                post_id=use.post_id,
                thread_id=use.thread_id,
                position=use.position,
                post_user=use.username,
                reaction_users=reaction_users,
            )
        else:
            webhook_sent = False

        if persist:
            safetools_usage_record = SafetyToolsUse(
                postId=use.post_id,
                threadId=use.thread_id,
                postUser=use.username,
                reactionUsers=", ".join(reaction_users),
                notified=webhook_sent,
                dateObserved=scrape_time,
            )

            await safetools_usage_record.commit()

    return safetytool_uses
