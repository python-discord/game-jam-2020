import arcade
import numpy as np
import matplotlib.pyplot as plt

EVEN_GRID_COLOR = arcade.color.JASMINE
ODD_GRID_COLOR = arcade.color.LIGHT_PASTEL_PURPLE
ATTACKABLE_GRID_COLOR = arcade.color.CARMINE_RED
MOVABLE_GRID_COLOR = arcade.color.ASPARAGUS


class TriGrid:
    def __init__(self, board_size, cell_width):
        self.board_size = board_size
        self.cell_width = cell_width
        self.shape_list = None
        self.grid, self.grid_map = self.init_grid()
        self.update_shape_list()

    def init_grid(self):
        grid = []
        grid_index = 0
        grid_map = {}
        for row in range(self.board_size):
            tmp_row = []
            for col in range(self.board_size - row):
                tmp_col = [TriCell(row, col, 0)]
                grid_map[(row, col, 0)] = grid_index
                grid_index += 1
                if col + row != self.board_size - 1:
                    tmp_col.append(TriCell(row, col, 1))
                    grid_map[(row, col, 1)] = grid_index
                    grid_index += 1
                tmp_row.append(tmp_col)
            grid.append(tmp_row)
        return grid, grid_map

    def update_shape_list(self):
        self.shape_list = arcade.ShapeElementList()
        for grid_row in self.grid:
            for grid_col in grid_row:
                for cell in grid_col:
                    current_cell = self.create_cell_poly(cell)
                    self.shape_list.append(current_cell)

    def create_cell_poly(self, cell):
        coord = self.calc_cell_coord(cell.x, cell.y, cell.r)
        cell_poly = arcade.create_polygon(coord, EVEN_GRID_COLOR if cell.r else ODD_GRID_COLOR)
        return cell_poly

    def calc_cell_coord(self, x, y, r):
        if r == 0:
            x_list = np.array([x, x, x + 1]) * self.cell_width
            y_list = np.array([y, y + 1, y]) * self.cell_width
            x_list_skewed = x_list + y_list * .5
        else:
            x_list = np.array([x + 1, x, x + 1]) * self.cell_width
            y_list = np.array([y + 1, y + 1, y]) * self.cell_width
            x_list_skewed = x_list + y_list * .5
        return list(zip(x_list_skewed, y_list))

    def get_grid_position(self, coord_x, coord_y):
        x = (coord_x - coord_y * 0.5) / self.cell_width
        y = coord_y / self.cell_width
        r = (y % 1) > 1 - (x % 1)
        print((x + y) % 2, y, x)
        return int(x), int(y), r

    def toggle_cell(self, x, y, r):
        self.grid[x][y][r].toggle()

    def get_grid_neighbor(self, coord_x, coord_y):
        x, y, r = self.get_grid_position(coord_x, coord_y)
        if r == 0:
            neighbor_list = [(x, y - 1, not r), (x - 1, y, not r), (x, y, not r)]
        else:
            neighbor_list = [(x, y + 1, not r), (x + 1, y, not r), (x, y, not r)]

        neighbor_list = [cell for cell in neighbor_list if self.is_valid_cell(*cell)]
        return neighbor_list

    def is_valid_cell(self, x, y, r):
        return not (x < 0 or y < 0 or x >= self.board_size or y >= self.board_size or (
                    x + y == self.board_size - 1 and r == 1))

    def on_draw(self):
        arcade.start_render()
        self.shape_list.draw()


class TriCell:
    def __init__(self, x, y, r, piece=None):
        self.x = x
        self.y = y
        self.r = r
        self.piece = piece

    def toggle(self, tog_val=None):
        if tog_val is None:
            self.piece = not self.piece
        else:
            self.piece = tog_val
