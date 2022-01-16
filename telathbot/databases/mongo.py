import logging
from fastapi import Depends
import fastapi_plugins
from motor.motor_asyncio import AsyncIOMotorClient
from telathbot.config import DefaultSettings
from telathbot.constants import METADATA_COLLECTION, TELATHBOT_DB, VERSION


def mongo_client(settings: DefaultSettings = Depends(fastapi_plugins.get_config)):
    return AsyncIOMotorClient(settings.telathbot_db_url)


async def initialize(
    settings: DefaultSettings = Depends(fastapi_plugins.get_config),
    logger: logging.Logger = Depends(fastapi_plugins.depends_logging),
):
    database = mongo_client(settings)
    metadata_collection = database[TELATHBOT_DB][METADATA_COLLECTION]

    if await metadata_collection.count_documents() == 0:
        metadata = {"type": "metadata", "appVersion": VERSION, "lastPostId": 0}

        await metadata_collection.insert_one(metadata)
        logger.debug("Matadata not found, inserting.")
    else:
        logger.debug("Matadata already exists.")
