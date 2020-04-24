import csv

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder



def layer_to_grid(layer_filename):

    with open(layer_filename, newline='') as f:
        reader = csv.reader(f)
        matrix = list(reader)

    matrix_2 = []

    for row in matrix:
        matrix_2.append([1 if int(num) < 0 else 0 for num in row])

    return matrix_2


# grid = layer_to_grid('../resources/maps/test_map_islands.csv')


def find_path(matrix, start_x, start_y, end_x, end_y):

    grid = Grid(matrix=matrix)

    tile_size = 64

    for i in (start_x, start_y, end_x, end_y):
        if i < 0:
            i = 0

    # For some reason the y value is inverted. Probably has to do with the grid
    # Hence the 36-..., where 36 is the map's height in tiles
    start = grid.node(int(start_x/tile_size), 36-int(start_y/tile_size))
    end = grid.node(int(end_x/tile_size), 36-int(end_y/tile_size))

    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    path, runs = finder.find_path(start, end, grid)

    # Again, subtracting by the tile height otherwise the path is flipped
    path_resized = [
        (position[0]*tile_size, (36-position[1])*tile_size) for position in path
    ]

    print('operations:', runs, 'path length:', len(path))
    print(grid.grid_str(path=path, start=start, end=end))

    return path_resized
