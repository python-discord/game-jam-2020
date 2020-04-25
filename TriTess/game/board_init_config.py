p1_orient = 0
hex2_player1_init = [("pawn", (index, 1, 0), p1_orient, 0) for index in range(3, 8)] + \
                    [("pawn", (index, 1, 1), p1_orient, 0) for index in range(2, 8)] + \
                    [("rook", (3, 0, 1), p1_orient, 0),
                     ("rook", (7, 0, 1), p1_orient, 0),
                     ("knight", (4, 0, 0), p1_orient, 0),
                     ("knight", (7, 0, 0), p1_orient, 0),
                     ("knight", (5, 0, 1), p1_orient, 0),
                     ("bishop", (4, 0, 1), p1_orient, 0),
                     ("bishop", (6, 0, 1), p1_orient, 0),
                     ("king", (5, 0, 0), p1_orient, 0),
                     ("queen", (6, 0, 0), p1_orient, 0)]

p2_orient = 3
player_num = 2
hex2_player2_init = [("pawn", (index, 6, 0), p2_orient, player_num) for index in range(0, 6)] + \
                    [("pawn", (index, 6, 1), p2_orient, player_num) for index in range(0, 5)] + \
                    [("rook", (0, 7, 0), p2_orient, player_num),
                     ("rook", (4, 8, 0), p2_orient, player_num),
                     ("knight", (0, 7, 1), p2_orient, player_num),
                     ("knight", (3, 7, 1), p2_orient, player_num),
                     ("knight", (2, 7, 0), p2_orient, player_num),
                     ("bishop", (1, 6, 1), p2_orient, player_num),
                     ("bishop", (3, 6, 1), p2_orient, player_num),
                     ("king", (1, 7, 1), p2_orient, player_num),
                     ("queen", (2, 7, 1), p2_orient, player_num)]


p2_orient = 3
player_num = 2
trichess3_player1_init = [("pawn", (index, 6, 0), p2_orient, player_num) for index in range(0, 6)] + \
                         [("pawn", (index, 6, 1), p2_orient, player_num) for index in range(0, 5)] + \
                         [("rook", (0, 7, 0), p2_orient, player_num),
                     ("rook", (4, 8, 0), p2_orient, player_num),
                     ("knight", (0, 7, 1), p2_orient, player_num),
                     ("knight", (3, 7, 1), p2_orient, player_num),
                     ("knight", (2, 7, 0), p2_orient, player_num),
                     ("bishop", (1, 6, 1), p2_orient, player_num),
                     ("bishop", (3, 6, 1), p2_orient, player_num),
                     ("king", (1, 7, 1), p2_orient, player_num),
                     ("queen", (2, 7, 1), p2_orient, player_num)]

hex2_board_size = 12


def is_valid_hex2_cell(x, y, r):
    if r and x + y == hex2_board_size - 1:
        return False