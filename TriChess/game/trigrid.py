import arcade
import numpy as np

EVEN_GRID_COLOR = arcade.color.JASMINE
ODD_GRID_COLOR = arcade.color.LIGHT_PASTEL_PURPLE
ATTACKABLE_GRID_COLOR = arcade.color.CARMINE_RED
MOVABLE_GRID_COLOR = arcade.color.ASPARAGUS
PLAYER_COLOR = {0: "White", 1: 'Black', 2: "Red"}


class TriGrid:
    def __init__(self, screen_width, screen_height, grid_type='hex2'):
        self.grid_type = grid_type
        self.board_center_x, self.board_center_y = screen_width/2, screen_height/2
        self.board_size = board_init_config.board_size[grid_type]
        self.cell_width = int(screen_width / self.board_size)

        self.grid_map = self.init_grid()
        self.piece_list = self.init_pieces()
        self.grid_cell_list = None
        self.num_players = board_init_config.num_players[grid_type]
        self.player_status = board_init_config.player_flag[self.grid_type]
        self.cur_player = 0
        self.cur_selected_cell = None
        self.cur_valid_moves = None
        self.cur_valid_attacks = None
        self.finished = False

    def cur_player_name(self):
        return PLAYER_COLOR[self.cur_player]

    def init_grid(self):
        return board_init_config.grid_map[self.grid_type](self.cell_width)

    def init_pieces(self):
        piece_list = arcade.SpriteList()

        if self.grid_type == "hex2":

            for name, pos, orientation, player in board_init_config.hex2_player1_init:
                cur_piece = trichess_piece.TriPiece.create_piece(self, name, pos, orientation, player)
                self.get_cell(pos).piece = cur_piece
                piece_list.append(cur_piece)

            for name, pos, orientation, player in board_init_config.hex2_player2_init:
                cur_piece = trichess_piece.TriPiece.create_piece(self, name, pos, orientation, player)
                self.get_cell(pos).piece = cur_piece
                piece_list.append(cur_piece)

            return piece_list

        elif self.grid_type == "tri3":

            for name, pos, orientation, player in board_init_config.trichess3_player1_init:
                cur_piece = trichess_piece.TriPiece.create_piece(self, name, pos, orientation, player)
                self.get_cell(pos).piece = cur_piece
                piece_list.append(cur_piece)

            for name, pos, orientation, player in board_init_config.trichess3_player2_init:
                cur_piece = trichess_piece.TriPiece.create_piece(self, name, pos, orientation, player)
                self.get_cell(pos).piece = cur_piece
                piece_list.append(cur_piece)

            for name, pos, orientation, player in board_init_config.trichess3_player3_init:
                cur_piece = trichess_piece.TriPiece.create_piece(self, name, pos, orientation, player)
                self.get_cell(pos).piece = cur_piece
                piece_list.append(cur_piece)

            return piece_list

    def update_grid_cell_list(self):
        self.grid_cell_list = arcade.ShapeElementList()
        for grid_pos, cell in self.grid_map.items():
            current_cell = cell.create_cell_poly()
            self.grid_cell_list.append(current_cell)

    def get_grid_position(self, coord_x, coord_y):
        x = (coord_x - coord_y * 0.5) / self.cell_width
        y = coord_y / self.cell_width
        r = (y % 1) > 1 - (x % 1)
        print((x + y) % 2, y, x)
        return int(x), int(y), r

    def is_valid_cell(self, pos):
        return pos in self.grid_map

    def get_player_at_cell(self, pos):
        sel_cell = self.get_cell(pos)
        return None if sel_cell.piece is None else sel_cell.piece.player

    def next_player(self):
        if sum(self.player_status) == 1:
            self.finished = True
        else:
            # select next player cycle through if player is dead
            next_player = (self.cur_player + 1) % self.num_players
            while not self.player_status[next_player]:
                next_player = (next_player + 1) % self.num_players
            self.cur_player = next_player

    def clear_highlights(self):
        for pos in self.grid_map:
            self.get_cell(pos).set_highlight(None)

    def on_mouse_press(self, coord_x, coord_y, button, modifiers):
        pos = self.get_grid_position(coord_x, coord_y)
        if pos in self.grid_map:
            print(f"Click coordinates: ({coord_x}, {coord_y}). Grid coordinates: ({pos})")

            if button == arcade.MOUSE_BUTTON_LEFT:
                self.clear_highlights()
                self.cur_selected_cell = self.get_cell(pos)
                if self.cur_selected_cell.piece is not None and self.cur_selected_cell.piece.player == self.cur_player:
                    self.cur_valid_attacks = self.cur_selected_cell.piece.list_valid_attacks()
                    for attack_pos in self.cur_valid_attacks:
                        self.get_cell(attack_pos).set_highlight("attackable")

                    self.cur_valid_moves = self.cur_selected_cell.piece.list_valid_moves()
                    for move_pos in self.cur_valid_moves:
                        self.get_cell(move_pos).set_highlight("movable")

                else:
                    self.clear_selection()

            elif button == arcade.MOUSE_BUTTON_RIGHT:
                if self.cur_selected_cell is not None:
                    new_cell = self.get_cell(pos)
                    # if selected cell is a valid to attack and if there is a piece there that is not the current
                    # player's then remove the piece on the selceted and move current cell piece
                    if pos in self.cur_valid_attacks and new_cell.piece is not None \
                            and self.cur_selected_cell.piece.player != new_cell.piece.player:

                        if new_cell.piece.piece_name == 'king':
                            # if king killed set player as dead
                            self.player_status[new_cell.piece.player] = False

                        new_cell.piece.remove_from_sprite_lists()
                        new_cell.piece = None
                        self.cur_selected_cell.piece.move_to(pos)
                        self.next_player()

                    elif pos in self.cur_valid_moves:
                        self.get_cell(pos).piece = self.cur_selected_cell.piece
                        self.cur_selected_cell.piece.move_to(pos)
                        self.next_player()
                self.clear_selection()

    def clear_selection(self):
        self.cur_selected_cell = None
        self.cur_valid_moves = None
        self.cur_valid_attacks = None
        self.clear_highlights()

    def on_draw(self, grid_coord=False):
        self.update_grid_cell_list()
        self.grid_cell_list.draw()
        self.piece_list.draw()
        if grid_coord:
            for pos in self.grid_map:
                grid_x, grid_y, grid_r = pos
                (x, y) = self.get_cell(pos).center_coord
                x -= 17
                y -= 5
                arcade.draw_text(f'{grid_x}, {grid_y}, {int(grid_r)}',
                                 float(x), float(y), color=arcade.color.BLACK, font_size=10)

    def get_cell(self, pos):
        return self.grid_map[pos]


