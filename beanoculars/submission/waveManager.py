import arcade
from random import randint
import math

from submission.gameConstants import *
from submission.loadAnimatedChars import AnimatedEntity


class EnemyGroup:
    def __init__(self, timeBefore: float, e_type: int, row: int, number: int, timeBetween: float):
        self.timeB4 = timeBefore
        self.timeB = timeBetween
        self.e_type = e_type
        self.number = number
        self.row = row


class SpawnOrder:
    def __init__(self, time: float, e_type: int, row: int):
        self.time = time
        self.e_type = e_type
        self.row = row


def takeTime(spOr: SpawnOrder):
    return spOr.time


def doSpawn(entity_list: arcade.sprite_list, spOr: SpawnOrder, top_coor: [int, int], mid_coor: [int, int],
            bot_coor: [int, int]):
    if spOr.row == TOP_ROW:
        entity_list.append(AnimatedEntity(spOr.e_type, top_coor))

    elif spOr.row == MID_ROW:
        entity_list.append(AnimatedEntity(spOr.e_type, mid_coor))

    elif spOr.row == BOT_ROW:
        entity_list.append(AnimatedEntity(spOr.e_type, bot_coor))


def generateASpawn(num: int, timeSinceFirst: float):
    row = randint(0, 2)
    e_type = randint(1, 3)

    if num < 65:
        rdm = randint(0, 4)
    if num >= 65:
        rdm = randint(0, 3)
    if num >= 85:
        rdm = randint(0, 2)

    if rdm == 0:
        timeBetween = 0.5
    if rdm == 1:
        timeBetween = 1
    if rdm == 2:
        timeBetween = 1.5
    if rdm == 3:
        timeBetween = 3
    if rdm == 4:
        timeBetween = 5

    if num < 75:
        rdm = randint(0, 5)
    if num >= 75:
        rdm = randint(0, 4)
    if num >= 100:
        rdm = randint(0, 3)

    if rdm == 0 or rdm == 1:
        timeB4 = timeSinceFirst
    if rdm == 2:
        timeB4 = timeSinceFirst + 1
    if rdm == 3:
        timeB4 = timeSinceFirst + 2
    if rdm == 4:
        timeB4 = timeSinceFirst + 3
    if rdm == 5:
        timeB4 = timeSinceFirst + 5

    timeSinceFirst = timeB4

    number = 1 + randint(2, math.floor(math.sqrt(num)))

    return [EnemyGroup(timeB4, e_type, row, number, timeBetween), timeSinceFirst]


