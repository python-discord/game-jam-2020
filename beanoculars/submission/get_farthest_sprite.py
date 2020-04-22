import arcade
from arcade.sprite_list import get_distance_between_sprites
from typing import Optional, Tuple


def get_farthest_sprite(sprite: arcade.Sprite, sprite_list: arcade.SpriteList, radius: float = -1) -> Optional[
    Tuple[arcade.Sprite, float]]:
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
    max_distance = get_distance_between_sprites(sprite, sprite_list[max_pos])
    if radius != -1:
        for i in range(1, len(sprite_list)):
            distance = get_distance_between_sprites(sprite, sprite_list[i])
            if radius > distance > max_distance:
                max_pos = i
                max_distance = distance
    else:
        for i in range(1, len(sprite_list)):
            distance = get_distance_between_sprites(sprite, sprite_list[i])
            if radius > distance > max_distance:
                max_pos = i
                max_distance = distance
    return sprite_list[max_pos], max_distance
