import arcade
import math
from submission.gameConstants import *

def move(sprite: arcade.sprite):
    order = sprite.order
    #move

def movePlayer(destination: [int, int], sprite: arcade.sprite, delta_time: float):
    if destination == [-1, -1]:
        return True

    cur_pos = [math.floor(sprite.center_x - 16) / 3, math.floor(sprite.center_y - 16) / 32]
    print(cur_pos)
    vector = [destination[0] - cur_pos[0], destination[1] - cur_pos[1]]

    if vector == [0, 0]:
        destination = [-1,-1]
        return True

    if sprite.is_moving == False:
        if vector[0] >= vector[1]:
            sprite.order = [1, 0]
        elif vector[0] < vector[1]:
            sprite.order = [0, 1]

        sprite.is_moving = True

    sprite.order = move(sprite)

    if sprite.order == []:
        sprite.is_moving == False