class TriCell:
    def __init__(self, pos, cell_width, highlight=None, piece=None):
        self.pos = pos
        self.cell_width = cell_width
        self.highlight = highlight
        self.bound_coords, self.center_coord = self.calc_cell_world_coords()
        self.piece = piece

    def calc_cell_world_coords(self):
        x, y, r = self.pos
        if r:
            x_list = np.array([x + 1, x, x + 1]) * self.cell_width
            y_list = np.array([y + 1, y + 1, y]) * self.cell_width
            x_list_skewed = x_list + y_list * .5
        else:
            x_list = np.array([x, x, x + 1]) * self.cell_width
            y_list = np.array([y, y + 1, y]) * self.cell_width
            x_list_skewed = x_list + y_list * .5

        x_center, y_center = np.mean(x_list_skewed), np.mean(y_list)
        return list(zip(x_list_skewed, y_list)), (x_center, y_center)

    def create_cell_poly(self):
        coord = self.bound_coords
        if self.highlight is None:
            cell_color = EVEN_GRID_COLOR if self.pos[2] else ODD_GRID_COLOR
        elif self.highlight == 'movable':
            cell_color = MOVABLE_GRID_COLOR
        elif self.highlight == 'attackable':
            cell_color = ATTACKABLE_GRID_COLOR
        else:
            raise ValueError('cell is missing highlight')
        cell_poly = arcade.create_polygon(coord, cell_color)
        return cell_poly

    def set_highlight(self, hightlight=None):
        self.highlight = hightlight


from . import trichess_piece, board_init_config
