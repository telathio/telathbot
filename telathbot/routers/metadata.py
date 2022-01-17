from fastapi import APIRouter

from telathbot.constants import VERSION
from telathbot.discord import send_ip_changed_notification
from telathbot.logger import LOGGER
from telathbot.models import Metadata
from telathbot.public_ip import get_ip_address
from telathbot.schemas import MetadataCheckIPRequest, MetadataCheckIPResponse
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
async def get_metadata() -> MetadataSchema:
    """
    Application metadata
    """
    metadata = await Metadata.find_one({"type": "metadata"})
    response = MetadataSchema(**metadata.to_mongo())

    return response


@METADATA_ROUTER.post("/check/ip")
async def check_ip(ip: MetadataCheckIPRequest) -> MetadataCheckIPResponse:
    """
    Checks if IP is still valid.  Will send a Discord notification if not.
    """
    metadata = await Metadata.find_one({"type": "metadata"})

    if not ip.ip:
        public_ip = str(await get_ip_address())
    else:
        public_ip = ip.ip

    if metadata.lastPublicIp != public_ip:
        webhook_status = send_ip_changed_notification(new_ip=public_ip)
        response = MetadataCheckIPResponse(changed=True, webhook_status=webhook_status)
        metadata.update({"lastPublicIp": public_ip})
        await metadata.commit()
    else:
        response = MetadataCheckIPResponse(changed=False, webhook_status=False)

    return response
