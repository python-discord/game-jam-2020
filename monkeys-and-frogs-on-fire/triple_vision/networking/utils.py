from frost.client import Status
from frost.client.events import EventStatus


def get_status(name):
    status = None
    while status is None:
        status = EventStatus.get_status(name)

    return Status(status)
