from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

# 0 is an unwalkable block. Numbers larger than 0 are walkable.
# The higher the number the harder it is to walk on.
matrix = [
	    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
	    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
	    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
	    [0, 1, 1, 1, 0, 0, 1, 1, 1, 1],
	    [0, 1, 1, 1, 0, 0, 1, 1, 1, 1],
	    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
	    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
	    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
	    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

grid = Grid(matrix=matrix)
start = grid.node(1, 1)
end = grid.node(8, 8)

finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
path, runs = finder.find_path(start, end, grid)

print('operations:', runs, 'path length:', len(path))
print(grid.grid_str(path=path, start=start, end=end))
