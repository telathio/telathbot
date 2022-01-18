import logging

import uvicorn

FORMAT: str = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
LOGGER = logging.getLogger("telathbot")


def init_logger():
    LOGGER.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = uvicorn.logging.DefaultFormatter(FORMAT)
    console_handler.setFormatter(formatter)
    LOGGER.addHandler(console_handler)
