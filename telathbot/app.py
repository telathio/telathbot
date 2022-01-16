from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from telathbot.databases.mongo import initialize
from telathbot.logger import init_logger
from telathbot.routers import safetytools

init_logger()
app = FastAPI()
Instrumentator().instrument(app).expose(app)


app.include_router(safetytools.SAFETYTOOLS_ROUTER)


@app.on_event("startup")
async def on_startup() -> None:
    await initialize()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    pass


@app.get("/")
async def root():
    return {"Hello": "World!"}
