import random
from typing import List, Tuple

import arcade
import numpy as np

from triple_vision.constants import (
    SCALED_TILE,
    SCALING,
    TILE_SIZE
)


class Map:

    def __init__(self, shape: Tuple[int, int]) -> None:
        self.shape = shape

        self.AIR = 0
        self.WALL = 1
        self.FLOOR = 2
        self.GENERATIONS = 6
        self.FILL_PROBABILITY = 0.4

        self.sprites = None

    def generate(self) -> List[List[int]]:
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
                    wall_count_1_away = len(np.where(submap.flatten() == self.WALL)[0])

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
                            map_[i][j] = self.FLOOR

                        # Make the current point a wall if it's on the edge of the map
                        if i == 0 or j == 0 or i == self.shape[0] - 1 or j == self.shape[1] - 1:
                            map_[i][j] = self.WALL

                    else:
                        submap = map_[
                            max(i - 1, 0): min(i + 2, map_.shape[0]),
                            max(j - 1, 0): min(j + 2, map_.shape[1])
                        ]
                        floor_count_1_away = len(np.where(submap.flatten() == self.FLOOR)[0])

                        # Turn all walls that aren't near floor into air
                        if floor_count_1_away == 0 and map_[i][j] == self.WALL:
                            map_[i][j] = self.AIR

        return map_

    def spritify(self, map_) -> arcade.SpriteList:
        sprites = arcade.SpriteList()

        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                val = map_[i][j]

                if val == 0:
                    continue

                filename = 'wall_mid' if val == self.WALL else f'floor_{random.randint(1, 8)}'

                sprites.append(
                    arcade.Sprite(
                        filename=f'assets/dungeon/frames/{filename}.png',
                        scale=SCALING,
                        center_x=i * SCALED_TILE + SCALED_TILE / 2,
                        center_y=j * SCALED_TILE + SCALED_TILE / 2
                    )
                )

        return sprites

    def setup(self) -> None:
        floor_count = 0
        map_ = None

        while floor_count < (self.shape[0] * self.shape[1]) // 3:
            map_ = self.generate()
            floor_count = len(np.where(map_.flatten() == self.FLOOR)[0])

        self.sprites = self.spritify(map_)

    def draw(self) -> None:
        self.sprites.draw()

    def update(self, delta_time: float = 1/60) -> None:
        self.sprites.update()
