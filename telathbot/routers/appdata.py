from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from telathbot.constants import APPDATA_COLLECTION, VERSION
from telathbot.databases.mongo import DB
from telathbot.discord import send_ip_changed_notification
from telathbot.logger import LOGGER
from telathbot.models import AppData
from telathbot.public_ip import get_ip_address
from telathbot.schemas import MetadataCheckIPRequest, MetadataCheckIPResponse

APPDATA_ROUTER = APIRouter(prefix="/appdata", tags=["appdata"])


async def initialize():
    if await DB[APPDATA_COLLECTION].count_documents({}) == 0:
        ip_address = await get_ip_address()

        await DB[APPDATA_COLLECTION].insert_one(
            jsonable_encoder(
                AppData(
                    type="appdata",
                    appVersion=VERSION,
                    lastPostId=0,
                    lastPublicIp=str(ip_address),
                ).dict()
            )
        )

        LOGGER.info("No app data found.  Initializing!")
    else:
        query_response = await DB[APPDATA_COLLECTION].find_one({"type": "appdata"})
        app_data = AppData(**query_response)
        await DB[APPDATA_COLLECTION].update_one(
            {"_id": app_data.id}, {"$set": {"appVersion": VERSION}}
        )

        LOGGER.info("App data found, updating")


@APPDATA_ROUTER.get("/", response_model=AppData)
async def get_metadata() -> AppData:
    """
    Application metadata
    """
    metadata = await DB[APPDATA_COLLECTION].find_one({"type": "appdata"})
    response = AppData(**metadata)

    return response


@APPDATA_ROUTER.post("/check/ip")
async def check_ip(
    ip: MetadataCheckIPRequest,  # pylint: disable=invalid-name
) -> MetadataCheckIPResponse:
    """
    Checks if IP is still valid.  Will send a Discord notification if not.
    """
    query_result = await DB[APPDATA_COLLECTION].find_one({"type": "appdata"})
    app_data = AppData(**query_result)

    if not ip.ip:
        public_ip = await get_ip_address()
    else:
        public_ip = ip.ip

    if app_data.lastPublicIp != public_ip:
        webhook_status = send_ip_changed_notification(new_ip=public_ip)
        response = MetadataCheckIPResponse(changed=True, webhook_status=webhook_status)
        await DB[APPDATA_COLLECTION].update_one(
            {"_id": app_data.id}, {"$set": {"lastPublicIp": public_ip}}
        )
    else:
        response = MetadataCheckIPResponse(changed=False, webhook_status=False)

    return response
