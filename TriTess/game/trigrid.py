import arcade
import numpy as np
from . import trichess_piece, board_init_config

EVEN_GRID_COLOR = arcade.color.JASMINE
ODD_GRID_COLOR = arcade.color.LIGHT_PASTEL_PURPLE
ATTACKABLE_GRID_COLOR = arcade.color.CARMINE_RED
MOVABLE_GRID_COLOR = arcade.color.ASPARAGUS


class TriGrid:
    def __init__(self, board_size, cell_width, grid_type='hex2'):
        self.board_size = board_size
        self.cell_width = cell_width
        self.shape_list = None
        self.grid_map = self.init_grid(grid_type)
        self.piece_list = self.init_pieces(grid_type)
        self.num_players = board_init_config.num_player_for_grid[grid_type]
        self.on_draw()

    def init_grid(self, grid_type):
        grid_map = {}
        if grid_type == "hex2":
            for grid_x in range(board_init_config.hex2_board_size):
                for grid_y in range(board_init_config.hex2_board_size - grid_x):
                    for r in [False, True]:
                        if board_init_config.is_valid_hex2_cell(grid_x, grid_y, r):
                            grid_map[(grid_x, grid_y, r)] = TriCell(grid_x, grid_y, r, self.cell_width)

        return grid_map

    def init_pieces(self, grid_type):
        piece_list = arcade.SpriteList()
        if grid_type == "hex2":

            for name, pos, orientation, player in board_init_config.hex2_player1_init:
                cur_piece = trichess_piece.TriPiece.create_piece(self, name, pos, orientation, player)
                self.get_cell(*pos).piece = cur_piece
                piece_list.append(cur_piece)

            for name, pos, orientation, player in board_init_config.hex2_player2_init:
                cur_piece = trichess_piece.TriPiece.create_piece(self, name, pos, orientation, player)
                self.get_cell(*pos).piece = cur_piece
                piece_list.append(cur_piece)

            return piece_list

        elif grid_type == "trichess3":
            for name, pos, orientation, player in board_init_config.trichess3_player1_init:
                cur_piece = trichess_piece.TriPiece.create_piece(self, name, pos, orientation, player)
                self.get_cell(*pos).piece = cur_piece
                piece_list.append(cur_piece)

            for name, pos, orientation, player in board_init_config.trichess3_player2_init:
                cur_piece = trichess_piece.TriPiece.create_piece(self, name, pos, orientation, player)
                self.get_cell(*pos).piece = cur_piece
                piece_list.append(cur_piece)

            for name, pos, orientation, player in board_init_config.trichess3_player3_init:
                cur_piece = trichess_piece.TriPiece.create_piece(self, name, pos, orientation, player)
                self.get_cell(*pos).piece = cur_piece
                piece_list.append(cur_piece)

            return piece_list

    def update_shape_list(self):
        self.shape_list = arcade.ShapeElementList()
        for grid_posm, cell in self.grid_map.items():
            current_cell = cell.create_cell_poly()
            self.shape_list.append(current_cell)

    def get_grid_position(self, coord_x, coord_y):
        x = (coord_x - coord_y * 0.5) / self.cell_width
        y = coord_y / self.cell_width
        r = (y % 1) > 1 - (x % 1)
        print((x + y) % 2, y, x)
        return int(x), int(y), r

    def toggle_cell(self, x, y, r):
        self.grid_map[(x, y, r)].toggle()

    def is_valid_cell(self, x, y, r):
        return (x, y, r) in self.grid_map

    def get_player_at_cell(self, x, y, r):
        sel_cell = self.get_cell(x, y, r)
        return None if sel_cell.piece is None else sel_cell.piece.player

    def clear_highlights(self):
        for pos in self.grid_map:
            self.get_cell(*pos).set_highlight(None)

    def on_draw(self, grid_coord=False):
        self.update_shape_list()
        arcade.start_render()
        self.shape_list.draw()
        self.piece_list.draw()
        if grid_coord:
            for grid_x, grid_y, grid_r in self.grid_map:
                (x, y) = self.get_cell(grid_x, grid_y, grid_r).center_coord
                x -= 20
                arcade.draw_text(f'{grid_x, grid_y, int(grid_r)}', float(x), float(y), color=arcade.color.BLACK, font_size=12)

    def get_cell(self, grid_x, grid_y, grid_r):
        return self.grid_map[(grid_x, grid_y, grid_r)]


class TriCell:
    def __init__(self, x, y, r, cell_width, highlight=None, piece=None):
        self.x = x
        self.y = y
        self.r = r
        self.cell_width = cell_width
        self.highlight = highlight
        self.bound_coords, self.center_coord = self.calc_cell_world_coords()
        self.piece = piece

    def calc_cell_world_coords(self):
        if self.r:
            x_list = np.array([self.x + 1, self.x, self.x + 1]) * self.cell_width
            y_list = np.array([self.y + 1, self.y + 1, self.y]) * self.cell_width
            x_list_skewed = x_list + y_list * .5
        else:
            x_list = np.array([self.x, self.x, self.x + 1]) * self.cell_width
            y_list = np.array([self.y, self.y + 1, self.y]) * self.cell_width
            x_list_skewed = x_list + y_list * .5

        x_center, y_center = np.mean(x_list_skewed), np.mean(y_list)
        return list(zip(x_list_skewed, y_list)), (x_center, y_center)

    def create_cell_poly(self):
        coord = self.bound_coords
        if self.highlight is None:
            cell_color = EVEN_GRID_COLOR if self.r else ODD_GRID_COLOR
        elif self.highlight == 'movable':
            cell_color = MOVABLE_GRID_COLOR
        elif self.highlight == 'attackable':
            cell_color = ATTACKABLE_GRID_COLOR
        else:
            raise ValueError('cell is missing highlight')
        cell_poly = arcade.create_polygon(coord, cell_color)
        return cell_poly

    def toggle(self, tog_val=None):
        if tog_val is None:
            self.piece = not self.piece
        else:
            self.piece = tog_val

    def set_highlight(self, hightlight=None):
        self.highlight = hightlight
