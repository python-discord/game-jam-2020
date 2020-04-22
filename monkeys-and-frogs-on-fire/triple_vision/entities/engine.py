from typing import Tuple

import arcade

from triple_vision import Settings as s
from triple_vision.utils import pixels_to_tile, tile_to_pixels, closest_grid_position
from triple_vision.entities.sprites import MovingSprite


class SlowModeSupportEngine:
    def __init__(self, player: MovingSprite, collision_list: arcade.SpriteList):
        self.player = player
        self.collision_list = collision_list

    def update(self):
        collision = arcade.check_for_collision_with_list(self.player, self.collision_list)
        if collision and self.player.target is not None:
            # If there is a collision but player is traveling stop him (so he doesn't go further
            # into the obstacle)
            self.player.path = None
            self.player.target = None
        elif collision and self.player.target is None:
            # If there is a collision but player is not traveling then move him to the nearest tile
            # that is NOT passable (can't be in collision_list like walls etc)

            closest_grid_x, closest_grid_y = self.get_closest_passable_tile_position(
                self.player.center_x,
                self.player.center_y
            )

            self.player.move_to(
                closest_grid_x,
                closest_grid_y + s.PLAYER_CENTER_Y_COMPENSATION,
                set_target=True
            )

    def get_closest_passable_tile_position(
            self,
            center_x: float,
            center_y: float
    ) -> Tuple[float, float]:

        closest_grid_x, closest_grid_y = closest_grid_position(center_x, center_y)

        # Sometimes the player gets pushed into the wall just enough that the closest tile is
        # actually the wall itself, so our return is actually a wall tile, which isn't passable!
        if self._is_tile_position_blocking(closest_grid_x, closest_grid_y):

            tile = pixels_to_tile(center_x, center_y)
            # Currently only works for y direction if the player is pushed up
            closest_grid_x, closest_grid_y = tile_to_pixels(tile[0], tile[1] - 1)
            return closest_grid_x, closest_grid_y
        else:
            return closest_grid_x, closest_grid_y

    def _is_tile_position_blocking(self, grid_tile_x: float, grid_tile_y: float):
        """
        Passed coordinate have to be valid grid tile position.
        """
        return any(block.position == (grid_tile_x, grid_tile_y) for block in self.collision_list)
