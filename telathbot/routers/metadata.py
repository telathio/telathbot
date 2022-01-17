from ipaddress import ip_address
from urllib import response

from fastapi import APIRouter

from telathbot.constants import VERSION
from telathbot.logger import LOGGER
from telathbot.models import Metadata
from telathbot.public_ip import get_ip_address
from telathbot.schemas.metadata import MetadataSchema

METADATA_ROUTER = APIRouter(prefix="/metadata", tags=["metadata"])


async def initialize():
    if await Metadata.count_documents() == 0:
        ip_address = await get_ip_address()
        new_metadata = Metadata(
            type="metadata",
            appVersion=VERSION,
            lastPostId=0,
            lastPublicIp=str(ip_address),
        )
        await new_metadata.commit()
        LOGGER.info("No metadata found.  Initializing!")
    else:
        LOGGER.info("Metadata found.")


@METADATA_ROUTER.get("/", response_model=MetadataSchema)
async def get_safetytool_reactions() -> MetadataSchema:
    """
    Application metadata
    """
    metadata = await Metadata.find_one()
    response = MetadataSchema(**metadata.to_mongo())

    return response
