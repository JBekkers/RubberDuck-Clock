import time


APP_START_TIME = time.monotonic()


def get_session_uptime():

    return time.monotonic() - APP_START_TIME