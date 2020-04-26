# from math import floor, ceil

from .constants import JUMP_FORCE, JUMP_FORCE_REDUCTION, RIGHT
from .sprite import Sprite

# from .utils import AnimLoader
# import arcade

# import time


class Player(Sprite):
    colors = {"white": 0, "red": 1, "green": 2, "blue": 3}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.movement_x = 0
        self.previous_movement_x = 0
        self.movement_control = 0.5
        self.is_jumping = False
        self.jump_force = JUMP_FORCE
        self.jump_count = 0
        self.dash_count = 0
        self.direction = RIGHT
        self.str_color = "white"
        # self.anims_right = AnimLoader("assets/player")
        # self.anims_left = AnimLoader("assets/player", mirrored=True)

    def set_color(self, color: str) -> None:
        self.set_texture(self.colors.get(color, 0))
        self.str_color = color

    def update(self):
        if self.is_jumping:
            self.change_y += self.jump_force
            self.jump_force *= JUMP_FORCE_REDUCTION
        self.change_x = (self.movement_x * self.movement_control + self.previous_movement_x) / (
            1 + self.movement_control
        )
        self.previous_movement_x = self.change_x

        # if floor(self.change_x) > 0:
        #     self.texture = self.anims_right.moving[
        #         int(time.time() * 10) % len(self.anims_right.moving)
        #     ]

        # if ceil(self.change_x) < 0:
        #     self.texture = self.anims_left.moving[
        #         int(time.time() * 10) % len(self.anims_left.moving)
        #     ]
