import logging
import logging.config

from src.config import config

LOGGING_FORMAT = "%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s"


def setup_logging() -> None:
    log_level = config.app.log_level

    logging.basicConfig(level=log_level, format=LOGGING_FORMAT)
