import arcade

from submission.gameConstants import *
from submission.get_farthest_sprite import get_farthest_sprite
from submission.loadAnimatedChars import AnimatedDamage


def turretAttack(turret: arcade.sprite, entity_list: arcade.sprite_list, delta_time: float,
                 dmg_anim_list: arcade.sprite_list):
    if not entity_list:
        return True

    turret.cooldown += delta_time
    if not turret.target:
        turret.target = getTarget(turret, entity_list)

    elif turret.cooldown >= T_COOLDOWN:
        turret.cooldown = 0

        if turret.e_type - 9 == turret.target.e_type:
            turret.target.health -= turret.dmg * DMG_MULTIPLIER
            if turret.e_type == T_SPRAY:
                dmg_anim_list.append(AnimatedDamage("y_dmg", [turret.target.center_x, turret.target.center_y]))

            elif turret.e_type == T_LAMP:
                dmg_anim_list.append(AnimatedDamage("b_dmg", [turret.target.center_x, turret.target.center_y]))

            elif turret.e_type == T_VACUUM:
                dmg_anim_list.append(AnimatedDamage("r_dmg", [turret.target.center_x, turret.target.center_y]))

        else:
            turret.target.health -= turret.dmg
            if turret.e_type == T_SPRAY:
                dmg_anim_list.append(AnimatedDamage("y_dmg", [turret.target.center_x, turret.target.center_y], 0.5))

            elif turret.e_type == T_LAMP:
                dmg_anim_list.append(AnimatedDamage("b_dmg", [turret.target.center_x, turret.target.center_y], 0.5))

            elif turret.e_type == T_VACUUM:
                dmg_anim_list.append(AnimatedDamage("r_dmg", [turret.target.center_x, turret.target.center_y], 0.5))

        if turret.target.health <= 0:
            turret.target.kill()
            turret.target = None
            if not entity_list:
                return True

        elif arcade.get_distance_between_sprites(turret, turret.target) >= 32 * T_RANGE:
            turret.target = None


def getTarget(turret: arcade.sprite, entity_list: arcade.sprite_list):
    distance = None
    target = False
    max_x = 0
    max_x_pref = 0
    max_pos = 0
    max_pos_pref = 0

    for i in range(len(entity_list)):
        distance = arcade.get_distance_between_sprites(turret, entity_list[i])
        if not distance >= 32*T_RANGE:
            if entity_list[i].e_type == turret.e_type - 9:
                if entity_list[i].center_x > max_x_pref:
                    max_x_pref = entity_list[i].center_x
                    max_pos_pref = i
                    target = True

            elif entity_list[i].center_x > max_x:
                max_x = entity_list[i].center_x
                max_pos = i
                target = True

    if target:
        if max_x_pref != 0:
            x_sign = turret.center_x - entity_list[max_pos_pref].center_x
            y_sign = turret.center_y - entity_list[max_pos_pref].center_y
            if abs(x_sign) > abs(y_sign):
                if x_sign > 0:
                    turret.character_face_direction = RIGHT_FACING
                else:
                    turret.character_face_direction = LEFT_FACING

            if abs(x_sign) <= abs(y_sign):
                if y_sign > 0:
                    turret.character_face_direction = DOWN_FACING
                else:
                    turret.character_face_direction = UP_FACING

            return entity_list[max_pos_pref]

        elif max_x != 0:
            x_sign = turret.center_x - entity_list[max_pos].center_x
            y_sign = turret.center_y - entity_list[max_pos].center_y
            if abs(x_sign) > abs(y_sign):
                if x_sign > 0:
                    turret.character_face_direction = RIGHT_FACING
                else:
                    turret.character_face_direction = LEFT_FACING

            if abs(x_sign) <= abs(y_sign):
                if y_sign > 0:
                    turret.character_face_direction = DOWN_FACING
                else:
                    turret.character_face_direction = UP_FACING
            return entity_list[max_pos]

    else:
        return None
