import os
from math import floor
from itertools import zip_longest
from pathlib import Path

import arcade


def sweep_trace(
    sprite: arcade.Sprite,
    dir_x: int,
    dir_y: int,
    collide_with: arcade.SpriteList,
    reset_pos: bool = True,
) -> bool:
    """Do a sweep trace and check for collisions. True if collision."""
    prev_x = sprite.left
    prev_y = sprite.bottom
    default_x = sprite.left
    default_y = sprite.bottom
    for x, y in zip_longest(
        range(floor(sprite.left), floor(sprite.left + dir_x)),
        range(floor(sprite.bottom), floor(sprite.bottom + dir_y)),
    ):
        sprite.left = x if x else prev_x
        sprite.bottom = y if y else prev_y
        if x:
            prev_x = x
        if y:
            prev_y = y
        if sprite.collides_with_list(collide_with):
            sprite.left = default_x
            sprite.bottom = default_y
            return True
    if reset_pos:
        sprite.left = default_x
        sprite.bottom = default_y
    return False


class AnimLoader:
    def __init__(self, base_dir: str, **kwargs):
        self.cache = {}
        self.base_dir = Path(base_dir)
        self.kwargs = kwargs

    def load_anim(self, name):
        self.cache[name] = []
        path = self.base_dir / name
        for frame in sorted([f for f in os.listdir(path.as_posix()) if os.path.isfile(path / f)]):
            self.cache[name].append(arcade.load_texture(path / frame, **self.kwargs))

    def __getattr__(self, item):
        if item not in self.cache:
            self.load_anim(item)
        return self.cache[item]
