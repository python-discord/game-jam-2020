import random
from typing import List, Tuple

import numpy as np


class Map:

    def __init__(self, shape: Tuple[int, int]) -> None:
        self.shape = shape

        self.WALL = 1
        self.FLOOR = 0
        self.GENERATIONS = 6
        self.FILL_PROBABILITY = 0.4

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
                        # Solidify walls if 1 away has 5 or more walls
                        if wall_count_1_away >= 5:
                            map_[i][j] = self.WALL
                        else:
                            map_[i][j] = self.FLOOR

        return map_


if __name__ == "__main__":
    map_ = Map((20, 20))
    print(map_.generate())
