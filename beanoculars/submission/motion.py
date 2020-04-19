import arcade
import math
from submission.gameConstants import MOVE_SPEED, MOVE_SPEED_CHARGED, ENTITY_MS


def movePlayer(destination: [int, int], sprite: arcade.Sprite):
    cur_pos = [int((sprite.center_x-16)/32), int((sprite.center_y-16)/32)]
    print(cur_pos, destination)
    vector = [destination[0]-cur_pos[0], destination[1]-cur_pos[1]]
    print(vector)

