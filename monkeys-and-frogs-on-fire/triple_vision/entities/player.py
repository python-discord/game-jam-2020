import time

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

    def check_mouse_press(self, x, y, button, modifiers) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.move_to(x, y, rotate=False)

        elif button == arcade.MOUSE_BUTTON_RIGHT:
            if time.time() - self.last_shot < 0.75:  # TODO hardcoded
                # TODO Play empty gun sound or something similar
                return

            bullet = LaserProjectile(
                center_x=self.center_x,
                center_y=self.center_y
            )
            bullet.move_to(x, y, rotate=True, set_target=False)
            self.window.game_manager.player_projectiles.append(bullet)
            self.last_shot = time.time()
