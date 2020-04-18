from triple_vision.constants import SCALING
from triple_vision.entities.entity import AnimatedEntity
from triple_vision.entities.sprites import MovingSprite


class Player(AnimatedEntity, MovingSprite):

    def __init__(self, gender: str) -> None:
        super().__init__(
            sprite_name='wizzard',
            assets_path='assets/wizard',
            is_colored=True,
            has_hit_frame=True,
            gender='m',
            moving_speed=3,
            scale=SCALING,
            center_x=500,
            center_y=500
        )
