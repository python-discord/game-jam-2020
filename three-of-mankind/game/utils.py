import os
from math import floor
from itertools import zip_longest
from pathlib import Path
from typing import Tuple

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


def check_touch(sprite, geometry, x, y):
    sprite.center_x += x
    sprite.center_y += y
    out = len(sprite.collides_with_list(geometry)) > 0
    sprite.center_x -= x
    sprite.center_y -= y
    return out


def is_touching(sprite: arcade.Sprite, geometry: arcade.SpriteList, *, check_top: bool = False, displacement: Tuple[int, int] = (5, 5)) -> bool:
    """Return True if sprite is touching any sprite in geometry"""
    dirs = [
        (-1, 0),  # Left
        (+1, 0),  # Right
        (0, -1)   # Bottom
    ]
    if check_top:
        dirs.append((0, +1))  # Top

    for dir in dirs:
        if check_touch(sprite, geometry, *map(lambda x, y: x*y, dir, displacement)):
            return True
    return False
