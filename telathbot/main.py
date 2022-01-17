import uvicorn

from telathbot import app
from telathbot.config import get_settings

if __name__ == "__main__":
    config = get_settings()
    uvicorn.run(app, host="0.0.0.0", port=config.telathbot_port)
