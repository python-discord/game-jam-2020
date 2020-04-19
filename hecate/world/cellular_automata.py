import random


# This code was taken from the arcade example for procedural caves using cells
# Did not import directly from library because I may need to make changes down the line

class DungeonAgar:
    def __init__(self, w, h, s, c, b, d):
        self.width = w
        self.height = h
        self.steps = s
        self.chance = c
        self.birth = b
        self.death = d
        self.dungeon = []

        self.make_grid()

        for step in range(self.steps):
            self.simulate_step()

    def make_grid(self):
        """ Randomly set grid locations to on/off based on chance. """
        grid = [[False for _x in range(self.width)] for _y in range(self.height)]
        height = len(grid)
        width = len(grid[0])
        for row in range(height):
            for column in range(width):
                if random.random() <= self.chance:
                    grid[row][column] = True

        self.dungeon = grid

    def count_alive_neighbors(self, x, y):
        """ Count neighbors that are alive. """
        height = len(self.dungeon)
        width = len(self.dungeon[0])
        alive_count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                neighbor_x = x + i
                neighbor_y = y + j
                if i == 0 and j == 0:
                    continue
                elif neighbor_x < 0 or neighbor_y < 0 or neighbor_y >= height or neighbor_x >= width:
                    # Edges are considered alive. Makes map more likely to appear naturally closed.
                    alive_count += 1
                elif self.dungeon[neighbor_y][neighbor_x]:
                    alive_count += 1
        return alive_count

    def simulate_step(self):
        """ Run a step of the cellular automaton. """
        height = len(self.dungeon)
        width = len(self.dungeon[0])
        new_grid = [[False for _x in range(width)] for _y in range(height)]
        for x in range(width):
            for y in range(height):
                alive_neighbors = self.count_alive_neighbors(x, y)
                if self.dungeon[y][x]:
                    if alive_neighbors < self.death:
                        new_grid[y][x] = False
                    else:
                        new_grid[y][x] = True
                else:
                    if alive_neighbors > self.birth:
                        new_grid[y][x] = True
                    else:
                        new_grid[y][x] = False
        self.dungeon = new_grid
