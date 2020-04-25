import os

import arcade
import numpy as np

PLAYER1_COLOR = arcade.color.IVORY
PLAYER2_COLOR = arcade.color.BLACK
PLAYER3_COLOR = arcade.color.BATTLESHIP_GREY
color_dict = {0: PLAYER1_COLOR, 1: PLAYER2_COLOR, 2: PLAYER3_COLOR}
data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)).rsplit(os.sep, 1)[0], 'data')
DEFAULT_SPRITE_SIZE = 20
chess_thump = arcade.Sound(os.path.join(data_dir, "chess_tap.mp3"))
# TODO fix the fact that r changes depending on  orientation
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
        self.pos = pos
        sprite_image = os.path.join(data_dir, f'sprite_{piece_name}{player}.png')
        scale = (self.trigrid.cell_width / np.sqrt(3)) / DEFAULT_SPRITE_SIZE
        center_x, center_y = self.get_coord_from_pos()
        super().__init__(sprite_image, scale=scale, center_x=center_x, center_y=center_y)

        self.angle -= 60 * orientation
        self.player = player

    def get_coord_from_pos(self):
        x, y = self.trigrid.get_cell(*self.pos).center_coord
        return x, y

    def list_valid_moves(self):
        return []

    def is_blocked(self, pos):
        if self.trigrid.is_valid_cell(*pos):
            pos_piece = self.trigrid.get_cell(*pos).piece
            if pos_piece is None:
                return False
            elif pos_piece.player == self.player:
                return True
            else:
                return True
        else:
            return True

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
        pos = self.pos if pos is None else pos
        normed_move = (self.orientation - move + 5) % 6
        return MOVE_DICT[normed_move](*pos)

    def move_to(self, x, y, r):
        """
        remove self from current cell then set to selected coord cell at grid coordinate x, y, r
        :return:
        """
        self.trigrid.get_cell(*self.pos).piece = None
        self.trigrid.get_cell(x, y, r).piece = self
        self.pos = (x, y, r)
        self.center_x, self.center_y = self.get_coord_from_pos()
        chess_thump.play()

    @staticmethod
    def create_piece(trigrid, piece_name, pos, orientation, player):
        return PIECE_DICT[piece_name](trigrid, pos, orientation, player)


class Pawn(TriPiece):
    piece_name = "pawn"

    def __init__(self, trigrid, pos, orientation, player):
        super().__init__(trigrid, self.piece_name, pos, orientation, player)

    def list_valid_moves(self):
        valid_moves = []
        first_step = self.get_neighbor_pos(0)
        if self.trigrid.get_cell(*first_step).piece is None and self.trigrid.is_valid_cell(*first_step):
            valid_moves.append(first_step)
            second_step = self.get_neighbor_pos(0, first_step)
            if self.trigrid.get_cell(*second_step).piece is None and self.trigrid.is_valid_cell(*second_step):
                valid_moves.append(second_step)
        return valid_moves

    def list_valid_attacks(self):
        possible_attacks = [self.get_neighbor_pos(5), self.get_neighbor_pos(1)]
        return [attack for attack in possible_attacks if self.is_attackable(*attack)]

    def is_attackable(self, x, y, r):
        if self.trigrid.is_valid_cell(x, y, r):
            cell_piece = self.trigrid.get_cell(x, y, r).piece
            if cell_piece is not None and cell_piece.player is not self.player:
                return True
        return False


class Rook(TriPiece):
    piece_name = "rook"

    def __init__(self, trigrid, pos, orientation, player):
        super().__init__(trigrid, self.piece_name, pos, orientation, player)

    def list_valid_moves(self):
        valid_moves = []

        rook_direction_list = [lambda r: 1 if r else 2,
                               lambda r: 5 if r else 4,
                               lambda r: 1 if r else 0,
                               lambda r: 3 if r else 4,
                               lambda r: 3 if r else 2,
                               lambda r: 5 if r else 0]

        for rook_direction in rook_direction_list:
            cur_pos = self.pos
            while True:
                next_pos = self.get_neighbor_pos(rook_direction(cur_pos[2]), cur_pos)
                if not self.trigrid.is_valid_cell(*next_pos):
                    break
                player_at_next_cell = self.trigrid.get_player_at_cell(*next_pos)
                if player_at_next_cell == self.player:
                    break
                valid_moves.append(next_pos)
                if player_at_next_cell is not None:
                    break
                cur_pos = next_pos
        return valid_moves

    def list_valid_attacks(self):
        return self.list_valid_moves()


