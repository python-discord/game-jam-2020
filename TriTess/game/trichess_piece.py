import os

import arcade
import numpy as np

PLAYER1_COLOR = arcade.color.IVORY
PLAYER2_COLOR = arcade.color.BLACK
PLAYER3_COLOR = arcade.color.BATTLESHIP_GREY
color_dict = {0: PLAYER1_COLOR, 1: PLAYER2_COLOR, 2: PLAYER3_COLOR}
data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)).rsplit(os.sep, 1)[0], 'data')
DEFAULT_SPRITE_SIZE = 20

MOVE_DICT = {0: lambda x, y, r: (x + 1, y + 1, not r) if r else (x, y, not r),
             1: lambda x, y, r: (x + 1, y, not r) if r else (x + 1, y - 1, not r),
             2: lambda x, y, r: (x + 1, y - 1, not r) if r else (x, y - 1, not r),
             3: lambda x, y, r: (x - 1, y - 1, not r) if r else (x, y, not r),
             4: lambda x, y, r: (x - 1, y + 1, not r) if r else (x - 1, y, not r),
             5: lambda x, y, r: (x, y + 1, not r) if r else (x - 1, y + 1, not r)}


class TriPiece(arcade.Sprite):
    def __init__(self, trigrid, piece_name, pos, orientation, player):
        """
        :type trigrid: the grid object that this piece is bound to
        :type piece_name: name of the piece type
        :type player: value that indicates the id of the player
        :type pos: three value (x,y,r) that determines the grid position of piece on the triangular grid
        :type orientation: a value between 0 to 5 that determines which direction the piece is facing
        """
        self.orientation = orientation
        self.trigrid = trigrid
        self.grid_x, self.grid_y, self.grid_r = pos
        sprite_image = os.path.join(data_dir, f'sprite_{piece_name}{player}.png')
        scale = (self.trigrid.cell_width / np.sqrt(3)) / DEFAULT_SPRITE_SIZE
        center_x, center_y = self.get_coord_from_pos()
        super().__init__(sprite_image, scale=scale, center_x=center_x, center_y=center_y)

        self.angle -= 60 * orientation
        self.player = player

    def get_coord_from_pos(self):
        x, y = self.trigrid.grid[self.grid_x][self.grid_y][self.grid_r].center_coord
        return x, y

    def list_valid_moves(self):
        return []

    def list_valid_attacks(self):
        return []

    def get_neighbor_pos(self, move, pos=None):
        """
        This function gets the position of the neighbor in the direction of move
        :param move: value between 0 to 5 corresponding to forward direction and moving clockwise with each increment
                     this takes into account the orientation of the piece as well
        :param pos: the initial position to calc the neighbor from if None then use the
        :return:
        """
        pos = (self.grid_x, self.grid_y, self.grid_r) if pos is None else pos
        normed_move = self.orientation - move + 5 % 6
        return MOVE_DICT[normed_move](*pos)

    def move(self, grid_x, grid_y, grid_r):
        self.grid_x, self.grid_y, self.grid_r = grid_x, grid_y, grid_r
        self.center_x, self.center_y = self.get_coord_from_pos()

    @staticmethod
    def create_piece(trigrid, piece_name, pos, orientation, player):
        return PIECE_DICT[piece_name](trigrid, pos, orientation, player)


class Pawn(TriPiece):
    piece_name = "pawn"

    def __init__(self, trigrid, pos, orientation, player):
        super().__init__(trigrid, self.piece_name, pos, orientation, player)

    def list_valid_moves(self):
        pos = self.get_neighbor_pos(0)
        pos2 = self.get_neighbor_pos(0, pos)
        return [pos, pos2]

    def list_valid_attacks(self):
        return [self.get_neighbor_pos(5), self.get_neighbor_pos(1)]


class Rook(TriPiece):
    piece_name = "rook"

    def __init__(self, trigrid, pos, orientation, player):
        super().__init__(trigrid, self.piece_name, pos, orientation, player)


class Bishop(TriPiece):
    piece_name = "bishop"

    def __init__(self, trigrid, pos, orientation, player):
        super().__init__(trigrid, self.piece_name, pos, orientation, player)


class UKnight(TriPiece):
    piece_name = "uknight"

    def __init__(self, trigrid, pos, orientation, player):
        super().__init__(trigrid, self.piece_name, pos, orientation, player)


class Knight(TriPiece):
    piece_name = "knight"

    def __init__(self, trigrid, pos, orientation, player):
        super().__init__(trigrid, self.piece_name, pos, orientation, player)


class Queen(TriPiece):
    piece_name = "queen"

    def __init__(self, trigrid, pos, orientation, player):
        super().__init__(trigrid, self.piece_name, pos, orientation, player)


class King(TriPiece):
    piece_name = "king"

    def __init__(self, trigrid, pos, orientation, player):
        super().__init__(trigrid, self.piece_name, pos, orientation, player)


PIECE_DICT = {"pawn": Pawn,
              "bishop": Bishop,
              "rook": Rook,
              "queen": Queen,
              "king": King,
              "knight": Knight,
              "uknight": UKnight}
