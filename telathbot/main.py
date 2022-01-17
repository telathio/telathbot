import uvicorn

from telathbot import app
from telathbot.config import get_settings

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
