from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


def route(start, end, matrix) -> path:
    """
    Take a matrix of the level in the form wighted numbers, a start and stop point, and return a path between them.
    
    param: start: (x, y) location of the monster
    param: end: (x, y) location of the player
    param: matrix: a 2d list of the level. 0s are walls, numbers greater than 0 are weighted
    """

    grid = Grid(matrix=matrix)
    start = grid.node(start[0], start[1])
    end = grid.node(end[0], end[1])
    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    path, runs = finder.find_path(start, end, grid)

    return path



