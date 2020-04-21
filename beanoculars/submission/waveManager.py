import arcade
from random import randint

from submission.gameConstants import *


class EnemyGroup:
    def __init__(self, timeBefore: float, e_type: int, row: int, number: int, timeBetween: float):
        self.timeB4 = timeBefore
        self.timeB = timeBetween
        self.e_type = e_type
        self.number = number
        self.row = row


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
            spawnList.append(EnemyGroup(0.5, E_ANT, MID_ROW, 3, 1.5))
            spawnList.append(EnemyGroup(0.5, E_ANT, BOT_ROW, 3, 1.5))
            spawnList.append(EnemyGroup(14.5, E_ANT, TOP_ROW, 3, 1.5))
            spawnList.append(EnemyGroup(0.5, E_ANT, MID_ROW, 3, 1.5))
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
            spawnList.append(EnemyGroup(0.5, E_SPIDER, MID_ROW, 5, 1))

        print('Manually made wave for round: ' + str(waveNumber))
        print(spawnList)
        print(len(spawnList))

    else:
        # return the generated enemies
        spawnList = ['Generated']
        print('Generated wave')

    if spawnList:
        return spawnList

    else:
        raise Exception('Error: cannot create a spawn list')


def manageEnemySpawn(spawnList: list):
    """
    Manages the spawn of enemies during the round.
    """
    pass
