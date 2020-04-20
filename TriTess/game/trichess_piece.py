import arcade
import numpy as np

PLAYER1_COLOR = arcade.color.IVORY
PLAYER2_COLOR = arcade.color.BLACK
PLAYER3_COLOR = arcade.color.BATTLESHIP_GREY
color_dict = {0: PLAYER1_COLOR, 1: PLAYER2_COLOR, 2: PLAYER3_COLOR}


class TriPiece:
    def __init__(self, pos, player, cell_width):
        self.pos = pos
        self.player = player
        self.cell_width = cell_width

    def get_shape(self):
        pass

    def moves(self, grid):
        pass

    def attack(self, grid):
        pass

    def calc_cell_coord(self, x, y, r):
        x_offset, y_offest = self.calc_face_offset(x, y, r)
        rot_mat = self.calc_rot()

        piece_coord = self.get_shape()
        piece_coord = piece_coord * self.cell_width
        piece_coord = piece_coord * rot_mat
        piece_coord[:, 0] += x_offset
        piece_coord[:, 1] += y_offest

        return list(zip(piece_coord[:, 0], piece_coord[:, 1]))

    #TODO calc offset
    def calc_face_offset(self, x, y, r):
        return 0, 0

    def piece_poly(self):
        coord = self.calc_cell_coord(*self.pos)

        arcade.create_polygon(coord, color_dict[self.player])

    def calc_rot(self):
        if self.player == 0:
            rot_mat = np.array([1, 0], [0, 1])
        elif self.player == 1:
            rot_mat = np.array([np.cos(np.pi * (210 / 180)), -np.sin(np.pi * (210 / 180))],
                               [np.sin(np.pi * (210 / 180)), np.cos(np.pi * (210 / 180))])
        elif self.player == 2:
            rot_mat = np.array([np.cos(np.pi * (330 / 180)), -np.sin(np.pi * (330 / 180))],
                               [np.sin(np.pi * (330 / 180)), np.cos(np.pi * (330 / 180))])
        return rot_mat


class Pawn(TriPiece):
    def __init__(self, pos, player):
        super().__init__(pos, player)
        self.shape = self.get_shape()

    def get_shape_coord(self):
        coord = ()

        return coord


class Rook(TriPiece):
    def __init__(self, pos, player):
        super().__init__(pos, player)
        self.shape = self.get_shape()

    def get_shape(self):
        return 1


class Bishop(TriPiece):
    def __init__(self, pos, player):
        super().__init__(pos, player)
        self.shape = self.get_shape()

    def get_shape(self):
        return 1


class UKnight(TriPiece):
    def __init__(self, pos, player):
        super().__init__(pos, player)
        self.shape = self.get_shape()

    def get_shape(self):
        return 1


class Knight(TriPiece):
    def __init__(self, pos, player):
        super().__init__(pos, player)
        self.shape = self.get_shape()

    def get_shape(self):
        return 1


class Queen(TriPiece):
    def __init__(self, pos, player):
        super().__init__(pos, player)
        self.shape = self.get_shape()

    def get_shape(self):
        return 1


class King(TriPiece):
    def __init__(self, pos, player):
        super().__init__(pos, player)
        self.shape = self.get_shape()

    def get_shape(self):
        return 1
