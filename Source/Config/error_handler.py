import logging
import os

from logging.handlers import RotatingFileHandler

from Source.Config.paths import CONFIG_DIR


LOG_DIR = os.path.join(CONFIG_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")

logger = logging.getLogger("RubberDuckClock")
logger.setLevel(logging.ERROR)
logger.propagate = False


class OldestFirstRotatingFileHandler(RotatingFileHandler):

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None

        oldest = f"{self.baseFilename}.{self.backupCount}"

        if os.path.exists(oldest):
            os.remove(oldest)

        for index in range(
            self.backupCount - 1,
            0,
            -1
        ):
            source = f"{self.baseFilename}.{index}"
            destination = f"{self.baseFilename}.{index + 1}"

            if os.path.exists(source):
                os.replace(
                    source,
                    destination
                )

        if os.path.exists(self.baseFilename):
            os.replace(
                self.baseFilename,
                f"{self.baseFilename}.1"
            )

        if not self.delay:
            self.stream = self._open()


def setup_error_logging():

    if logger.handlers:
        return

    os.makedirs(
        LOG_DIR,
        exist_ok=True
    )

    handler = OldestFirstRotatingFileHandler(
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


def log_exception(
    error_type,
    error,
    traceback
):
    logger.error(
        "Unhandled exception",
        exc_info=(
            error_type,
            error,
            traceback
        )
    )


def handle_uncaught_exception(
    error_type,
    error,
    traceback
):
    log_exception(
        error_type,
        error,
        traceback
    )