class Bishop(TriPiece):
    piece_name = "bishop"

    def __init__(self, trigrid, pos, orientation, player):
        super().__init__(trigrid, self.piece_name, pos, orientation, player)

    def list_valid_moves(self):
        valid_moves = []

        bishop_direction_list = [0, 1, 2, 3, 4, 5]
        for bishop_direction in bishop_direction_list:
            cur_pos = self.pos
            while True:
                next_pos = self.get_neighbor_pos(bishop_direction, cur_pos)
                if not self.trigrid.is_valid_cell(*next_pos):
                    break
                player_at_next_cell = self.trigrid.get_player_at_cell(*next_pos)
                if player_at_next_cell == self.player:
                    break
                valid_moves.append(next_pos)
                if player_at_next_cell is not None:
                    break
                cur_pos = next_pos
        return valid_moves

    def list_valid_attacks(self):
        return self.list_valid_moves()


class UKnight(TriPiece):
    piece_name = "uknight"

    def __init__(self, trigrid, pos, orientation, player):
        super().__init__(trigrid, self.piece_name, pos, orientation, player)


class Knight(TriPiece):
    piece_name = "knight"

    def __init__(self, trigrid, pos, orientation, player):
        super().__init__(trigrid, self.piece_name, pos, orientation, player)

    def list_valid_moves(self):
        possible_moves = []
        if self.pos[2]:
            tmp = self.get_neighbor_pos(0, self.get_neighbor_pos(0))
            possible_moves.append(self.get_neighbor_pos(1, tmp))
            possible_moves.append(self.get_neighbor_pos(5, tmp))
            tmp = self.get_neighbor_pos(2, self.get_neighbor_pos(2))
            possible_moves.append(self.get_neighbor_pos(1, tmp))
            possible_moves.append(self.get_neighbor_pos(3, tmp))
            tmp = self.get_neighbor_pos(4, self.get_neighbor_pos(4))
            possible_moves.append(self.get_neighbor_pos(3, tmp))
            possible_moves.append(self.get_neighbor_pos(5, tmp))
        else:
            tmp = self.get_neighbor_pos(0, self.get_neighbor_pos(0))
            possible_moves.append(self.get_neighbor_pos(2, tmp))
            possible_moves.append(self.get_neighbor_pos(4, tmp))
            tmp = self.get_neighbor_pos(2, self.get_neighbor_pos(2))
            possible_moves.append(self.get_neighbor_pos(0, tmp))
            possible_moves.append(self.get_neighbor_pos(4, tmp))
            tmp = self.get_neighbor_pos(4, self.get_neighbor_pos(4))
            possible_moves.append(self.get_neighbor_pos(0, tmp))
            possible_moves.append(self.get_neighbor_pos(2, tmp))

        possible_moves = [self.get_neighbor_pos(direction) for direction in range(6)]
        valid_moves = [pos for pos in possible_moves if not self.is_blocked(pos)]
        return valid_moves

    def list_valid_attacks(self):
        return self.list_valid_moves()


class Queen(TriPiece):
    piece_name = "queen"

    def __init__(self, trigrid, pos, orientation, player):
        super().__init__(trigrid, self.piece_name, pos, orientation, player)

    def list_valid_moves(self):
        valid_moves = []
        bishop_direction_list = [0, 1, 2, 3, 4, 5]
        for bishop_direction in bishop_direction_list:
            cur_pos = self.pos
            while True:
                next_pos = self.get_neighbor_pos(bishop_direction, cur_pos)
                if not self.trigrid.is_valid_cell(*next_pos):
                    break
                player_at_next_cell = self.trigrid.get_player_at_cell(*next_pos)
                if player_at_next_cell == self.player:
                    break
                valid_moves.append(next_pos)
                if player_at_next_cell is not None:
                    break
                cur_pos = next_pos

        rook_direction_list = [lambda r: 1 if r else 2,
                               lambda r: 5 if r else 4,
                               lambda r: 1 if r else 0,
                               lambda r: 3 if r else 4,
                               lambda r: 3 if r else 2,
                               lambda r: 5 if r else 0]

        for rook_direction in rook_direction_list:
            cur_pos = self.pos
            while True:
                next_pos = self.get_neighbor_pos(rook_direction(cur_pos[2]), cur_pos)
                if not self.trigrid.is_valid_cell(*next_pos):
                    break
                player_at_next_cell = self.trigrid.get_player_at_cell(*next_pos)
                if player_at_next_cell == self.player:
                    break
                valid_moves.append(next_pos)
                if player_at_next_cell is not None:
                    break
                cur_pos = next_pos
            return valid_moves

    def list_valid_attacks(self):
        return self.list_valid_moves()


class King(TriPiece):
    piece_name = "king"

    def __init__(self, trigrid, pos, orientation, player):
        super().__init__(trigrid, self.piece_name, pos, orientation, player)

    def list_valid_moves(self):
        possible_moves = [self.get_neighbor_pos(direction) for direction in range(6)]
        valid_moves = [pos for pos in possible_moves if not self.is_blocked(pos)]
        return valid_moves

    def list_valid_attacks(self):
        return self.list_valid_moves()


PIECE_DICT = {"pawn": Pawn,
              "bishop": Bishop,
              "rook": Rook,
              "queen": Queen,
              "king": King,
              "knight": Knight,
              "uknight": UKnight}
