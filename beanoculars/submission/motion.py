import arcade
import math
from submission.gameConstants import *
import PIL


def movePlayer(sprite: arcade.sprite, dt):
    if sprite.destination != [-1, -1]:

        vector = [sprite.destination[0] - math.floor(sprite.center_x - 16) / 32,
                  sprite.destination[1] - math.floor(sprite.center_y - 16) / 32]

        if sprite.is_moving:
            if sprite.direction == 0:
                if vector[0] > 0:
                    sprite.center_x += sprite.cur_speed * dt
                    sprite.character_face_direction = LEFT_FACING
                elif vector[0] < 0:
                    if not sprite.corr_x:
                        vector[0] -= 1
                        sprite.corr_x = True
                    sprite.center_x -= sprite.cur_speed * dt
                    sprite.character_face_direction = RIGHT_FACING

            elif sprite.direction == 1:
                if vector[1] > 0:
                    sprite.center_y += sprite.cur_speed * dt
                elif vector[1] < 0:
                    if not sprite.corr_y:
                        vector[1] -= 1
                        sprite.corr_y = True
                    sprite.center_y -= sprite.cur_speed * dt

            if sprite.direction == 0:

                if abs(vector[0]) < 0.05:
                    sprite.center_x = sprite.destination[0] * 32 + 16
                    sprite.is_moving = False

            elif sprite.direction == 1:

                if abs(vector[1]) < 0.05:
                    sprite.center_y = sprite.destination[1] * 32 + 16
                    sprite.is_moving = False

            if sprite.center_x == sprite.destination[0] * 32 + 16 and sprite.center_y == sprite.destination[
                1] * 32 + 16:
                sprite.destination = [-1, -1]

        else:
            sprite.cur_pos = [math.floor((sprite.center_x - 16) / 32),
                              math.floor((sprite.center_y - 16) / 32)]

            if abs(vector[0]) > abs(vector[1]):
                sprite.direction = 0
            elif abs(vector[0]) < abs(vector[1]):
                sprite.direction = 1
            elif vector != [0, 0]:
                sprite.direction = 0

            sprite.is_moving = True

    else:
        sprite.face_character_direction = RIGHT_FACING


def moveEntities(entity_list: arcade.sprite_list, path_list: arcade.sprite_list, delta_time: float):
    for entity in entity_list:  # pour chaque entité
        position = [entity.center_x, entity.center_y]  # trouver la position actuelle (en px?)
        if arcade.get_sprites_at_point(position, path_list):
            cur_path = arcade.get_sprites_at_point(position, path_list)[0]  # trouver le sprite de chemin actuel
        else:
            position[0] += 1
            position[1] += 1
            cur_path = arcade.get_sprites_at_point(position, path_list)[0]

        path_coor = [math.floor((cur_path.center_x - 16) / 32), math.floor((cur_path.center_y - 16) / 32)]

        if path_coor in TILE_UP:
            # changer la direction vers le haut et se snap sur l'axe
            if position[0] % 32 >= 16:
                entity.center_x = path_coor[0] * 32 + 16
                entity.character_face_direction = UP_FACING
                entity.ud = True

        if path_coor in TILE_DOWN:
            # changer la direction vers le bas
            if position[0] % 32 >= 16:
                entity.center_x = path_coor[0] * 32 + 16
                entity.character_face_direction = DOWN_FACING
                entity.ud = False

        if path_coor in TILE_RIGHT:
            # changer la direction vers la droite
            if entity.character_face_direction == UP_FACING:
                if position[1] % 32 >= 16:
                    entity.center_y = path_coor[1] * 32 + 16
                    entity.character_face_direction = RIGHT_FACING

            elif entity.character_face_direction == DOWN_FACING:
                if position[1] % 32 <= 16:
                    entity.center_y = path_coor[1] * 32 + 16
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
            print('GAME OVER')
            entity.kill()
        # si le x est au delà d'un point, return True (game over)
        # sinon, return false

    return False


def updateActualPos(sprite: arcade.sprite):
    sprite.actual_cur_pos = [math.floor((sprite.center_x - 16) / 32), math.floor((sprite.center_y - 16) / 32)]
