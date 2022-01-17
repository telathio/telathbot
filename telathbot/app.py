from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from telathbot import constants
from telathbot.logger import init_logger
from telathbot.routers import metadata, safetytools
from telathbot.schemas.responses import HealthResponse

init_logger()
app = FastAPI()
Instrumentator().instrument(app).expose(app)


app.include_router(safetytools.SAFETYTOOLS_ROUTER)
app.include_router(metadata.METADATA_ROUTER)


@app.on_event("startup")
async def on_startup() -> None:
    await metadata.initialize()


@app.get("/health")
async def health() -> HealthResponse:
    health_response = HealthResponse(version=constants.VERSION)
    return health_response
