import asyncio

from motor.motor_asyncio import AsyncIOMotorClient
from umongo.frameworks import MotorAsyncIOInstance

from telathbot.config import get_settings
from telathbot.constants import TELATHBOT_DB

CLIENT = AsyncIOMotorClient(get_settings().telathbot_db_url)
CLIENT.get_io_loop = asyncio.get_running_loop
DB = CLIENT[TELATHBOT_DB]

UMONGO = MotorAsyncIOInstance(DB)
