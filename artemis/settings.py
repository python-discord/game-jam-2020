"""Read and write data to/from a JSON file."""
import typing

from constants import AWARDS
import utils


FILE = 'data/config.json'


def data_util(fun: typing.Callable) -> typing.Callable:
    """Use specific file."""
    return utils.data_util(fun, FILE)


@data_util
def get_sfx_volume(data: dict) -> float:
    """Check the user's sound effects volume preference."""
    return data.get('sfx_vol', 1.0)


@data_util
def set_sfx_volume(data: dict, volume: float):
    """Set sound effects volume preference."""
    data['sfx_vol'] = volume


@data_util
def get_music_volume(data: dict) -> float:
    """Check the user's music volume preference."""
    return data.get('music_vol', 1.0)


@data_util
def set_music_volume(data: dict, volume: float):
    """Set the user's music volume preference."""
    data['music_vol'] = volume