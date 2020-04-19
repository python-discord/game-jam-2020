import math
import logging

logger = logging.getLogger()


def get_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def log_exceptions(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            raise
        except BaseException:
            logging.error("Got error!", exc_info=True)
            raise

    return inner
