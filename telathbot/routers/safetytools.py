# pylint: disable=invalid-name
import json
from typing import List

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from telathbot.config import get_settings
from telathbot.constants import SAFETYTOOLS_COLLECTION
from telathbot.databases.mongo import DB
from telathbot.databases.mysql import get_post_reactions
from telathbot.discord import send_safetytools_notification
from telathbot.enums import SafetyToolsLevels
from telathbot.models import SafetyToolsNotifyResponse, SafetyToolsUse

SAFETYTOOLS_ROUTER = APIRouter(prefix="/safetytools", tags=["safetytools"])


@SAFETYTOOLS_ROUTER.post("/uses/{level}", response_model=List[SafetyToolsUse])
async def get_safetytool_uses(level: SafetyToolsLevels) -> List[SafetyToolsUse]:
    """
    Search for uses of Safety Tools usage and save to database.
    """
    config = get_settings()
    # Run database queries
    if level.lower() == "red":
        raw_safetytool_uses = await get_post_reactions(config.xenforo_stop_reaction_id)
    else:
        raw_safetytool_uses = []

    safetytool_uses = []
    # Handle notifications and persistence.
    for use in raw_safetytool_uses:
        # Check if postId already exists.
        if not await DB[SAFETYTOOLS_COLLECTION].count_documents({"post_id": use[0]}):
            reaction_users = [
                x["username"]
                for x in json.loads(use[4])
                if x["reaction_id"] == config.xenforo_stop_reaction_id
            ]

            # Mappings from database query.
            new_safetool_use = SafetyToolsUse(
                level=level,
                post_id=use[0],
                thread_id=use[1],
                post_user=use[2],
                reaction_users=reaction_users,
                position=use[5],
            )

            insert_result = await DB[SAFETYTOOLS_COLLECTION].insert_one(
                jsonable_encoder(new_safetool_use.dict())
            )
            new_safetool_use.object_id = insert_result.inserted_id
            safetytool_uses.append(new_safetool_use)

    return safetytool_uses


@SAFETYTOOLS_ROUTER.delete("/uses/{level}")
async def clear_safetytools_uses(level: SafetyToolsLevels) -> None:
    if level != SafetyToolsLevels.ALL:
        delete_filter = {"level": level}
    else:
        delete_filter = {}

    await DB[SAFETYTOOLS_COLLECTION].delete_many(delete_filter)


@SAFETYTOOLS_ROUTER.post(
    "/notify/{level}", response_model=List[SafetyToolsNotifyResponse]
)
async def notify_safetytool_uses(
    level: SafetyToolsLevels,
) -> List[SafetyToolsNotifyResponse]:
    query_filter = {"notified": False}
    if level != SafetyToolsLevels.ALL:
        query_filter["level"] = level  # type: ignore

    uses = []
    # Grab all the documents that haven't been notified.
    async for document in DB[SAFETYTOOLS_COLLECTION].find(query_filter):
        uses.append(SafetyToolsUse(**document))

    response = []
    for use in uses:
        webhook_result = send_safetytools_notification(
            level=use.level,
            post_id=use.post_id,
            thread_id=use.thread_id,
            position=use.position,
            post_user=use.post_user,
            reaction_users=use.reaction_users,
        )

        if webhook_result:
            await DB[SAFETYTOOLS_COLLECTION].update_one(
                {"_id": use.object_id}, {"$set": {"notified": True}}
            )

        response.append(
            SafetyToolsNotifyResponse(
                object_id=str(use.object_id), notified=webhook_result
            )
        )

    return response
