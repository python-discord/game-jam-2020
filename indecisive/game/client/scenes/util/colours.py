from typing import Union


def make_colour_valid(colour: Union[int, float]) -> int:
    if colour < 0:
        return 0
    elif colour > 255:
        return 255
    else:
        return int(colour)
