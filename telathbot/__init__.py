import fastapi
import fastapi_plugins
from prometheus_fastapi_instrumentator import Instrumentator

app = fastapi_plugins.register_middleware(fastapi.FastAPI())
Instrumentator().instrument(app).expose(app)

@app.on_event('startup')
async def on_startup() -> None:
    await fastapi_plugins.control_plugin.init_app(
        app,
        version='1.2.3',
    )
    await fastapi_plugins.control_plugin.init()

@app.on_event('shutdown')
async def on_shutdown() -> None:
    await fastapi_plugins.control_plugin.terminate()

@app.get("/")
async def root():
    return {"message": "Hello World"}
