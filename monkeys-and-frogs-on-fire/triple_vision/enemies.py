import math
import enum
from pathlib import Path

import arcade

_IDLE_SUFFIX = '_idle_anim_f'
_RUN_SUFFIX = '_run_anim_f'
_FILE_EXTENSION = '.png'
_ANIMATION_SPRITE_COUNT = 4


class Enemies(enum.Enum):
    big_demon = 0


class BaseEnemy(arcade.Sprite):
    enemy_assets_path = Path('assets/dungeon/frames')
    """
    Sprite with idle and run animation.
    """
    def __init__(self, enemy: Enemies, **kwargs):
        super().__init__(**kwargs)
        self.idle = True
        self._delta_tick = 0
        self._animation_time = 0.15
        self._current_texture = 0
        self._idle_textures = []
        self._run_textures = []
        self._load_textures(self._idle_textures, _IDLE_SUFFIX, enemy)
        self._load_textures(self._run_textures, _RUN_SUFFIX, enemy)
        self.texture = self._idle_textures[0]

    def _load_textures(self, container: list, suffix: str, enemy: Enemies):
        for i in range(_ANIMATION_SPRITE_COUNT):
            texture_path = self.enemy_assets_path / f"{enemy.name}{suffix}{i}{_FILE_EXTENSION}"
            texture = arcade.load_texture(texture_path)
            container.append(texture)

    def update(self, delta_time: float = 1/60):
        self._delta_tick += delta_time
        self._current_texture += 1
        if self._current_texture == _ANIMATION_SPRITE_COUNT:
            self._current_texture = 0

        if self._delta_tick >= self._animation_time:
            if self.idle:
                self.texture = self._idle_textures[self._current_texture]
            else:
                self.texture = self._run_textures[self._current_texture]

            self._delta_tick = 0

        super().update()

    def make_it_run(self):
        self.idle = False

    def make_it_idle(self):
        self.idle = True


class ChasingEnemy(BaseEnemy):
    """
    Simple chasing enemy that tries to catch some other sprite.
    No path-finding, just goes straight to sprite if it is in radius.
    """
    def __init__(self, enemy: Enemies,
                 what_to_chase: arcade.Sprite,
                 chase_speed: int,
                 detection_radius: int,
                 **kwargs):
        super().__init__(enemy, **kwargs)
        self.chase_speed = chase_speed
        self.what_to_chase = what_to_chase
        self.detection_radius = detection_radius

    def _detect(self) -> bool:
        return (abs(self.center_x - self.what_to_chase.center_x) <= self.detection_radius or
                abs(self.center_y - self.what_to_chase.center_y) <= self.detection_radius)

    def update(self, delta_time: float = 1/60):
        if self._detect():
            dest_x = self.what_to_chase.center_x
            dest_y = self.what_to_chase.center_y

            x_diff = dest_x - self.center_x
            y_diff = dest_y - self.center_y
            angle = math.atan2(y_diff, x_diff)

            self.change_x = math.cos(angle) * self.chase_speed
            self.change_y = math.sin(angle) * self.chase_speed

        super().update()
