import arcade

from submission.gameConstants import *


def pickUp(sprite: arcade.sprite, path_list: arcade.sprite_list): # called when q is pressed
    """
    Manage the pick up of turrets and so on
    :param sprite: player sprite
    :return: current inventory state
    """
    if not sprite.is_moving:
        if sprite.inventory != 0: # free it
            #check if turret can be placed
            sprite.cur_speed = MOVE_SPEED # reset speed
            sprite.inventory = 0 # reset inventory
            #actually place the turret on the actual_cur_pos maybe do a new var

            return 0

        if sprite.inventory == 0:
            #check if turret underneath
            #check if turret can be picked up
            #return 0 if false
            #else
            sprite.inventory = T_SPRAY #following the actual turret
            #kill the turret instance on the ground

            sprite.cur_speed = MOVE_SPEED_CHARGED

            return sprite.inventory

    #else play sound?