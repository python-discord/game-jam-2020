import arcade
from arcade import sprite_list

from submission.gameConstants import *
from submission.loadAnimatedChars import AnimatedEntity
import math


def pickUp(sprite: arcade.sprite, player_list: arcade.sprite_list, path_list: arcade.sprite_list,
           turret_list: arcade.sprite_list):  # called when q is pressed
    """
    Manage the pick up of turrets and so on
    :param sprite: player sprite
    :return: current inventory state
    """

    if not sprite.is_moving:
        if sprite.inventory != 0:  # free it
            if not sprite.actual_cur_pos[0] > 28:  # if in town
                if not arcade.sprite_list.get_sprites_at_point([sprite.center_x, sprite.center_y],
                                                               path_list):  # check if turret can be placed
                    if not arcade.sprite_list.get_sprites_at_point([sprite.center_x, sprite.center_y],
                                                                   turret_list):
                        t_type = sprite.inventory
                        newTurret = AnimatedEntity(t_type, 2, [math.floor(sprite.center_x-16)/32,
                                                               math.floor(sprite.center_y-16)/32])
                        turret_list.append(newTurret)
                        sprite.cur_speed = MOVE_SPEED  # reset speed
                        sprite.inventory = 0  # reset inventory

            return 0

        if sprite.inventory == 0:
            if arcade.sprite_list.get_sprites_at_point([sprite.center_x, sprite.center_y],
                                                       turret_list):
                # if there's a turret under the player

                t_list = arcade.sprite_list.get_sprites_at_point([sprite.center_x, sprite.center_y], turret_list)
                # get the turrets at the player position

                sprite.inventory = t_list[0].e_type  # put the turret in  the inventory

                t_list[0].kill()  # kill picked up turret

                sprite.cur_speed = MOVE_SPEED_CHARGED  # slow down the player

                return 0  # return the inventory

    # else play sound?
