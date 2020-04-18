import math
from .config import PIXELS_PER_SECOND


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def move_towards(curr_mouse, curr_position, dt):
    overall_distance = distance(*curr_mouse, *curr_position)

    if not overall_distance:
        return (0, 0)
    else:
        travel = min(overall_distance, PIXELS_PER_SECOND * dt)

        x_distance = curr_mouse[0] - curr_position[0]
        y_distance = curr_mouse[1] - curr_position[1]

        return (
            travel * x_distance / overall_distance,
            travel * y_distance / overall_distance,
        )
