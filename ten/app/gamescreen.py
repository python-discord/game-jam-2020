from buttons import MenuButton
import arcade

PLAYER_SPEED = 0.5
PLAYER_SCALE = 1

key = {
    119: "W",
    97: "A",
    115: "S",
    100: "D",
    105: "I",
    106: "J",
    107: "K",
    108: "L",
    65361: "←",
    65362: "↑",
    65363: "→",
    65364: "↓",
}


class PlayerText:
    def __init__(self, player_sprite):
        self.player_sprite = player_sprite
        self.text = key[self.player_sprite.get_direction(key=True)]
        self.x_pos = self.player_sprite.center_x
        self.y_pos = self.player_sprite.center_y

    def draw(self):
        arcade.draw_text(self.text, self.x_pos, self.y_pos, arcade.color.BLACK, 100)

    def update(self):
        self.text = key[self.player_sprite.get_direction(key=True)]
        self.x_pos = self.player_sprite.center_x
        self.y_pos = self.player_sprite.center_y


class PlayerSprite(arcade.Sprite):
    def __init__(self, idle_dict, up_frames, down_frames, left_frames, right_frames, x, y, default_direction, up_key,
                 down_key, left_key, right_key):
        super().__init__()
        self.current_texture_counter = 0
        self.idle_dict = idle_dict
        self.up_frames = up_frames
        self.down_frames = down_frames
        self.left_frames = left_frames
        self.right_frames = right_frames
        self.center_x = x
        self.center_y = y
        self.scale = 0.4
        self.up_key = up_key
        self.down_key = down_key
        self.left_key = left_key
        self.right_key = right_key

        self.texture = idle_dict[default_direction]
        if default_direction == "up":
            self.change_y = PLAYER_SPEED
        elif default_direction == "down":
            self.change_y = -PLAYER_SPEED
        elif default_direction == "left":
            self.change_x = -PLAYER_SPEED
        elif default_direction == "right":
            self.change_x = PLAYER_SPEED

    def on_key_press_control(self, key, modifiers):
        if key == self.up_key:
            self.change_x = 0
            self.change_y = PLAYER_SPEED
        elif key == self.down_key:
            self.change_x = 0
            self.change_y = -PLAYER_SPEED
        elif key == self.left_key:
            self.change_y = 0
            self.change_x = -PLAYER_SPEED
        elif key == self.right_key:
            self.change_y = 0
            self.change_x = PLAYER_SPEED

    def get_direction(self, key=False):
        if self.change_x != 0:
            if self.change_x > 0:
                return self.right_key if key else "right"
            else:
                return self.left_key if key else "left"

        if self.change_y != 0:
            if self.change_y > 0:
                return self.up_key if key else "up"
            else:
                return self.down_key if key else "down"

    def update_animation(self, delta_time: float = 1 / 60):
        if self.get_direction() == "up":
            self.texture = self.up_frames[int(self.current_texture_counter / (10 / PLAYER_SPEED)) % len(self.up_frames)]
        elif self.get_direction() == "down":
            self.texture = self.down_frames[
                int(self.current_texture_counter / (10 / PLAYER_SPEED)) % len(self.down_frames)]
        elif self.get_direction() == "left":
            self.texture = self.left_frames[
                int(self.current_texture_counter / (10 / PLAYER_SPEED)) % len(self.left_frames)]
        elif self.get_direction() == "right":
            self.texture = self.right_frames[
                int(self.current_texture_counter / (10 / PLAYER_SPEED)) % len(self.right_frames)]

        self.current_texture_counter += 1


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        print("GameView Created")
        self.theme = None
        self.player_1_sprite = None
        self.player_2_sprite = None
        self.player_3_sprite = None

        self.player_sprite_list = None

        self.wall_list = None
        self.floor_list = None

        self.player_1_sprite_text = None
        self.player_2_sprite_text = None
        self.player_3_sprite_text = None

    def setup(self):
        self.player_sprite_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()

        # Loading all the textures for the players
        self.textures = []
        left = arcade.load_texture("assets/player1leftright.png", mirrored=True)
        right = arcade.load_texture("assets/player1leftright.png")
        up = arcade.load_texture("assets/player1up.png")
        down = arcade.load_texture("assets/player1down.png")
        idle_dict = {"up": up, "down": down, "left": left, "right": right}
        right_frames = []
        left_frames = []
        for x in range(7):
            right_frames.append(arcade.load_texture(f"assets/character_robot_walk{x}.png"))
            left_frames.append(
                arcade.load_texture(f"assets/character_robot_walk{x}.png", mirrored=True))
        up1 = arcade.load_texture("assets/player1up1.png")
        up2 = arcade.load_texture("assets/player1up1.png", mirrored=True)
        up_frames = [up1, up2]
        down1 = arcade.load_texture("assets/player1down1.png")
        down2 = arcade.load_texture("assets/player1down2.png", mirrored=True)
        down3 = arcade.load_texture("assets/player1down2.png")
        down4 = arcade.load_texture("assets/player1down1.png", mirrored=True)
        down_frames = [down1, down2, down3, down4, down3, down2]

        self.player_1_sprite = PlayerSprite(idle_dict, up_frames, down_frames, left_frames, right_frames, 150, 200,
                                            "up", arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT)
        self.player_2_sprite = PlayerSprite(idle_dict, up_frames, down_frames, left_frames, right_frames, 1000, 200,
                                            "left", arcade.key.W, arcade.key.S, arcade.key.A, arcade.key.D)
        self.player_3_sprite = PlayerSprite(idle_dict, up_frames, down_frames, left_frames, right_frames, 1000, 600,
                                            "down", arcade.key.I, arcade.key.K, arcade.key.J, arcade.key.L)

        # Creating all the player sprites and the text that follows the players
        self.player_sprite_list.append(self.player_1_sprite)
        self.player_sprite_list.append(self.player_2_sprite)
        self.player_sprite_list.append(self.player_3_sprite)
        self.player_1_sprite_text = PlayerText(self.player_1_sprite)
        self.player_2_sprite_text = PlayerText(self.player_2_sprite)
        self.player_3_sprite_text = PlayerText(self.player_3_sprite)

        # Grid for game play
        self.grid_layout = [
            [4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6],
        ]

        x_offset = 0
        y_offset = 0
        tile_width = 64
        tile_height = 64
        for row_index, row in enumerate(self.grid_layout):
            for col_index, column_value in enumerate(row):
                if column_value == 0:
                    sprite = arcade.Sprite("assets/tile_69.png")
                elif column_value == 1:
                    sprite = arcade.Sprite("assets/tile_282.png")
                elif column_value == 2:
                    sprite = arcade.Sprite("assets/wall_side_edge.png")
                elif column_value == 3:
                    sprite = arcade.Sprite("assets/tile_281.png")
                elif column_value == 4:
                    sprite = arcade.Sprite("assets/tile_280.png")
                elif column_value == 5:
                    sprite = arcade.Sprite("assets/bottom_left_corner.png")
                elif column_value == 6:
                    sprite = arcade.Sprite("assets/bottom_right_corner.png")
                else:
                    continue

                sprite.left = col_index * tile_width + x_offset
                sprite.top = self.window.WINDOW_HEIGHT - y_offset - (row_index * tile_height)
                print(sprite.left, sprite.top)
                if column_value != 0:
                    self.wall_list.append(sprite)
                else:
                    self.floor_list.append(sprite)

    def setup_buttons(self):
        from menuscreen import MenuView

        go_back = MenuButton(
            self,
            MenuView(),
            50,
            self.window.WINDOW_HEIGHT - 25,
            100,
            50,
            "Go Back",
            theme=self.theme,
        )
        self.button_list.append(go_back)

    def on_show(self):
        self.setup_buttons()
        arcade.set_background_color(arcade.color.WHITE)

    def on_key_press(self, key, modifiers):
        self.player_1_sprite.on_key_press_control(key, modifiers)
        self.player_2_sprite.on_key_press_control(key, modifiers)
        self.player_3_sprite.on_key_press_control(key, modifiers)

    def update(self, delta_time):
        self.player_sprite_list.update()
        self.player_sprite_list.update_animation()
        self.wall_list.update()
        self.floor_list.update()

        self.player_1_sprite_text.update()
        self.player_2_sprite_text.update()
        self.player_3_sprite_text.update()

    def on_draw(self):
        arcade.start_render()
        super().on_draw()
        self.wall_list.draw()
        self.floor_list.draw()
        self.player_sprite_list.draw()

        self.player_1_sprite_text.draw()
        self.player_2_sprite_text.draw()
        self.player_3_sprite_text.draw()
