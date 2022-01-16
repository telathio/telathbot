from motor.motor_asyncio import AsyncIOMotorClient

from telathbot.config import get_settings
from telathbot.constants import METADATA_COLLECTION, TELATHBOT_DB, VERSION
from telathbot.logger import LOGGER


async def initialize():
    config = get_settings()
    database = AsyncIOMotorClient(config.telathbot_db_url)
    metadata_collection = database[TELATHBOT_DB][METADATA_COLLECTION]

    if await metadata_collection.count_documents({}) == 0:
        metadata = {"type": "metadata", "appVersion": VERSION, "lastPostId": 0}

        await metadata_collection.insert_one(metadata)
        LOGGER.info("No metadata found.  Initializing!")
    else:
        LOGGER.info("Metadata found.")
