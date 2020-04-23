import arcade
from arcade.sprite_list import get_distance_between_sprites
from typing import Optional, Tuple


def get_farthest_sprite(sprite: arcade.Sprite, sprite_list: arcade.SpriteList, radius: float = -1): #-> Optional[
    #Tuple[arcade.Sprite, float]]:
    """
    Given a Sprite and SpriteList, returns the closest sprite, and its distance.

    :param Sprite sprite: Target sprite
    :param SpriteList sprite_list: List to search for closest sprite.
    :param float radius: Maximum radius around the sprite in which we search for another sprite, optional

    :return: Farthest sprite.
    :rtype: Sprite
    """
    if len(sprite_list) == 0:
        return None

    max_pos = 0
    max_distance = -1

    if radius != -1:
        for i in range(1, len(sprite_list)):
            distance = sprite_list[i].center_x
            if radius > distance > max_distance:
                max_pos = i
                max_distance = distance

    if max_distance == -1:
        return None

    return sprite_list[max_pos], max_distance
