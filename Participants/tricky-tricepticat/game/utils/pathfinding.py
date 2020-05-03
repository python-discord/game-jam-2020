import csv

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


def clamp(n, smallest, largest): return max(smallest, min(n, largest))


def layer_to_grid(layer_filename):
    """
    Converts a TMX layer to a matrix indicating if a tile is
    present (0) or not (1). This provides the barriers needed for pathfinding.
    """
    with open(layer_filename, newline='') as f:
        reader = csv.reader(f)
        matrix = list(reader)

    matrix_2 = []

    for row in matrix:
        matrix_2.append([1 if int(num) < 0 else 0 for num in row])

    return matrix_2


def find_path(matrix, start_x, start_y, end_x, end_y, tile_size, map_height):
    """
    Creates a path from a matrix of barriers, a start position,
    a desired end position, the size of tiles used in a map,
    and the map's height (in tiles).
    """

    # TODO: Get map height from matrix instead of it being a parameter

    grid = Grid(matrix=matrix)

    start_x = clamp(start_x, 0, start_x)
    start_y = clamp(start_y, 0, start_y)
    end_x = clamp(end_x, 0, end_x)
    end_y = clamp(end_y, 0, end_y)

    print(len(matrix))
    print((int(
        start_x/tile_size), map_height-int(start_y/tile_size), (int(
            end_x/tile_size), map_height-int(end_y/tile_size))))

    # For some reason the y value is inverted. Probably has to do with the grid
    # Hence map_height - ...,

    # TODO: Figure out why bottom of the map causes IndexError

    try:
        start = grid.node(int(
            start_x / tile_size), map_height - int(start_y / tile_size) - 1
        )

        end = grid.node(int(
            end_x / tile_size), map_height - int(end_y / tile_size)
        )

        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path, runs = finder.find_path(start, end, grid)
    except IndexError:
        print("Out of range.")
        path = []


    # Again, subtracting by the tile height otherwise the path is flipped
    path_resized = [
        (position[0]*tile_size, (map_height-position[1])
            * tile_size) for position in path
    ]

    # print('operations:', runs, 'path length:', len(path))
    # print(grid.grid_str(path=path, start=start, end=end))

    return path_resized
