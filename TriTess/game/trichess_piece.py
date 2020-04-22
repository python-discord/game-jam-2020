import os

import arcade
import numpy as np

PLAYER1_COLOR = arcade.color.IVORY
PLAYER2_COLOR = arcade.color.BLACK
PLAYER3_COLOR = arcade.color.BATTLESHIP_GREY
color_dict = {0: PLAYER1_COLOR, 1: PLAYER2_COLOR, 2: PLAYER3_COLOR}
data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)).rsplit(os.sep, 1)[0], 'data')
DEFAULT_SPRITE_SIZE = 32


class TriPiece(arcade.Sprite):
    def __init__(self, pos, player, piece_name, trigrid):
        self.trigrid = trigrid
        self.grid_x, self.grid_y, self.grid_r = pos
        sprite_image = os.path.join(data_dir, f'sprite_{piece_name}{player}.png')
        scale = (self.trigrid.cell_width / np.sqrt(3)) / DEFAULT_SPRITE_SIZE
        center_x, center_y = self.get_coord_from_pos()
        super().__init__(sprite_image, scale=scale, center_x=center_x, center_y=center_y)

        if player == 1:
            self.angle += 120
        elif player == 2:
            self.angle += 240

        self.player = player

    def get_coord_from_pos(self):
        x, y = self.trigrid.grid[self.grid_x][self.grid_y][self.grid_r].center_coord
        return x, y

    def list_valid_moves(self):
        return []

    def list_valid_attacks(self):
        return []

    @staticmethod
    def create_piece(name, pos, player, trigrid):
        return PIECE_DICT[name](pos, player, trigrid)


class Pawn(TriPiece):
    piece_name = "pawn"

    def __init__(self, pos, player, trigrid):
        super().__init__(pos, player, self.piece_name, trigrid)

    def list_valid_moves(self):
        if self.grid_r == 1:
            return [(self.grid_x + 1, self.grid_y + 1, not self.grid_r),
                    (self.grid_x + 1, self.grid_y + 1, self.grid_r)]
        else:
            return [(self.grid_x, self.grid_y, not self.grid_r), (self.grid_x + 1, self.grid_y + 1, self.grid_r)]

    def list_valid_attack(self):
        return [(self.grid_x + 1, self.grid_y, self.grid_r), (self.grid_x, self.grid_y + 1, self.grid_r)]


class Rook(TriPiece):
    piece_name = "rook"

    def __init__(self, pos, player, scale=5):
        super().__init__(pos, player, self.piece_name, scale)


class Bishop(TriPiece):
    piece_name = "bishop"

    def __init__(self, pos, player, scale=5):
        super().__init__(pos, player, self.piece_name, scale)


class UKnight(TriPiece):
    piece_name = "uknight"

    def __init__(self, pos, player, scale=5):
        super().__init__(pos, player, self.piece_name, scale)


class Knight(TriPiece):
    piece_name = "knight"

    def __init__(self, pos, player, scale=5):
        super().__init__(pos, player, self.piece_name, scale)


class Queen(TriPiece):
    piece_name = "queen"

    def __init__(self, pos, player, scale=5):
        super().__init__(pos, player, self.piece_name, scale)


class King(TriPiece):
    piece_name = "king"

    def __init__(self, pos, player, scale=5):
        super().__init__(pos, player, self.piece_name, scale)


PIECE_DICT = {"pawn": Pawn,
              "bishop": Bishop,
              "rook": Rook,
              "queen": Queen,
              "king": King,
              "knight": Knight,
              "uknight": UKnight}
