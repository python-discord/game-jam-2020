import enum
import random
from pathlib import Path

import arcade

from triple_vision import Settings as s
from triple_vision.entities.entities import LivingEntity
from triple_vision.entities.sprites import MovingSprite
from triple_vision.entities.weapons import LaserProjectile
from triple_vision.pathfinding import PathFinder
from triple_vision.utils import is_in_radius, pixels_to_tile, tile_to_pixels


class Enemies(enum.Enum):
    """
    Key is base name of the image file.
    Value is default enemy health
    """
    big_demon = 1024
    chort = 100
    wogol = 512
    big_zombie = 512
    tiny_zombie = 100
    goblin = 64
    ice_zombie = 256
    muddy = 2048

    imp = 300
    necromancer = 512


class BaseEnemy(LivingEntity):
    enemy_assets_path = Path('assets/dungeon/frames')

    def __init__(self, enemy: Enemies, kill_value: int, hp: int = 0, **kwargs) -> None:
        super().__init__(
            sprite_name=enemy.name,
            assets_path=self.enemy_assets_path,
            scale=s.SCALING,
            **kwargs
        )

        self.hp = enemy.value if hp < 1 else hp
        self.being_pushed = False
        self.kill_value = kill_value

        self.can_melee_attack = True
        self._melee_tick = 0.0
        self._melee_interval = 1

    def kill(self) -> None:
        self.ctx.enemy_killed(self)
        super().kill()

    def update_melee(self, delta_time: float):
        if self.can_melee_attack:
            return

        self._melee_tick += delta_time
        if self._melee_tick >= self._melee_interval:
            self._melee_tick = 0.0
            self.can_melee_attack = True


class SimpleChasingEnemy(BaseEnemy, MovingSprite):
    """
    Simple chasing enemy that tries to catch some other sprite.
    No path-finding, just goes straight to sprite if it is in radius.
    """

    def __init__(
        self,
        enemy: Enemies,
        melee_weapon,
        target_sprite: arcade.Sprite,
        detection_radius: int,
        **kwargs
    ) -> None:
        super().__init__(enemy, rotate=False, **kwargs)

        self.melee_weapon = melee_weapon
        self.target_sprite = target_sprite
        self.detection_radius = detection_radius

    def on_update(self, delta_time: float = 1/60) -> None:
        if not self.being_pushed:
            if is_in_radius(self, self.target_sprite, self.detection_radius):
                self.move_to(
                    self.target_sprite.center_x,
                    self.target_sprite.center_y,
                )
            else:
                self.change_x = 0
                self.change_y = 0

        # Since both are defined in both parents it's gonna call only from BaseEnemy
        # so we're forcing the call for MovingSprite
        super().on_update(delta_time)
        super().update_melee(delta_time)
        super().force_moving_sprite_on_update(delta_time)


class ChasingEnemy(BaseEnemy, MovingSprite):
    """
    Advanced chasing enemy that, if in detection radius, tries to catch some other sprite.
    Uses path-finding.
    """

    def __init__(
        self,
        enemy: Enemies,
        melee_weapon,
        target_sprite: arcade.Sprite,
        detection_radius: int,
        **kwargs
    ) -> None:
        super().__init__(enemy, rotate=False, kill_value=5, **kwargs)

        self.melee_weapon = melee_weapon
        self.target_sprite = target_sprite
        self.detection_radius = detection_radius

        self.path_finder = PathFinder()
        self.path = None

        self._tick_time = 0.0

    def on_update(self, delta_time: float = 1/60) -> None:
        if not self.being_pushed:
            if is_in_radius(self, self.target_sprite, self.detection_radius):

                if self.path is not None and self.target is None:

                    try:
                        self.move_to(*tile_to_pixels(*next(self.path)))

                    except StopIteration:
                        self.path = None

                else:
                    # Once path is found it should be rarely updated.
                    # However we don't really want multiple enemies to call find()
                    # in the same on_update, so we add a bit of randomness to it that isn't
                    # noticeable in the gameplay.
                    if self._tick_time > round(random.uniform(0.0, 0.2), 2):
                        self._tick_time = 0.0
                        try:
                            self.path = self.path_finder.find(
                                        pixels_to_tile(self.center_x, self.center_y),
                                        pixels_to_tile(
                                            self.target_sprite.center_x,
                                            self.target_sprite.center_y
                                        ),
                                        self.ctx.view.collision_list,
                                        self.ctx.view.map.sprites
                            )

                        except TypeError:
                            pass
                    else:
                        self._tick_time += delta_time
            else:
                self.change_x = 0
                self.change_y = 0

        # Since both are defined in both parents it's gonna call only from BaseEnemy
        # so we're forcing the call for MovingSprite
        super().on_update(delta_time)
        super().update_melee(delta_time)
        super().force_moving_sprite_on_update(delta_time)


class StationaryEnemy(BaseEnemy):

    def __init__(
        self,
        enemy: Enemies,
        melee_weapon,
        target_sprite: arcade.Sprite,
        detection_radius: int,
        shoot_interval: float,
        dmg: random.randrange,
        **kwargs
    ) -> None:
        super().__init__(enemy, is_pushable=False, kill_value=5, **kwargs)

        self.melee_weapon = melee_weapon  # If player gets too close to the sprite
        self.target_sprite = target_sprite
        self.detection_radius = detection_radius
        self.shoot_interval = shoot_interval
        self.dmg = dmg
        self._passed_time = 0.0

    def on_update(self, delta_time: float = 1/60) -> None:
        super().on_update(delta_time)
        super().update_melee(delta_time)
        self._passed_time += delta_time

        if not is_in_radius(self, self.target_sprite, self.detection_radius):
            return

        if self._passed_time < self.shoot_interval:
            return

        laser = LaserProjectile(
            color='red',
            dmg=self.dmg,
            center_x=self.center_x,
            center_y=self.center_y,
            rotate=True
        )
        laser.move_to(
            self.target_sprite.center_x,
            self.target_sprite.center_y,
            set_target=False
        )
        laser.play_activate_sound()

        self.ctx.enemy_projectiles.append(laser)
        self._passed_time = 0.0
