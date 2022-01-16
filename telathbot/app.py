from fastapi import FastAPI
import fastapi_plugins
from prometheus_fastapi_instrumentator import Instrumentator
from telathbot.config import (
    LocalSettings,
    TestSettings,
    DockerSettings,
)  # pylint: disable=unused-import

app = fastapi_plugins.register_middleware(FastAPI())
Instrumentator().instrument(app).expose(app)
config = fastapi_plugins.get_config()


@app.on_event("startup")
async def on_startup() -> None:
    await fastapi_plugins.config_plugin.init_app(app, config)
    await fastapi_plugins.config_plugin.init()
    await fastapi_plugins.control_plugin.init_app(
        app, version="0.1.0", environ=config.dict()
    )
    await fastapi_plugins.control_plugin.init()
    await fastapi_plugins.log_plugin.init_app(app, config=config)
    await fastapi_plugins.log_plugin.init()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await fastapi_plugins.control_plugin.terminate()
    await fastapi_plugins.log_plugin.terminate()
    await fastapi_plugins.config_plugin.terminate()


@app.get("/")
async def root():
    return dict(config)
