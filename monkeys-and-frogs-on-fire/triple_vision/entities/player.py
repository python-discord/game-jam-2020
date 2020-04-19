import time
import random

import arcade

from triple_vision.constants import SCALING
from triple_vision.entities.entities import LivingEntity
from triple_vision.entities.sprites import MovingSprite
from triple_vision.entities.weapons import LaserProjectile


class Player(LivingEntity, MovingSprite):

    def __init__(self, window: arcade.Window, gender: str) -> None:
        super().__init__(
            sprite_name='wizzard',
            assets_path='assets/wizard',
            is_colored=True,
            has_hit_frame=True,
            gender=gender,
            moving_speed=3,
            scale=SCALING,
            center_x=500,
            center_y=500,
            hp=1000
        )

        self.window = window
        self.last_shot = time.time()

        self.is_alive = True
        self.attack_multiplier = 1
        self.dexterity = 0.75

        self._curr_color = self.curr_color

    @property
    def curr_color(self):
        return self._curr_color

    @curr_color.setter
    def curr_color(self, value):
        if value == 'red':
            self.resistance = 0.1
            self.attack_multiplier = 1.5
            self.speed_multiplier = 1.1
            self.dexterity = 0.6

        elif value == 'green':
            self.resistance = 0.5
            self.attack_multiplier = 1.1
            self.speed_multiplier = 1
            self.dexterity = 0.75

        elif value == 'blue':
            self.resistance = 0
            self.attack_multiplier = 1
            self.speed_multiplier = 1.5
            self.dexterity = 0.5

        else:
            raise ValueError('Color can only be red, green, or blue.')

        self._curr_color = value

    def setup(self) -> None:
        self.set_hit_box([
            (-4.0, -1.0),
            (4.0, -1.0),
            (6.0, -3.0),
            (6.0, -11.0),
            (4.0, -13.0),
            (-4.0, -13.0),
            (-6.0, -11.0),
            (-6.0, -3.0)
        ])
        self.curr_color = 'red'

    def process_mouse_press(self, x, y, button) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.move_to(x, y, rotate=False)

        elif button == arcade.MOUSE_BUTTON_RIGHT:

            if time.time() - self.last_shot < self.dexterity:
                # TODO Play empty gun sound or something similar
                return

            bullet = LaserProjectile(
                center_x=self.center_x,
                center_y=self.center_y,
                dmg=round(random.randrange(60, 70) * self.attack_multiplier, 2),
                moving_speed=5
            )
            bullet.move_to(x, y, rotate=True, set_target=False)
            bullet.play_activate_sound()
            self.window.game_manager.player_projectiles.append(bullet)
            self.last_shot = time.time()

    def kill(self):
        self.is_alive = False
        super().kill()
