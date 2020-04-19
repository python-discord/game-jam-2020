import arcade
import numpy as np
import matplotlib.pyplot as plt


class TriCell:
    def __init__(self, x, y, r, cell_width):
        self.x = x
        self.y = y
        self.r = r
        self.coord = self.calc_cell_coord(x, y, r, cell_width)
        self.piece = None
        self.color = arcade.color.SPANISH_VIOLET

    def draw(self):
        if self.r == 0:
            arcade.draw_polygon_filled(self.coord, self.color)
        else:
            arcade.draw_polygon_outline(self.coord, self.color, 3)

    def calc_cell_coord(self, x, y, r, cell_width):
        if r == 0:
            x_list = np.array([x, x, x+1])*cell_width
            y_list = np.array([y, y+1, y])*cell_width
            x_list_skewed = x_list + y_list*.5
        else:
            x_list = np.array([x + 1, x, x + 1])*cell_width
            y_list = np.array([y + 1, y + 1, y])*cell_width
            x_list_skewed = x_list + y_list * .5
        return list(zip(x_list_skewed, y_list))


class TriGrid:
    def __init__(self, board_size, cell_width):
        self.grid = []
        for row in range(board_size):
            tmp_row = []
            for col in range(board_size-row):
                tmp_row.append(TriCell(row, col, 0, cell_width))
                if col + row != board_size-1:
                    tmp_row.append(TriCell(row, col, 1, cell_width))
            self.grid.append(tmp_row)

    def draw(self):
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                cell.draw()
