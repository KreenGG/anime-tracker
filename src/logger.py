import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path(__file__).parent.parent / "logs"
if not Path.exists(LOG_DIR):
    Path(LOG_DIR).mkdir(parents=True)

LOG_FILE_PATH = Path(LOG_DIR) / "app.log"

LOGGING_LEVEL = logging.DEBUG
LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def setup_logging() -> None:
    logging.basicConfig(level=LOGGING_LEVEL, format=LOGGING_FORMAT)

    file_handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=10485760, backupCount=5)
    file_handler.setLevel(LOGGING_LEVEL)
    file_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))

    logging.getLogger("").addHandler(file_handler)
