import arcade
import math
from submission.gameConstants import *


def movePlayer(sprite: arcade.sprite, delta_time: float):
    # check si destination n'est pas set
    if sprite.destination == [-1, -1]:

        if sprite.is_moving:
            sprite.is_moving = False

    # sinon
    else:
        # moving est true

        sprite.is_moving = True

        # créer un vecteur (EN PX)
        vectorPX = [sprite.destination[0] * 32 + 16 - sprite.center_x,
                    sprite.destination[1] * 32 + 16 - sprite.center_y]

        v_sign = [0, 0]

        # (ajuster vecteur)
        for i in range(len(vectorPX)):
            if vectorPX[i] < 0:
                vectorPX[i] -= 32

        # trouver le signe du vecteur
        for i in range(len(vectorPX)):
            if vectorPX[i] < 0:
                v_sign[i] = -1
                if i == 0:
                    sprite.character_face_direction = LEFT_FACING
            elif vectorPX[i] > 0:
                v_sign[i] = 1
                if i == 0:
                    sprite.character_face_direction = RIGHT_FACING
            elif vectorPX[i] == 0:
                v_sign[i] = 0

        # bouger le sprite selon le vecteur
        if sprite.destination[0] != -1:
            sprite.center_x += (vectorPX[0] * LERP + .5 * v_sign[0]) * sprite.cur_speed * delta_time * abs(v_sign[0])
        if sprite.destination[1] != -1:
            sprite.center_y += (vectorPX[1] * LERP + .5 * v_sign[1]) * sprite.cur_speed * delta_time * abs(v_sign[1])

        # si l'on est arrivé à destination (pour chaque coor)
        if sprite.destination[0] * 32 + 16 - 2 < sprite.center_x < sprite.destination[0] * 32 + 16 + 2:
            sprite.center_x = sprite.destination[0] * 32 + 16
            sprite.destination[0] = -1

        if sprite.destination[1] * 32 + 16 - 2 < sprite.center_y < sprite.destination[1] * 32 + 16 + 2:
            sprite.center_y = sprite.destination[1] * 32 + 16
            sprite.destination[1] = -1


def moveEntities(entity_list: arcade.sprite_list, path_list: arcade.sprite_list, delta_time: float):
    for entity in entity_list:  # pour chaque entité
        position = [entity.center_x, entity.center_y]  # trouver la position actuelle (en px?)

        if entity.character_face_direction == DOWN_FACING:
            grid_pos = [math.floor((position[0] - 16) / 32), math.floor((position[1] + 16) / 32)]
        else:
            grid_pos = [math.floor((position[0] - 16) / 32), math.floor((position[1] - 16) / 32)]

        if grid_pos in TILE_UP:
            # changer la direction vers le haut et se snap sur l'axe
            if position[0] % 32 >= 16:
                entity.center_x = grid_pos[0] * 32 + 16
                entity.character_face_direction = UP_FACING
                entity.ud = True

        if grid_pos in TILE_DOWN:
            # changer la direction vers le bas
            if position[0] % 32 >= 16:
                entity.center_x = grid_pos[0] * 32 + 16
                entity.character_face_direction = DOWN_FACING
                entity.ud = False

        if grid_pos in TILE_RIGHT:
            # changer la direction vers la droite
            if entity.character_face_direction == UP_FACING:
                if position[1] % 32 >= 16:
                    entity.center_y = grid_pos[1] * 32 + 16
                    entity.character_face_direction = RIGHT_FACING

            elif entity.character_face_direction == DOWN_FACING:

                if position[1] % 32 <= 16:
                    entity.center_y = grid_pos[1] * 32 + 16
                    entity.character_face_direction = RIGHT_FACING

        # selon le chemin, si l'on a passé la moitié (utiliser modulo)
        # se repositioner sur le bon axe et changer sa direction

        if entity.character_face_direction == UP_FACING:
            # se déplacer de ms * delta_time dans la bonne direction
            entity.center_y += ENTITY_MS * delta_time

        elif entity.character_face_direction == DOWN_FACING:
            entity.center_y -= ENTITY_MS * delta_time

        elif entity.character_face_direction == RIGHT_FACING:
            entity.center_x += ENTITY_MS * delta_time

        if entity.center_x >= 32 * 31:
            entity.kill()
            return True
        # si le x est au delà d'un point, return True (game over)
        # sinon, return false

    return False


def updateActualPos(sprite: arcade.sprite):
    sprite.actual_cur_pos = [math.floor((sprite.center_x - 16) / 32), math.floor((sprite.center_y - 16) / 32)]
