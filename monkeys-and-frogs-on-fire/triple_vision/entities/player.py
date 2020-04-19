import time

from triple_vision.constants import SCALING
from triple_vision.entities.entities import LivingEntity
from triple_vision.entities.sprites import MovingSprite


class Player(LivingEntity, MovingSprite):

    def __init__(self, gender: str) -> None:
        self.last_shot = time.time()
        self.is_alive = True

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

    def kill(self):
        self.is_alive = False
        super().kill()
