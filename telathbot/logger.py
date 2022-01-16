import logging

import uvicorn

FORMAT: str = "%(levelprefix)s %(asctime)s | %(message)s"
LOGGER = logging.getLogger("telathbot")


def init_logger():
    LOGGER.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = uvicorn.logging.DefaultFormatter(FORMAT, datefmt="%Y-%m-%d %H:%M:%S")
    console_handler.setFormatter(formatter)
    LOGGER.addHandler(console_handler)
