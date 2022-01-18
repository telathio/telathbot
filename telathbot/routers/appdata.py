from ipaddress import ip_address

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from telathbot.constants import APPDATA_COLLECTION, VERSION
from telathbot.databases.mongo import DB
from telathbot.discord import send_ip_changed_notification
from telathbot.logger import LOGGER
from telathbot.models import AppData, AppDataCheckIPRequest, AppDataCheckIPResponse
from telathbot.public_ip import get_ip_address

APPDATA_ROUTER = APIRouter(prefix="/appdata", tags=["appdata"])


async def initialize():
    if await DB[APPDATA_COLLECTION].count_documents({}) == 0:
        current_ip_address = await get_ip_address()

        await DB[APPDATA_COLLECTION].insert_one(
            jsonable_encoder(
                AppData(
                    type="appdata",
                    appVersion=VERSION,
                    lastPublicIp=str(current_ip_address),
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
    ip: AppDataCheckIPRequest,  # pylint: disable=invalid-name
) -> AppDataCheckIPResponse:
    """
    Checks if IP is still valid.  Will send a Discord notification if not.
    """
    query_result = await DB[APPDATA_COLLECTION].find_one({"type": "appdata"})
    app_data = AppData(**query_result)

    if not ip.ip:
        public_ip = await get_ip_address()
    else:
        public_ip = ip_address(ip.ip)

    if app_data.lastPublicIp != public_ip:
        webhook_status = send_ip_changed_notification(new_ip=str(public_ip))
        response = AppDataCheckIPResponse(changed=True, webhook_status=webhook_status)
        await DB[APPDATA_COLLECTION].update_one(
            {"_id": app_data.id}, {"$set": {"lastPublicIp": str(public_ip)}}
        )
    else:
        response = AppDataCheckIPResponse(changed=False, webhook_status=False)

    return response
