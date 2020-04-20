import arcade
import math
from submission.gameConstants import *


def movePlayer(sprite: arcade.sprite, dt):
    print(sprite.destination)
    if sprite.destination != [-1, -1]:

        vector = [sprite.destination[0] - math.floor(sprite.center_x - 16) / 32,
                  sprite.destination[1] - math.floor(sprite.center_y - 16) / 32]

        if sprite.is_moving:
            if sprite.direction == 0:
                if vector[0] > 0:
                    sprite.center_x += MOVE_SPEED * dt
                    sprite.character_face_direction = LEFT_FACING
                elif vector[0] < 0:
                    if not sprite.corr_x:
                        vector[0] -= 1
                        sprite.corr_x = True
                    sprite.center_x -= MOVE_SPEED * dt
                    sprite.character_face_direction = RIGHT_FACING

            elif sprite.direction == 1:
                if vector[1] > 0:
                    sprite.center_y += MOVE_SPEED * dt
                elif vector[1] < 0:
                    if not sprite.corr_y:
                        vector[1] -= 1
                        sprite.corr_y = True
                    sprite.center_y -= MOVE_SPEED * dt

            if sprite.direction == 0:

                if abs(vector[0]) < 0.05:
                    sprite.center_x = sprite.destination[0] * 32 + 16
                    sprite.is_moving = False

            elif sprite.direction == 1:

                if abs(vector[1]) < 0.05:
                    sprite.center_y = sprite.destination[1] * 32 + 16
                    sprite.is_moving = False

            if sprite.center_x == sprite.destination[0] * 32 + 16 and sprite.center_y == sprite.destination[1] * 32 + 16:
                sprite.destination = [-1, -1]

        else:
            sprite.cur_pos = [math.floor((sprite.center_x - 16) / 32),
                              math.floor((sprite.center_y - 16) / 32)]

            if abs(vector[0]) > abs(vector[1]):
                sprite.direction = 0
            elif abs(vector[0]) < abs(vector[1]):
                sprite.direction = 1
            elif vector != [0,0]:
                sprite.direction = 0

            sprite.is_moving = True
