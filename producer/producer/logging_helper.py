"""Module that configures logging"""
from datetime import datetime
from logging import (
    FileHandler,
    LoggerAdapter,
    StreamHandler,
    getLevelName,
    getLogger,
    root,
)
from os import getenv

from ecs_logging import StdlibFormatter

LOGGING_EXTRA = {"correlation_id": f"correlation_{datetime.now():%m%d%Y:%H%M}"}
LOG_LEVEL = getLevelName(getenv("LOG_LEVEL", "DEBUG"))


def setup_logging():
    """Setup logging to file and stdout as json."""
    file_handler = FileHandler("logs/producer.log")
    file_handler.setFormatter(StdlibFormatter())

    stream_handler = StreamHandler()
    stream_handler.setFormatter(StdlibFormatter())

    root.handlers = [file_handler, stream_handler]
    root.setLevel(LOG_LEVEL)

    for name in root.manager.loggerDict.keys():
        logger = getLogger(name)
        logger = LoggerAdapter(logger, LOGGING_EXTRA)
        logger.handlers = []
        logger.propagate = True
