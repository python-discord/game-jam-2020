import time
import random
from itertools import chain

import arcade

from triple_vision import Settings as s
from triple_vision.entities import LivingEntity
from triple_vision.entities.sprites import MovingSprite
from triple_vision.entities.weapons import LaserProjectile
from triple_vision.pathfinding import PathFinder
from triple_vision.utils import pixels_to_tile, tile_to_pixels


class Player(LivingEntity, MovingSprite):

    def __init__(self, view: arcade.View, gender: str) -> None:
        super().__init__(
            sprite_name='wizzard',
            assets_path='assets/wizard',
            is_colored=True,
            has_hit_frame=True,
            gender=gender,
            moving_speed=3,
            scale=s.SCALING,
            center_x=500,
            center_y=500,
            hp=1000,
            rotate=False
        )

        self.view = view
        self.last_shot = time.time()

        self.is_alive = True
        self.attack_multiplier = 1
        self.dexterity = 0.75

        self._curr_color = self.curr_color

        self.path_finder = PathFinder()
        self.path = None

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
            # First path position is the closest grid center from player center,
            # to force the player to be centered in tile before transversing
            closest_grid_tile_x, closest_grid_tile_y = pixels_to_tile(self.center_x, self.center_y)

            try:
                path = iter(
                    self.path_finder.find(
                        pixels_to_tile(self.center_x, self.center_y),
                        pixels_to_tile(x, y),
                        self.view.collision_list
                    )
                )

            except TypeError:
                print('Path is either impossible or too far away!')

            else:
                self.path = chain(((closest_grid_tile_x, closest_grid_tile_y),), path)

        elif button == arcade.MOUSE_BUTTON_RIGHT:

            if time.time() - self.last_shot < self.dexterity:
                # TODO Play empty gun sound or something similar
                return

            bullet = LaserProjectile(
                center_x=self.center_x,
                center_y=self.center_y,
                dmg=round(random.randrange(60, 70) * self.attack_multiplier, 2),
                moving_speed=5,
                rotate=True
            )
            bullet.move_to(x, y, set_target=False)
            bullet.play_activate_sound()
            self.view.game_manager.player_projectiles.append(bullet)
            self.last_shot = time.time()

    def kill(self):
        self.is_alive = False
        super().kill()

    def on_update(self, delta_time: float = 1/60) -> None:
        if self.path is not None and self.target is None:
            try:
                pos = tile_to_pixels(*next(self.path))
                self.move_to(pos[0], pos[1] + s.PLAYER_CENTER_Y_COMPENSATION)

            except StopIteration:
                self.path = None

        super().on_update(delta_time)
        super().force_moving_sprite_on_update(delta_time)
