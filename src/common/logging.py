import logging
import os
from datetime import datetime

import logging.handlers

LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE_CLIENT = os.path.join(
    LOG_DIR, f'client_{datetime.now().strftime("%Y%m%d")}.log'
)
LOG_FILE_COMMON = os.path.join(
    LOG_DIR, f'common_{datetime.now().strftime("%Y%m%d")}.log'
)
LOG_FILE_SERVER = os.path.join(
    LOG_DIR, f'server_{datetime.now().strftime("%Y%m%d")}.log'
)


def get_logger(
    name: str = "openbench_client", level: int = logging.INFO
) -> logging.Logger:
    if name == "openbench_client":
        LOG_FILE = LOG_FILE_CLIENT
    elif name == "openbench_common":
        LOG_FILE = LOG_FILE_COMMON
    elif name == "openbench_server":
        LOG_FILE = LOG_FILE_SERVER
    else:
        LOG_FILE = os.path.join(
            LOG_DIR, f'{name}_{datetime.now().strftime("%Y%m%d")}.log'
        )

    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        file_handler = logging.handlers.RotatingFileHandler(
            LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=5
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(level)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        logger.propagate = False
    return logger
