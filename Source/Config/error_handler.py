import logging
import os
import sys

from logging.handlers import RotatingFileHandler
from Source.Config.paths import CONFIG_DIR


LOG_DIR = os.path.join(CONFIG_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")

logger = logging.getLogger("RubberDuckClock")
logger.setLevel(logging.ERROR)

logger.propagate = False


def setup_error_logging():
    os.makedirs(LOG_DIR, exist_ok=True)

    handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
        delay=True
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)


def log_exception(error_type, error, traceback):
    logger.error(
        "Unhandled exception",
        exc_info=(error_type, error, traceback)
    )


def handle_uncaught_exception(
    error_type,
    error,
    traceback
):
    log_exception(error_type, error, traceback)