def getSpawnList(waveNumber: int, timeGeneration: float):
    spawnList = []
    if waveNumber < PREMADE_WAVES:
        # return the premade enemies
        if waveNumber == 0:
            spawnList.append(EnemyGroup(0, E_ANT, MID_ROW, 1, 1))

        elif waveNumber == 1:
            spawnList.append(EnemyGroup(0, E_MOSQUITO, BOT_ROW, 1, 1))

        elif waveNumber == 2:
            spawnList.append(EnemyGroup(0, E_SPIDER, TOP_ROW, 1, 1))

        elif waveNumber == 3:
            spawnList.append(EnemyGroup(0, E_ANT, TOP_ROW, 1, 1))
            spawnList.append(EnemyGroup(0, E_ANT, MID_ROW, 1, 1))
            spawnList.append(EnemyGroup(0, E_ANT, BOT_ROW, 1, 1))

        elif waveNumber == 4:
            spawnList.append(EnemyGroup(0, E_MOSQUITO, BOT_ROW, 3, 1))
            spawnList.append(EnemyGroup(3, E_ANT, TOP_ROW, 3, 1))
            spawnList.append(EnemyGroup(6, E_SPIDER, MID_ROW, 3, 1))

        elif waveNumber == 5:
            spawnList.append(EnemyGroup(0, E_ANT, BOT_ROW, 10, 1))
            spawnList.append(EnemyGroup(1, E_MOSQUITO, TOP_ROW, 10, 1))
            spawnList.append(EnemyGroup(2, E_SPIDER, MID_ROW, 10, 1))

        elif waveNumber == 6:
            spawnList.append(EnemyGroup(0, E_ANT, TOP_ROW, 3, 1.5))
            spawnList.append(EnemyGroup(0.5, E_MOSQUITO, MID_ROW, 3, 1.5))
            spawnList.append(EnemyGroup(1, E_SPIDER, BOT_ROW, 3, 1.5))
            spawnList.append(EnemyGroup(10, E_MOSQUITO, TOP_ROW, 3, 1.5))
            spawnList.append(EnemyGroup(10.5, E_SPIDER, MID_ROW, 3, 1.5))
            spawnList.append(EnemyGroup(11, E_ANT, BOT_ROW, 3, 1.5))

        elif waveNumber == 7:
            spawnList.append(EnemyGroup(0, E_ANT, TOP_ROW, 10, 1))
            spawnList.append(EnemyGroup(7.5, E_MOSQUITO, TOP_ROW, 10, 1))
            spawnList.append(EnemyGroup(15, E_SPIDER, TOP_ROW, 10, 1))

        elif waveNumber == 8:
            spawnList.append(EnemyGroup(0, E_ANT, TOP_ROW, 10, 2))
            spawnList.append(EnemyGroup(0, E_SPIDER, TOP_ROW, 20, 1))
            spawnList.append(EnemyGroup(1, E_MOSQUITO, BOT_ROW, 10, 0.75))

        elif waveNumber == 9:
            spawnList.append(EnemyGroup(0, E_MOSQUITO, TOP_ROW, 10, 1))
            spawnList.append(EnemyGroup(0.5, E_SPIDER, TOP_ROW, 10, 1))

        elif waveNumber == 10:
            spawnList.append(EnemyGroup(0, E_SPIDER, BOT_ROW, 10, 1))
            spawnList.append(EnemyGroup(0.5, E_ANT, BOT_ROW, 10, 1))

        elif waveNumber == 11:
            spawnList.append(EnemyGroup(0, E_SPIDER, MID_ROW, 15, 0.8))
            spawnList.append(EnemyGroup(10, E_ANT, MID_ROW, 15, 0.8))
            spawnList.append(EnemyGroup(20, E_MOSQUITO, MID_ROW, 15, 0.8))

        elif waveNumber == 12:
            spawnList.append(EnemyGroup(0, E_SPIDER, MID_ROW, 20, 1))
            spawnList.append(EnemyGroup(0, E_MOSQUITO, MID_ROW, 20, 1))
            spawnList.append(EnemyGroup(0, E_ANT, MID_ROW, 20, 1))

        elif waveNumber == 13:
            spawnList.append(EnemyGroup(0, E_ANT, TOP_ROW, 10, 1.5))
            spawnList.append(EnemyGroup(3, E_MOSQUITO, BOT_ROW, 10, 1.5))
            spawnList.append(EnemyGroup(6, E_SPIDER, MID_ROW, 10, 1.5))

            spawnList.append(EnemyGroup(21, E_ANT, BOT_ROW, 10, 1.5))
            spawnList.append(EnemyGroup(15, E_MOSQUITO, MID_ROW, 10, 1.5))
            spawnList.append(EnemyGroup(18, E_SPIDER, TOP_ROW, 10, 1.5))

            spawnList.append(EnemyGroup(31, E_ANT, MID_ROW, 10, 1.5))
            spawnList.append(EnemyGroup(28, E_MOSQUITO, TOP_ROW, 10, 1.5))
            spawnList.append(EnemyGroup(25, E_SPIDER, BOT_ROW, 10, 1.5))

        elif waveNumber == 14:
            spawnList.append(EnemyGroup(0, E_MOSQUITO, TOP_ROW, 10, 1))
            spawnList.append(EnemyGroup(0.5, E_SPIDER, TOP_ROW, 10, 1))

            spawnList.append(EnemyGroup(4, E_ANT, BOT_ROW, 10, 1))
            spawnList.append(EnemyGroup(4.5, E_SPIDER, BOT_ROW, 10, 1))

        elif waveNumber == 15:
            spawnList.append(EnemyGroup(10, E_SPIDER, TOP_ROW, 10, 0.25))
            spawnList.append(EnemyGroup(10, E_ANT, BOT_ROW, 10, 0.25))
            spawnList.append(EnemyGroup(10, E_MOSQUITO, MID_ROW, 10, 0.25))

        elif waveNumber == 16:
            spawnList.append(EnemyGroup(0, E_SPIDER, BOT_ROW, 10, 0.5))
            spawnList.append(EnemyGroup(0, E_ANT, MID_ROW, 10, 0.5))
            spawnList.append(EnemyGroup(0, E_MOSQUITO, TOP_ROW, 10, 0.5))

            spawnList.append(EnemyGroup(15, E_SPIDER, BOT_ROW, 10, 0.5))
            spawnList.append(EnemyGroup(15, E_ANT, MID_ROW, 10, 0.5))
            spawnList.append(EnemyGroup(15, E_MOSQUITO, TOP_ROW, 10, 0.5))

            spawnList.append(EnemyGroup(30, E_SPIDER, BOT_ROW, 10, 0.5))
            spawnList.append(EnemyGroup(30, E_ANT, MID_ROW, 10, 0.5))
            spawnList.append(EnemyGroup(30, E_MOSQUITO, TOP_ROW, 10, 0.5))

        elif waveNumber == 17:
            spawnList.append(EnemyGroup(0, E_SPIDER, TOP_ROW, 10, 1))
            spawnList.append(EnemyGroup(0, E_ANT, MID_ROW, 20, 1))
            spawnList.append(EnemyGroup(0, E_MOSQUITO, BOT_ROW, 10, 1))

            spawnList.append(EnemyGroup(6, E_MOSQUITO, TOP_ROW, 10, 1))
            spawnList.append(EnemyGroup(6, E_SPIDER, BOT_ROW, 10, 1))

        elif waveNumber == 18:
            spawnList.append(EnemyGroup(0, E_SPIDER, TOP_ROW, 5, 0.5))
            spawnList.append(EnemyGroup(0.25, E_ANT, TOP_ROW, 5, 0.5))

            spawnList.append(EnemyGroup(3, E_ANT, BOT_ROW, 5, 0.5))
            spawnList.append(EnemyGroup(3.25, E_MOSQUITO, BOT_ROW, 5, 0.5))

            spawnList.append(EnemyGroup(6, E_MOSQUITO, MID_ROW, 5, 0.5))
            spawnList.append(EnemyGroup(6.25, E_SPIDER, MID_ROW, 5, 0.5))

            spawnList.append(EnemyGroup(7, E_ANT, MID_ROW, 5, 0.5))

        elif waveNumber == 19:
            spawnList.append(EnemyGroup(0, E_ANT, TOP_ROW, 10, 0.75))
            spawnList.append(EnemyGroup(0.25, E_MOSQUITO, TOP_ROW, 10, 0.75))
            spawnList.append(EnemyGroup(0.5, E_SPIDER, TOP_ROW, 10, 0.75))

            spawnList.append(EnemyGroup(5, E_ANT, BOT_ROW, 5, 3))
            spawnList.append(EnemyGroup(5, E_MOSQUITO, BOT_ROW, 5, 3))
            spawnList.append(EnemyGroup(5, E_SPIDER, BOT_ROW, 5, 3))

        elif waveNumber == 20:
            spawnList.append(EnemyGroup(0, E_ANT, MID_ROW, 2, 0.75))
            spawnList.append(EnemyGroup(0.25, E_MOSQUITO, MID_ROW, 2, 0.75))
            spawnList.append(EnemyGroup(0.5, E_SPIDER, MID_ROW, 2, 0.75))

            spawnList.append(EnemyGroup(3, E_ANT, TOP_ROW, 2, 0.75))
            spawnList.append(EnemyGroup(3.25, E_MOSQUITO, TOP_ROW, 2, 0.75))
            spawnList.append(EnemyGroup(3.5, E_SPIDER, TOP_ROW, 2, 0.75))

            spawnList.append(EnemyGroup(6, E_ANT, BOT_ROW, 2, 0.75))
            spawnList.append(EnemyGroup(6.25, E_MOSQUITO, BOT_ROW, 2, 0.75))
            spawnList.append(EnemyGroup(6.5, E_SPIDER, BOT_ROW, 2, 0.75))

        elif waveNumber == 21:
            spawnList.append(EnemyGroup(0, E_ANT, TOP_ROW, 10, 0.25))
            spawnList.append(EnemyGroup(3, E_ANT, MID_ROW, 10, 0.25))
            spawnList.append(EnemyGroup(6, E_ANT, BOT_ROW, 10, 0.25))

        elif waveNumber == 22:
            spawnList.append(EnemyGroup(0, E_ANT, TOP_ROW, 10, 0.25))
            spawnList.append(EnemyGroup(0, E_MOSQUITO, MID_ROW, 10, 0.25))
            spawnList.append(EnemyGroup(3, E_ANT, BOT_ROW, 10, 0.5))

        elif waveNumber == 23:
            spawnList.append(EnemyGroup(0, E_ANT, BOT_ROW, 5, 0.5))
            spawnList.append(EnemyGroup(0.25, E_MOSQUITO, BOT_ROW, 5, 0.5))

            spawnList.append(EnemyGroup(3, E_ANT, TOP_ROW, 5, 0.5))
            spawnList.append(EnemyGroup(3.25, E_MOSQUITO, TOP_ROW, 5, 0.5))

            spawnList.append(EnemyGroup(6, E_ANT, MID_ROW, 5, 0.5))
            spawnList.append(EnemyGroup(6.25, E_MOSQUITO, MID_ROW, 5, 0.5))

        elif waveNumber == 24:
            spawnList.append(EnemyGroup(0, E_SPIDER, MID_ROW, 100, 0.75))

        elif waveNumber == 25:
            spawnList.append(EnemyGroup(0, E_MOSQUITO, BOT_ROW, 100, 0.75))

        elif waveNumber == 26:
            spawnList.append(EnemyGroup(0, E_ANT, BOT_ROW, 100, 0.75))
            spawnList.append(EnemyGroup(55, E_MOSQUITO, TOP_ROW, 10, 0.1))

        elif waveNumber == 27:
            spawnList.append(EnemyGroup(0, E_ANT, TOP_ROW, 10, 0.25))
            spawnList.append(EnemyGroup(0, E_MOSQUITO, MID_ROW, 10, 0.25))
            spawnList.append(EnemyGroup(3, E_ANT, BOT_ROW, 15, 0.5))

        elif waveNumber == 28:
            spawnList.append(EnemyGroup(0, E_ANT, TOP_ROW, 2, 0.75))
            spawnList.append(EnemyGroup(0.25, E_MOSQUITO, TOP_ROW, 2, 0.75))
            spawnList.append(EnemyGroup(0.5, E_SPIDER, TOP_ROW, 2, 0.75))

            spawnList.append(EnemyGroup(2, E_ANT, BOT_ROW, 2, 0.75))
            spawnList.append(EnemyGroup(2.25, E_MOSQUITO, BOT_ROW, 2, 0.75))
            spawnList.append(EnemyGroup(2.5, E_SPIDER, BOT_ROW, 2, 0.75))

            spawnList.append(EnemyGroup(4, E_ANT, MID_ROW, 2, 0.75))
            spawnList.append(EnemyGroup(4.25, E_MOSQUITO, MID_ROW, 2, 0.75))
            spawnList.append(EnemyGroup(4.5, E_SPIDER, MID_ROW, 2, 0.75))

        elif waveNumber == 29:
            spawnList.append(EnemyGroup(0, E_ANT, MID_ROW, 10, 1))
            spawnList.append(EnemyGroup(0.25, E_MOSQUITO, MID_ROW, 15, 2 / 3))
            spawnList.append(EnemyGroup(5, E_SPIDER, MID_ROW, 20, 0.5))

        elif waveNumber == 30:
            spawnList.append(EnemyGroup(0, E_SPIDER, BOT_ROW, 15, 0.1))

        elif waveNumber == 31:
            spawnList.append(EnemyGroup(0, E_MOSQUITO, TOP_ROW, 15, 0.1))

        elif waveNumber == 32:
            spawnList.append(EnemyGroup(0, E_ANT, MID_ROW, 15, 0.1))

        elif waveNumber == 33:
            spawnList.append(EnemyGroup(0, E_SPIDER, TOP_ROW, 10, 0.75))
            spawnList.append(EnemyGroup(0.25, E_ANT, TOP_ROW, 10, 0.75))
            spawnList.append(EnemyGroup(0.5, E_MOSQUITO, TOP_ROW, 10, 0.75))

        elif waveNumber == 34:
            spawnList.append(EnemyGroup(10, E_SPIDER, TOP_ROW, 10, 0.25))
            spawnList.append(EnemyGroup(10, E_ANT, BOT_ROW, 10, 0.25))
            spawnList.append(EnemyGroup(10, E_MOSQUITO, MID_ROW, 10, 0.25))

        elif waveNumber == 35:
            spawnList.append(EnemyGroup(0, E_ANT, TOP_ROW, 10, 0.25))
            spawnList.append(EnemyGroup(3, E_ANT, MID_ROW, 10, 0.25))
            spawnList.append(EnemyGroup(6, E_ANT, BOT_ROW, 10, 0.25))

        elif waveNumber == 36:
            spawnList.append(EnemyGroup(0, E_ANT, TOP_ROW, 5, 1))
            spawnList.append(EnemyGroup(0, E_MOSQUITO, BOT_ROW, 5, 1))
            spawnList.append(EnemyGroup(2, E_SPIDER, MID_ROW, 5, 1))
            spawnList.append(EnemyGroup(2.25, E_MOSQUITO, MID_ROW, 5, 1))
            spawnList.append(EnemyGroup(2.5, E_ANT, MID_ROW, 5, 1))

        elif waveNumber == 37:
            spawnList.append(EnemyGroup(2, E_ANT, TOP_ROW, 15, 2))
            spawnList.append(EnemyGroup(6, E_MOSQUITO, MID_ROW, 15, 2))
            spawnList.append(EnemyGroup(10, E_SPIDER, BOT_ROW, 15, 2))

        elif waveNumber == 38:
            spawnList.append(EnemyGroup(2, E_ANT, TOP_ROW, 15, 1))
            spawnList.append(EnemyGroup(4, E_MOSQUITO, MID_ROW, 15, 1))
            spawnList.append(EnemyGroup(6, E_SPIDER, BOT_ROW, 15, 1))

        elif waveNumber == 39:

            spawnList.append(EnemyGroup(2, E_ANT, TOP_ROW, 15, 0.5))
            spawnList.append(EnemyGroup(2, E_MOSQUITO, MID_ROW, 15, 0.5))
            spawnList.append(EnemyGroup(2, E_SPIDER, BOT_ROW, 15, 0.5))

        elif waveNumber == 40:
            spawnList.append(EnemyGroup(4, E_ANT, BOT_ROW, 10, 0.3))
            spawnList.append(EnemyGroup(4, E_MOSQUITO, MID_ROW, 15, 0.3))
            spawnList.append(EnemyGroup(4, E_SPIDER, TOP_ROW, 10, 0.3))

        elif waveNumber == 41:
            spawnList.append(EnemyGroup(0, E_SPIDER, TOP_ROW, 10, 0.75))
            spawnList.append(EnemyGroup(0.25, E_ANT, TOP_ROW, 10, 0.75))
            spawnList.append(EnemyGroup(0.5, E_MOSQUITO, TOP_ROW, 10, 0.75))

            spawnList.append(EnemyGroup(10, E_MOSQUITO, BOT_ROW, 10, 0.25))
            spawnList.append(EnemyGroup(10.25, E_ANT, BOT_ROW, 10, 0.25))
            spawnList.append(EnemyGroup(10.5, E_SPIDER, BOT_ROW, 10, 0.25))

        elif waveNumber == 42:
            spawnList.append(EnemyGroup(2, E_ANT, TOP_ROW, 15, 2))
            spawnList.append(EnemyGroup(6, E_MOSQUITO, MID_ROW, 15, 2))
            spawnList.append(EnemyGroup(10, E_SPIDER, BOT_ROW, 15, 2))

        elif waveNumber == 43:
            spawnList.append(EnemyGroup(0, E_ANT, TOP_ROW, 30, 1))
            spawnList.append(EnemyGroup(0, E_MOSQUITO, BOT_ROW, 30, 1))

            spawnList.append(EnemyGroup(0, E_SPIDER, MID_ROW, 10, 0.5))
            spawnList.append(EnemyGroup(5.5, E_SPIDER, TOP_ROW, 10, 0.5))
            spawnList.append(EnemyGroup(10.5, E_SPIDER, BOT_ROW, 10, 0.5))
            spawnList.append(EnemyGroup(20.5, E_SPIDER, BOT_ROW, 10, 1))
            spawnList.append(EnemyGroup(20.5, E_SPIDER, TOP_ROW, 10, 1))

        elif waveNumber == 44:
            spawnList.append(EnemyGroup(0, E_ANT, TOP_ROW, 5, 0.75))
            spawnList.append(EnemyGroup(0, E_MOSQUITO, MID_ROW, 5, 0.75))
            spawnList.append(EnemyGroup(0, E_SPIDER, TOP_ROW, 5, 0.1))

            spawnList.append(EnemyGroup(5, E_ANT, TOP_ROW, 5, 0.75))
            spawnList.append(EnemyGroup(5, E_MOSQUITO, MID_ROW, 5, 0.75))
            spawnList.append(EnemyGroup(5, E_SPIDER, MID_ROW, 5, 0.1))

            spawnList.append(EnemyGroup(10, E_ANT, TOP_ROW, 5, 0.1))
            spawnList.append(EnemyGroup(10, E_MOSQUITO, MID_ROW, 5, 0.75))
            spawnList.append(EnemyGroup(10, E_SPIDER, BOT_ROW, 5, 0.75))

        elif waveNumber == 45:
            spawnList.append(EnemyGroup(0, E_ANT, TOP_ROW, 10, 0.5))
            spawnList.append(EnemyGroup(0.25, E_MOSQUITO, TOP_ROW, 10, 0.5))

            spawnList.append(EnemyGroup(5, E_SPIDER, BOT_ROW, 10, 0.5))
            spawnList.append(EnemyGroup(5.25, E_MOSQUITO, BOT_ROW, 10, 0.5))

            spawnList.append(EnemyGroup(12, E_SPIDER, BOT_ROW, 10, 0.5))
            spawnList.append(EnemyGroup(12.25, E_ANT, BOT_ROW, 10, 0.5))

        elif waveNumber == 46:
            spawnList.append(EnemyGroup(0, E_ANT, TOP_ROW, 10, 0.1))
            spawnList.append(EnemyGroup(1, E_SPIDER, MID_ROW, 10, 0.1))
            spawnList.append(EnemyGroup(0, E_ANT, BOT_ROW, 10, 0.1))

        elif waveNumber == 47:
            spawnList.append(EnemyGroup(0, E_ANT, BOT_ROW, 12, 0.5))
            spawnList.append(EnemyGroup(10, E_ANT, TOP_ROW, 12, 0.5))
            spawnList.append(EnemyGroup(20, E_ANT, MID_ROW, 12, 0.5))

            spawnList.append(EnemyGroup(35, E_ANT, BOT_ROW, 12, 0.5))
            spawnList.append(EnemyGroup(45, E_ANT, TOP_ROW, 12, 0.5))
            spawnList.append(EnemyGroup(55, E_ANT, MID_ROW, 12, 0.5))

            spawnList.append(EnemyGroup(70, E_ANT, TOP_ROW, 12, 0.4))
            spawnList.append(EnemyGroup(70, E_MOSQUITO, MID_ROW, 12, 0.4))
            spawnList.append(EnemyGroup(70, E_SPIDER, BOT_ROW, 12, 0.4))

        elif waveNumber == 48:
            spawnList.append(EnemyGroup(5, E_ANT, BOT_ROW, 1, 1))
            spawnList.append(EnemyGroup(5, E_MOSQUITO, MID_ROW, 1, 1))
            spawnList.append(EnemyGroup(5, E_SPIDER, TOP_ROW, 1, 1))

            spawnList.append(EnemyGroup(10, E_ANT, MID_ROW, 3, 1))
            spawnList.append(EnemyGroup(10, E_MOSQUITO, TOP_ROW, 3, 1))
            spawnList.append(EnemyGroup(10, E_SPIDER, BOT_ROW, 3, 1))

        elif waveNumber == 49:
            spawnList.append(EnemyGroup(5, E_SPIDER, TOP_ROW, 5, 1))
            spawnList.append(EnemyGroup(5, E_ANT, MID_ROW, 5, 1))
            spawnList.append(EnemyGroup(5, E_MOSQUITO, BOT_ROW, 5, 1))

            spawnList.append(EnemyGroup(15, E_SPIDER, BOT_ROW, 5, 0.5))
            spawnList.append(EnemyGroup(15, E_ANT, MID_ROW, 5, 1))
            spawnList.append(EnemyGroup(15, E_MOSQUITO, TOP_ROW, 5, 0.5))

            spawnList.append(EnemyGroup(20, E_SPIDER, TOP_ROW, 10, 0.25))
            spawnList.append(EnemyGroup(20, E_MOSQUITO, BOT_ROW, 10, 0.25))

            spawnList.append(EnemyGroup(35, E_SPIDER, MID_ROW, 35, 0.75))
            spawnList.append(EnemyGroup(35, E_ANT, TOP_ROW, 10, 0.1))
            spawnList.append(EnemyGroup(35, E_MOSQUITO, BOT_ROW, 10, 0.1))

            spawnList.append(EnemyGroup(45, E_ANT, BOT_ROW, 10, 0.1))
            spawnList.append(EnemyGroup(45, E_MOSQUITO, TOP_ROW, 10, 0.1))

            spawnList.append(EnemyGroup(75, E_ANT, TOP_ROW, 20, 1))
            spawnList.append(EnemyGroup(75, E_MOSQUITO, MID_ROW, 20, 1))
            spawnList.append(EnemyGroup(75, E_SPIDER, BOT_ROW, 20, 1))

            spawnList.append(EnemyGroup(100, E_MOSQUITO, TOP_ROW, 20, 0.5))
            spawnList.append(EnemyGroup(100, E_SPIDER, MID_ROW, 20, 0.5))
            spawnList.append(EnemyGroup(100, E_ANT, BOT_ROW, 20, 0.5))

    else:
        # return the generated enemies
        for i in range(math.floor(math.sqrt(waveNumber))):
            group = generateASpawn(waveNumber, timeGeneration)
            spawnList.append(group[0])
            timeGeneration = group[1]

    if spawnList:
        return spawnList

    else:
        raise Exception('Error: cannot create a spawn list')


def decomposeSpawnList(spawnList):
    """
    Transform the spawn list in each actual enemy spawn
    """
    eachSpawnList = []

    for i in range(len(spawnList)):
        for j in range(spawnList[i].number):
            eachSpawnList.append(SpawnOrder(spawnList[i].timeB4 + spawnList[i].timeB * j, spawnList[i].e_type,
                                            spawnList[i].row))

    eachSpawnList.sort(key=takeTime)

    return eachSpawnList


def manageEnemySpawn(entity_list: arcade.sprite_list, spawnList: list, time: float, delta_time: float,
                     top_coor: [int, int], mid_coor: [int, int], bot_coor: [int, int]):
    """
    Manages the spawn of enemies during the round.
    """

    time += delta_time
    poppedItems = []

    for i in range(len(spawnList)):
        if time > spawnList[i].time:
            poppedItems.append(spawnList[i])

    for i in range(len(poppedItems)):
        doSpawn(entity_list, spawnList[i], top_coor, mid_coor, bot_coor)

    for i in poppedItems:
        spawnList.remove(i)

    return time
