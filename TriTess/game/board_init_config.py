num_players = {'hex2': 2,
               'tri3': 3}

board_size = {'hex2': 12,
              'tri3': 18}

player_flag = {'hex2': [True, True],
               'tri3': [True, True, True]}


def gen_hex2_grid_map(cell_width):
    def is_valid_hex2_cell(x, y, r):
        if r and x + y == board_size['hex2'] - 1:
            return False
        elif r not in [True, False] or 0 < x >= 8 or 0 < y >= 8 or x + y + r <= 3:
            return False
        return True

    hex2_grid_map = {}
    for grid_x in range(board_size['hex2']):
        for grid_y in range(board_size['hex2'] - grid_x):
            for grid_r in [False, True]:
                if is_valid_hex2_cell(grid_x, grid_y, grid_r):
                    hex2_grid_map[(grid_x, grid_y, grid_r)] = TriCell((grid_x, grid_y, grid_r), cell_width)
    return hex2_grid_map


def gen_tri3_grid_map(cell_width):
    def is_valid_trichess3_cell(x, y, r):
        if (x, y, r) in trichess3_good_list:
            return True
        elif r in [True, False] and 10 > x >= 0 and 10 > y >= 0 and 18 > x + y + r > 7:
            return True
        else:
            return False

    tri3_grid_map = {}
    for grid_x in range(board_size['tri3']):
        for grid_y in range(board_size['tri3'] - grid_x):
            for grid_r in [False, True]:
                if is_valid_trichess3_cell(grid_x, grid_y, grid_r):
                    tri3_grid_map[(grid_x, grid_y, grid_r)] = TriCell((grid_x, grid_y, grid_r), cell_width)
    return tri3_grid_map


grid_map = {"hex2": gen_hex2_grid_map,
            "tri3": gen_tri3_grid_map}

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
player_num = 1
hex2_player2_init = [("pawn", (index, 6, 0), p2_orient, player_num) for index in range(0, 6)] + \
                    [("pawn", (index, 6, 1), p2_orient, player_num) for index in range(0, 5)] + \
                    [("rook", (0, 7, 0), p2_orient, player_num),
                     ("rook", (4, 7, 0), p2_orient, player_num),
                     ("knight", (0, 7, 1), p2_orient, player_num),
                     ("knight", (3, 7, 1), p2_orient, player_num),
                     ("knight", (2, 7, 0), p2_orient, player_num),
                     ("bishop", (1, 7, 0), p2_orient, player_num),
                     ("bishop", (3, 7, 0), p2_orient, player_num),
                     ("king", (1, 7, 1), p2_orient, player_num),
                     ("queen", (2, 7, 1), p2_orient, player_num)]

player_orient = 0
player_num = 0
trichess3_player1_init = [("pawn", (index, 1, 0), player_orient, player_num) for index in range(6, 11)] + \
                         [("pawn", (index, 1, 1), player_orient, player_num) for index in range(6, 10)] + \
                         [("rook", (6, 0, 1), player_orient, player_num),
                          # ("rook", (10, 0, 1), player_orient, player_num),
                            ("rook", (5, 5, 1), player_orient, player_num),
                          ("knight", (7, 0, 0), player_orient, player_num),
                          ("knight", (8, 0, 1), player_orient, player_num),
                          ("knight", (10, 0, 0), player_orient, player_num),
                          ("bishop", (7, 0, 1), player_orient, player_num),
                          ("bishop", (9, 0, 1), player_orient, player_num),
                          ("king", (8, 0, 0), player_orient, player_num),
                          ("queen", (9, 0, 0), player_orient, player_num)]

player_orient = 4
player_num = 1
trichess3_player2_init = [("pawn", (8 + index, 8 - index, 0), player_orient, player_num) for index in range(-2, 3)] + \
                         [("pawn", (6 + index, 9 - index, 1), player_orient, player_num) for index in range(0, 4)] + \
                         [("rook", (6, 10, 1), player_orient, player_num),
                          ("rook", (10, 6, 1), player_orient, player_num),
                          ("knight", (7, 10, 0), player_orient, player_num),
                          ("knight", (10, 7, 0), player_orient, player_num),
                          ("knight", (8, 8, 1), player_orient, player_num),
                          ("bishop", (7, 9, 1), player_orient, player_num),
                          ("bishop", (9, 7, 1), player_orient, player_num),
                          ("king", (8, 9, 0), player_orient, player_num),
                          ("queen", (9, 8, 0), player_orient, player_num)]

player_orient = 2
player_num = 2
trichess3_player3_init = [("pawn", (1, index, 0), player_orient, player_num) for index in range(6, 11)] + \
                         [("pawn", (1, index, 1), player_orient, player_num) for index in range(6, 10)] + \
                         [("rook", (0, 6, 1), player_orient, player_num),
                          ("rook", (0, 10, 1), player_orient, player_num),
                          ("knight", (0, 7, 0), player_orient, player_num),
                          ("knight", (0, 10, 0), player_orient, player_num),
                          ("knight", (0, 8, 1), player_orient, player_num),
                          ("bishop", (0, 7, 1), player_orient, player_num),
                          ("bishop", (0, 9, 1), player_orient, player_num),
                          ("king", (0, 8, 0), player_orient, player_num),
                          ("queen", (0, 9, 0), player_orient, player_num)]

trichess3_good_list = {(0, 10, 0), (0, 10, 1), (1, 10, 0),
                       (6, 10, 0), (6, 10, 1), (7, 10, 0),
                       (0, 7, 0), (0, 6, 1), (1, 6, 0),
                       (6, 1, 0), (6, 0, 1), (7, 0, 0),
                       (10, 0, 0), (10, 0, 1), (10, 1, 0),
                       (10, 6, 0), (10, 6, 1), (10, 7, 0)}

from .trigrid import TriCell
