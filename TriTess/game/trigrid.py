import arcade
import numpy as np
from . import trichess_piece
import matplotlib.pyplot as plt

EVEN_GRID_COLOR = arcade.color.JASMINE
ODD_GRID_COLOR = arcade.color.LIGHT_PASTEL_PURPLE
ATTACKABLE_GRID_COLOR = arcade.color.CARMINE_RED
MOVABLE_GRID_COLOR = arcade.color.ASPARAGUS



class TriGrid:
    def __init__(self, board_size, cell_width, grid_type='triangular'):
        self.board_size = board_size
        self.cell_width = cell_width
        self.shape_list = None
        self.grid, self.grid_map = self.init_grid(grid_type)
        self.piece_list = self.init_pieces(grid_type)
        self.update_shape_list()

    def init_grid(self, grid_type):
        grid = []
        grid_index = 0
        grid_map = {}
        if grid_type == "triangular":
            for row in range(self.board_size):
                tmp_row = []
                for col in range(self.board_size - row):
                    tmp_col = [TriCell(row, col, 0, self.cell_width)]
                    grid_map[(row, col, 0)] = grid_index
                    grid_index += 1
                    if col + row != self.board_size - 1:
                        tmp_col.append(TriCell(row, col, 1, self.cell_width))
                        grid_map[(row, col, 1)] = grid_index
                        grid_index += 1
                    tmp_row.append(tmp_col)
                grid.append(tmp_row)
        return grid, grid_map

    def init_pieces(self, grid_type):
        piece_list = arcade.SpriteList()
        if grid_type == "triangular":
            p1_piece_list = [("pawn", (index, 1, 0), 0) for index in range(2, 8)] + \
                            [("pawn", (index, 1, 0), 0) for index in range(3, 7)] + \
                            [("rook", (3, 0, 1), 0), ("rook", (7, 0, 1), 0)] + \
                            [("knight", (4, 0, 0), 0), ("knight", (7, 0, 0), 0)] + \
                            [("bishop", (4, 0, 1), 0), ("bishop", (6, 0, 1), 0)] + \
                            [("king", (5, 0, 0), 0), ("queen", (6, 0, 0), 0)]
            for name, pos, player in p1_piece_list:
                piece_list.append(trichess_piece.TriPiece.create_piece(name, pos, player, self))
            return piece_list

    def update_shape_list(self):
        self.shape_list = arcade.ShapeElementList()
        for grid_row in self.grid:
            for grid_col in grid_row:
                for cell in grid_col:
                    current_cell = cell.create_cell_poly()
                    self.shape_list.append(current_cell)

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
        return (x, y, r) in self.grid_map

    def on_draw(self, grid_coord=False):
        arcade.start_render()
        self.shape_list.draw()
        self.piece_list.draw()
        if grid_coord:
            for grid_x, grid_y, grid_r in self.grid_map:
                coord_list = self.grid[grid_x][grid_y][grid_r].bound_coords
                x, y = coord_list[0]
                if grid_r == 1:
                    x -= 45
                    y -= 30
                arcade.draw_text(f'{grid_x, grid_y, grid_r}', x, y, color=arcade.color.BLACK, font_size=12)


class TriCell:
    def __init__(self, x, y, r, cell_width, piece=None):
        self.x = x
        self.y = y
        self.r = r
        self.cell_width = cell_width
        self.bound_coords, self.center_coord = self.calc_cell_world_coords()
        self.piece = piece

    def calc_cell_world_coords(self):
        if self.r == 0:
            x_list = np.array([self.x, self.x, self.x + 1]) * self.cell_width
            y_list = np.array([self.y, self.y + 1, self.y]) * self.cell_width
            x_list_skewed = x_list + y_list * .5
        else:
            x_list = np.array([self.x + 1, self.x, self.x + 1]) * self.cell_width
            y_list = np.array([self.y + 1, self.y + 1, self.y]) * self.cell_width
            x_list_skewed = x_list + y_list * .5
        x_center, y_center = np.mean(x_list_skewed), np.mean(y_list)
        return list(zip(x_list_skewed, y_list)), (x_center, y_center)

    def create_cell_poly(self):
        coord = self.bound_coords
        cell_poly = arcade.create_polygon(coord, EVEN_GRID_COLOR if self.r else ODD_GRID_COLOR)
        return cell_poly

    def toggle(self, tog_val=None):
        if tog_val is None:
            self.piece = not self.piece
        else:
            self.piece = tog_val