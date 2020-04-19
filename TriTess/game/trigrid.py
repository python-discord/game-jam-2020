import arcade
import numpy as np
import matplotlib.pyplot as plt


ON_COLOR = arcade.color.SPANISH_VIOLET
OFF_COLOR = arcade.color.GRAY


class TriGrid:
    def __init__(self, board_size, cell_width):
        self.board_size = board_size
        self.cell_width = cell_width
        self.color = ON_COLOR
        self.shape_list = None
        self.grid = self.init_grid()
        self.update_shape_list()

    def init_grid(self):
        grid = []
        for row in range(self.board_size):
            tmp_row = []
            for col in range(self.board_size-row):
                tmp_row.append(TriCell(row, col, 0, 0))
                if col + row != self.board_size-1:
                    tmp_row.append(TriCell(row, col, 1, 1))
            grid.append(tmp_row)
        return grid

    def update_shape_list(self):
        self.shape_list = arcade.ShapeElementList()
        for grid_row in self.grid:
            for cell in grid_row:
                current_cell = self.create_cell_poly(cell)
                self.shape_list.append(current_cell)

    def create_cell_poly(self, cell):
        coord = self.calc_cell_coord(cell.x, cell.y, cell.r)
        cell_poly = arcade.create_polygon(coord, OFF_COLOR if cell.piece == 0 else ON_COLOR)
        return cell_poly

    def calc_cell_coord(self, x, y, r):
        if r == 0:
            x_list = np.array([x, x, x+1])*self.cell_width
            y_list = np.array([y, y+1, y])*self.cell_width
            x_list_skewed = x_list + y_list*.5
        else:
            x_list = np.array([x + 1, x, x + 1])*self.cell_width
            y_list = np.array([y + 1, y + 1, y])*self.cell_width
            x_list_skewed = x_list + y_list * .5
        return list(zip(x_list_skewed, y_list))

    def on_draw(self):
        arcade.start_render()
        self.shape_list.draw()


class TriCell:
    def __init__(self, x, y, r, piece):
        self.x = x
        self.y = y
        self.r = r
        self.piece = piece
