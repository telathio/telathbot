from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from telathbot import constants
from telathbot.databases.mongo import initialize
from telathbot.logger import init_logger
from telathbot.models.responses import HealthResponse
from telathbot.routers import safetytools

init_logger()
app = FastAPI()
Instrumentator().instrument(app).expose(app)


app.include_router(safetytools.SAFETYTOOLS_ROUTER)


@app.on_event("startup")
async def on_startup() -> None:
    await initialize()


@app.get("/health")
async def health() -> HealthResponse:
    health_response = HealthResponse(version=constants.VERSION)
    return health_response
