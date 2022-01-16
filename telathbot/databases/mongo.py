import logging
from fastapi import Depends
import fastapi_plugins
from motor.motor_asyncio import AsyncIOMotorClient
from telathbot.constants import METADATA_COLLECTION, TELATHBOT_DB, VERSION


async def initialize(logger: logging.Logger):
    config = fastapi_plugins.get_config()
    database = AsyncIOMotorClient(config.telathbot_db_url)
    metadata_collection = database[TELATHBOT_DB][METADATA_COLLECTION]

    if await metadata_collection.count_documents({}) == 0:
        metadata = {"type": "metadata", "appVersion": VERSION, "lastPostId": 0}

        await metadata_collection.insert_one(metadata)
        logger.info("Matadata not found, inserting.")
    else:
        logger.info("Matadata already exists.")
