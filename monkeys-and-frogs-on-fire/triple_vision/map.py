import random
import traceback
from typing import Optional, Tuple

import arcade
import numpy as np

from triple_vision import Settings as s
from triple_vision.entities import Spike
from triple_vision.utils import tile_to_pixels


random.seed(1234)


class Map:

    def __init__(self, view: arcade.View, shape: Tuple[int, int]) -> None:
        self.view = view
        self.shape = shape

        self.AIR = 0
        self.WALL = 1
        self.FLOOR = 2
        self.SPIKE = 3

        self.GENERATIONS = 6
        self.FILL_PROBABILITY = 0.2
        self.SPIKE_PROBABILITY = 0.01

        self.sprites: Optional[arcade.SpriteList] = None

    def generate(self) -> np.array:
        map_ = np.ones(self.shape)

        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                choice = random.uniform(0, 1)
                map_[i][j] = self.WALL \
                    if choice < self.FILL_PROBABILITY else self.FLOOR

        for gen in range(self.GENERATIONS):
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):

                    # Get walls that are 1 away from each index
                    submap = map_[
                        max(i - 1, 0): min(i + 2, map_.shape[0]),
                        max(j - 1, 0): min(j + 2, map_.shape[1])
                    ]
                    flat_submap = submap.flatten()
                    wall_count_1_away = len(np.where(flat_submap== self.WALL)[0])
                    floor_count_1_away = len(np.where((flat_submap == self.FLOOR) | (flat_submap == self.SPIKE))[0])

                    # Get walls that are 2 away from each index
                    submap = map_[
                        max(i - 2, 0): min(i + 3, map_.shape[0]),
                        max(j - 2, 0): min(j + 3, map_.shape[1])
                    ]
                    wall_count_2_away = len(np.where(submap.flatten() == self.WALL)[0])

                    # First (self.GENERATIONS - 1) generations build scaffolding for walls
                    if gen < self.GENERATIONS - 1:

                        # If 1 away has 5 or more walls, make the current point a wall
                        # If 2 away has 7 or more walls, make the current point a wall
                        # If neither, make the current point floor
                        if wall_count_1_away >= 5 or wall_count_2_away <= 7:
                            map_[i][j] = self.WALL
                        else:
                            chance = random.uniform(0, 1)
                            map_[i][j] = self.FLOOR \
                                if chance > self.SPIKE_PROBABILITY else self.SPIKE

                        # Make the current point a wall if it's on the edge of the map
                        if i == 0 or j == 0 or i == self.shape[0] - 1 or j == self.shape[1] - 1:
                            map_[i][j] = self.WALL

                    else:
                        # Turn all walls that aren't near floor into air
                        if floor_count_1_away == 0 and map_[i][j] == self.WALL:
                            map_[i][j] = self.AIR

        return map_

    def spritify(self, map_) -> arcade.SpriteList:
        spikes = arcade.SpriteList(use_spatial_hash=True)
        sprites = arcade.SpriteList(use_spatial_hash=True)
        collision_list = arcade.SpriteList(use_spatial_hash=True)

        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                val = map_[i][j]

                if val == self.AIR:
                    continue

                center_x, center_y = tile_to_pixels(i, j)

                if val == self.SPIKE:
                    sprite = Spike(
                        target_player=self.view.player,
                        target_enemies=None,
                        scale=s.SCALING,
                        center_x=center_x,
                        center_y=center_y
                    )
                    spikes.append(sprite)

                else:
                    filename = 'wall_mid' \
                        if val == self.WALL else f'floor_{random.randint(1, 8)}'

                    sprite = arcade.Sprite(
                        filename=f'assets/dungeon/frames/{filename}.png',
                        scale=s.SCALING,
                        center_x=center_x,
                        center_y=center_y
                    )

                    if val == self.WALL:
                        collision_list.append(sprite)

                sprites.append(sprite)

        return sprites, collision_list, spikes

    def setup(self) -> None:
        floor_count = 0
        map_ = None

        while floor_count < (self.shape[0] * self.shape[1]) / 2.5:
            map_ = self.generate()
            flat_map = map_.flatten()
            floor_count = len(np.where((flat_map == self.FLOOR) | (flat_map == self.SPIKE))[0])

        self.sprites, self.view.collision_list, self.view.game_manager.spikes = self.spritify(map_)

    def draw(self) -> None:
        self.sprites.draw()

    def on_update(self, delta_time: float = 1/60) -> None:
        self.sprites.on_update(delta_time)
