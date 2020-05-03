import logging
import os
import math
from math import floor
from itertools import zip_longest
from pathlib import Path
from numbers import Number
from typing import Tuple

import random
import os
import arcade
from PIL import Image
import time
from .constants import (
    DEFAULT_ALPHA,
    DEFAULT_EMIT_DURATION,
    DEFAULT_PARTICLE_LIFETIME,
    LINE_EMIT_INTERVAL,
    LINE_SCALE,
    NUM_COLORS,
    PARTICLE_SPEED_SLOW,
    PLUME_EMIT_INTERVAL,
    PLUME_PARTICLE_LIFETIME,
    PLUME_SCALE,
    PLUME_EMIT_DURATION,
    EXPLOSION_EMIT_INTERVAL,
    EXPLOSION_NUM_PARTICLE,
    PARTICLE_SPEED_FAST,
    DEFAULT_SCALE,
    EXPLOSION_SCALE,
    EXPLOSION_PARTICLE_LIFETIME,
)


def weird_sign(n: Number) -> int:
    if n < 0:
        return -1
    else:
        return 1

def dash(
    sprite: arcade.Sprite,
    dir_x: int,
    dir_y: int,
    collide_with: arcade.SpriteList,
) -> None:
    """Move sprite until it reaches something."""
    sprite.bottom += 1
    prev_x = sprite.left
    prev_y = sprite.bottom
    default_x = sprite.left
    default_y = sprite.bottom

    for x, y in zip_longest(
        range(floor(sprite.left), floor(sprite.left + dir_x), weird_sign(dir_x)),
        range(floor(sprite.bottom), floor(sprite.bottom + dir_y), weird_sign(dir_y)),
    ):
        sprite.left = x if x else prev_x
        sprite.bottom = y if y else prev_y
        if sprite.collides_with_list(collide_with):
            sprite.left = prev_x
            sprite.bottom = prev_y
            break
        if x:
            prev_x = x
        if y:
            prev_y = y


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


def is_touching(
    sprite: arcade.Sprite,
    geometry: arcade.SpriteList,
    *,
    check_top: bool = True,
    displacement: Tuple[int, int] = (5, 5)
) -> bool:
    """Return True if sprite is touching any sprite in geometry"""
    dirs = [(-1, 0), (+1, 0), (0, -1)]  # Left  # Right  # Bottom
    if check_top:
        dirs.append((0, +1))  # Top

    for dir in dirs:
        if check_touch(sprite, geometry, *map(lambda x, y: x * y, dir, displacement)):
            return True
    return False


# color conversion
def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0:
        r, g, b = v, t, p
    elif hi == 1:
        r, g, b = q, v, p
    elif hi == 2:
        r, g, b = p, v, t
    elif hi == 3:
        r, g, b = p, q, v
    elif hi == 4:
        r, g, b = t, p, v
    elif hi == 5:
        r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b


def rgb2hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx - mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g - b) / df) + 360) % 360
    elif mx == g:
        h = (60 * ((b - r) / df) + 120) % 360
    elif mx == b:
        h = (60 * ((r - g) / df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df / mx
    v = mx
    return h, s, v


def rand_color(c, scale=0.25):
    as_hsv = rgb2hsv(*c)
    clamp = lambda my_value, max_v: max(min(my_value, max_v), 0)
    for _ in range(NUM_COLORS):
        yield hsv2rgb(
            *(
                clamp(as_hsv[0] + (random.random() - 0.5) * scale, 360),
                clamp(as_hsv[1] + (random.random() - 0.5) * scale, 1.0),
                clamp(as_hsv[2] + (random.random() - 0.5) * scale, 1.0),
            )
        )


def dash_emitter_factory(color, pos_a, pos_b):
    """Interval, emit on line"""
    logging.info("Creating dash emitter")

    if pos_a[0] > pos_b[0]:
        angle = 0
    else:
        angle = 180
    textures = [
        arcade.Texture(f"{time.time()}", Image.new("RGBA", (10, 10), p))
        for p in rand_color(color)
    ]
    line_e = arcade.Emitter(
        center_xy=(0.0, 0.0),
        emit_controller=arcade.EmitterIntervalWithTime(
            LINE_EMIT_INTERVAL, DEFAULT_EMIT_DURATION
        ),
        particle_factory=lambda emitter: arcade.LifetimeParticle(
            filename_or_texture=random.choice(textures),
            change_xy=arcade.rand_in_circle((0.0, 0.0), PARTICLE_SPEED_SLOW),
            lifetime=DEFAULT_PARTICLE_LIFETIME,
            center_xy=arcade.rand_on_line(pos_a, pos_b),
            scale=LINE_SCALE,
            alpha=DEFAULT_ALPHA,
        ),
    )
    exhaust_plume_e = arcade.Emitter(
        center_xy=pos_a,
        emit_controller=arcade.EmitterIntervalWithTime(
            PLUME_EMIT_INTERVAL, PLUME_EMIT_DURATION
        ),
        particle_factory=lambda emitter: arcade.FadeParticle(
            filename_or_texture=random.choice(textures),
            change_xy=arcade.rand_vec_spread_deg(angle, 25, 4.0),
            lifetime=PLUME_PARTICLE_LIFETIME,
            scale=PLUME_SCALE,
        ),
    )
    return line_e, exhaust_plume_e


class ExplosionParticle(arcade.LifetimeParticle):
    def update(self):
        super().update()
        #self.change_y = -2*(self.lifetime_elapsed-math.sqrt(5))


def explosion_factory(pos, color):
    logging.info(f"Creating explosion emitter at {pos}")

    textures = [
        arcade.Texture(f"{time.time()}", Image.new("RGBA", (10, 10), p))
        for p in rand_color(color)
    ]

    line_e = arcade.Emitter(
        center_xy=(0.0, 0.0),
        emit_controller=arcade.EmitterIntervalWithCount(
            EXPLOSION_EMIT_INTERVAL, EXPLOSION_NUM_PARTICLE
        ),
        particle_factory=lambda emitter: arcade.FadeParticle(
            filename_or_texture=random.choice(textures),
            change_xy=arcade.rand_in_circle((0.0, 0.0), PARTICLE_SPEED_FAST),
            lifetime=EXPLOSION_PARTICLE_LIFETIME,
            center_xy=pos,
            change_angle=random.uniform(-6, 6),
            scale=EXPLOSION_SCALE,
        ),
    )
    line_e.change_angle = 16
    return line_e
