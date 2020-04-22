import os

import arcade
import numpy as np

PLAYER1_COLOR = arcade.color.IVORY
PLAYER2_COLOR = arcade.color.BLACK
PLAYER3_COLOR = arcade.color.BATTLESHIP_GREY
color_dict = {0: PLAYER1_COLOR, 1: PLAYER2_COLOR, 2: PLAYER3_COLOR}
data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)).rsplit(os.sep, 0)[0], 'data')


class TriPiece(arcade.Sprite):
    def __init__(self, pos, player, image, trigrid):
        self.trigrid = trigrid
        super().__init__(image, self.trigrid.cell_width / 6)
        if player == 1:
            self.angle += 120
        elif player == 2:
            self.angle += 240

        self.pos = pos
        self.center_x, self.center_y = self.get_coord_from_pos(*self.pos)
        self.player = player

    def get_coord_from_pos(self, x, y, r):
        x, y = self.trigrid.get_grid_position(x, y, r)
        return x, y

    def list_valid_moves(self, grid):
        return []

    def list_valid_moves(self, grid):
        pass


class Pawn(TriPiece):
    def __init__(self, pos, player, scale=5):
        sprite_image = os.path.join(data_dir, f'sprite_pawn{player}.png')
        super().__init__(pos, player, sprite_image, scale)

    def list_valid_moves(self, grid):
        return []


class Rook(TriPiece):
    def __init__(self, pos, player, scale=5):
        sprite_image = os.path.join(data_dir, f'sprite_rook{player}.png')
        super().__init__(pos, player, sprite_image, scale)


class Bishop(TriPiece):
    def __init__(self, pos, player, scale=5):
        sprite_image = os.path.join(data_dir, f'sprite_bishop{player}.png')
        super().__init__(pos, player, sprite_image, scale)


class UKnight(TriPiece):
    def __init__(self, pos, player, scale=5):
        sprite_image = os.path.join(data_dir, f'sprite_uknight{player}.png')
        super().__init__(pos, player, sprite_image, scale)


class Knight(TriPiece):
    def __init__(self, pos, player, scale=5):
        sprite_image = os.path.join(data_dir, f'sprite_knight{player}.png')
        super().__init__(pos, player, sprite_image, scale)


class Queen(TriPiece):
    def __init__(self, pos, player, scale=5):
        sprite_image = os.path.join(data_dir, f'sprite_queen{player}.png')
        super().__init__(pos, player, sprite_image, scale)


class King(TriPiece):
    def __init__(self, pos, player, scale=5):
        sprite_image = os.path.join(data_dir, f'sprite_king{player}.png')
        super().__init__(pos, player, sprite_image, scale)
