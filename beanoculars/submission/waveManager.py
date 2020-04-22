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
            spawnList.append(EnemyGroup(0, E_ANT, MID_ROW, 100, .25))
            spawnList.append(EnemyGroup(0, E_MOSQUITO, TOP_ROW, 100, .25))
            spawnList.append(EnemyGroup(0, E_SPIDER, BOT_ROW, 100, .25))

        elif waveNumber == 1:
            spawnList.append(EnemyGroup(0, E_ANT, TOP_ROW, 10, 3))
            spawnList.append(EnemyGroup(0, E_MOSQUITO, MID_ROW, 10, 3))
            spawnList.append(EnemyGroup(0, E_SPIDER, BOT_ROW, 10, 3))

        elif waveNumber == 2:
            spawnList.append(EnemyGroup(0, E_ANT, TOP_ROW, 3, 1.5))
            spawnList.append(EnemyGroup(0.5, E_MOSQUITO, MID_ROW, 3, 1.5))
            spawnList.append(EnemyGroup(1, E_SPIDER, BOT_ROW, 3, 1.5))
            spawnList.append(EnemyGroup(15, E_MOSQUITO, TOP_ROW, 3, 1.5))
            spawnList.append(EnemyGroup(15.5, E_SPIDER, MID_ROW, 3, 1.5))
            spawnList.append(EnemyGroup(16, E_ANT, BOT_ROW, 3, 1.5))

        elif waveNumber == 3:
            spawnList.append(EnemyGroup(0, E_ANT, TOP_ROW, 10, 1))
            spawnList.append(EnemyGroup(7.5, E_MOSQUITO, TOP_ROW, 10, 1))
            spawnList.append(EnemyGroup(15, E_SPIDER, TOP_ROW, 10, 1))

        elif waveNumber == 4:
            spawnList.append(EnemyGroup(0, E_SPIDER, BOT_ROW, 5, 1))
            spawnList.append(EnemyGroup(0.5, E_ANT, BOT_ROW, 5, 1))
            spawnList.append(EnemyGroup(4.5, E_ANT, MID_ROW, 5, 1))
            spawnList.append(EnemyGroup(0.5, E_MOSQUITO, MID_ROW, 5, 1))
            spawnList.append(EnemyGroup(4.5, E_MOSQUITO, TOP_ROW, 5, 1))
            spawnList.append(EnemyGroup(0.5, E_SPIDER, TOP_ROW, 5, 1))

        print('Manually made wave for round: ' + str(waveNumber))

    else:
        # return the generated enemies
        for i in range(math.floor(50 + math.sqrt(waveNumber))):
            group = generateASpawn(waveNumber, timeGeneration)
            spawnList.append(group[0])
            timeGeneration = group[1]
        print('Generated wave for round: ' + str(waveNumber))

    if spawnList:
        print(type(spawnList[0]))
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
