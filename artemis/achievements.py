from scores import get_scores, get_hiscore, get_seconds
from constants import ACHIEVEMENTS


def num_to_level(num, level_0=1, level_1=10, level_2=100):
    if num >= level_2:
        return 2
    if num >= level_1:
        return 1
    if num >= level_0:
        return 0
    return -1


def check_type_0():
    '''number of games'''
    return num_to_level(len(get_scores()))


def check_type_1():
    '''total points scored'''
    return num_to_level(sum(get_scores()))


def check_type_2():
    '''high score'''
    return num_to_level(get_hiscore())


def check_type_3():
    '''time played'''
    minute = 60
    hour = minute * 60
    ten_hours = hour * 10
    return num_to_level(get_seconds(), minute, hour, ten_hours)


def get_achievements():
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
