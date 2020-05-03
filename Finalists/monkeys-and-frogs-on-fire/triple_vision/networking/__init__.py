from triple_vision.networking.client import Client
from triple_vision.networking.utils import get_status

client = Client()
client.connect()

__all__ = ('client', 'get_status')
