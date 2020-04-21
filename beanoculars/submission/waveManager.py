import arcade
from random import randint

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


def getSpawnList(waveNumber: int):
    spawnList = []
    if waveNumber < PREMADE_WAVES:
        # return the premade enemies
        if waveNumber == 0:
            spawnList.append(EnemyGroup(0, E_ANT, MID_ROW, 3, 1.5))
            spawnList.append(EnemyGroup(5, E_MOSQUITO, TOP_ROW, 3, 1.5))
            spawnList.append(EnemyGroup(5, E_SPIDER, BOT_ROW, 3, 1.5))

        elif waveNumber == 1:
            spawnList.append(EnemyGroup(0, E_SPIDER, TOP_ROW, 3, 1.5))
            spawnList.append(EnemyGroup(1, E_ANT, BOT_ROW, 3, 1.5))
            spawnList.append(EnemyGroup(3, E_MOSQUITO, MID_ROW, 5, 1.5))

        elif waveNumber == 2:
            spawnList.append(EnemyGroup(0, E_ANT, TOP_ROW, 3, 1.5))
            spawnList.append(EnemyGroup(0.5, E_MOSQUITO, MID_ROW, 3, 1.5))
            spawnList.append(EnemyGroup(0.5, E_SPIDER, BOT_ROW, 3, 1.5))
            spawnList.append(EnemyGroup(14.5, E_MOSQUITO, TOP_ROW, 3, 1.5))
            spawnList.append(EnemyGroup(0.5, E_SPIDER, MID_ROW, 3, 1.5))
            spawnList.append(EnemyGroup(0.5, E_ANT, BOT_ROW, 3, 1.5))

        elif waveNumber == 3:
            spawnList.append(EnemyGroup(7.5, E_ANT, TOP_ROW, 10, 0.5))
            spawnList.append(EnemyGroup(0, E_MOSQUITO, TOP_ROW, 10, 0.5))
            spawnList.append(EnemyGroup(0, E_SPIDER, TOP_ROW, 10, 0.5))

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
        spawnList = ['Generated']
        print('Generated wave')

    if spawnList:
        return spawnList

    else:
        raise Exception('Error: cannot create a spawn list')


def decomposeSpawnList(spawnList):
    """
    Transform the spawn list in each actual enemy spawn
    """

    eachSpawnList = []
    time = 0

    for i in range(len(spawnList)):

        for j in range(spawnList[i].number):
            eachSpawnList.append(SpawnOrder(time + spawnList[i].timeB4 + spawnList[i].timeB * j, spawnList[i].e_type,
                                            spawnList[i].row))

        time += spawnList[i].timeB4

    eachSpawnList.sort(key=takeTime)
    return eachSpawnList


def manageEnemySpawn(entity_list: arcade.sprite_list, spawnList: list, time: float, delta_time: float,
                     top_coor: [int, int], mid_coor: [int, int], bot_coor: [int, int]):
    """
    Manages the spawn of enemies during the round.
    """

    time += delta_time
    poppedItems = []

    if time > 0.5:
        for i in range(len(spawnList)):
            if spawnList[i].time <= 0:
                poppedItems.append(spawnList[i])
            spawnList[i].time -= .5

        time -= .5

    for i in range(len(poppedItems)):
        doSpawn(entity_list, spawnList[i], top_coor, mid_coor, bot_coor)
        print(len(spawnList))
        print(i)
        print(spawnList.pop(i).e_type, ' spawned')

    return time
