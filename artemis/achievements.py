"""Functions to check which achievements have been achieved."""
import typing

from constants import ACHIEVEMENTS
from scores import get_hiscore, get_scores, get_seconds


number = typing.Union[float, int]


def num_to_level(num: number, level_0: number = 1, level_1: number = 10,
                 level_2: number = 100) -> int:
    """Get level from score/number.

    Given some number num, determine which is the highest level it is
    higher than.
    """
    if num >= level_2:
        return 2
    if num >= level_1:
        return 1
    if num >= level_0:
        return 0
    return -1


def check_type_0() -> int:
    """Check level for achievement type 0: number of games."""
    return num_to_level(len(get_scores()))


def check_type_1() -> int:
    """Check level for achievement type 1: total points scored."""
    return num_to_level(sum(get_scores()))


def check_type_2() -> int:
    """Check level for achievement type 2: high score."""
    return num_to_level(get_hiscore())


def check_type_3() -> int:
    """Check level for achievement type 3: total time played."""
    minute = 60
    hour = minute * 60
    ten_hours = hour * 10
    return num_to_level(get_seconds(), minute, hour, ten_hours)


def get_achievements() -> list:
    """Get a list of lists of achievements."""
    checked = []
    checks = [check_type_0, check_type_1, check_type_2, check_type_3]
    for achv_type, check in zip(ACHIEVEMENTS, checks):
        level = check()
        checked.append([])
        for n, achv in enumerate(achv_type):
            copy = dict(achv)
            copy['achieved'] = n <= level
            copy['type'] = checks.index(check)
            copy['level'] = n
            checked[-1].append(copy)
    return checked
