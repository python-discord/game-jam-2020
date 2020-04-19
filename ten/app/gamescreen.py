from buttons import MenuButton
import arcade

PLAYER_SPEED = 0.5
PLAYER_SCALE = 1


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

    def get_direction(self):
        if self.change_x != 0:
            if self.change_x > 0:
                return "right"
            else:
                return "left"

        if self.change_y != 0:
            if self.change_y > 0:
                return "up"
            else:
                return "down"

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

    def setup(self):
        self.player_sprite_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

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
        self.player_1_sprite = PlayerSprite(idle_dict, up_frames, down_frames, left_frames, right_frames, 100, 100,
                                            "up", arcade.key.UP, arcade.key.DOWN, arcade.key.LEFT, arcade.key.RIGHT)
        self.player_2_sprite = PlayerSprite(idle_dict, up_frames, down_frames, left_frames, right_frames, 1100, 100,
                                            "left", arcade.key.W, arcade.key.S, arcade.key.A, arcade.key.D)
        self.player_3_sprite = PlayerSprite(idle_dict, up_frames, down_frames, left_frames, right_frames, 1100, 700,
                                            "down", arcade.key.I, arcade.key.K, arcade.key.J, arcade.key.L)

        self.player_sprite_list.append(self.player_1_sprite)
        self.player_sprite_list.append(self.player_2_sprite)
        self.player_sprite_list.append(self.player_3_sprite)

    def setup_buttons(self):
        from menuscreen import MenuView

        go_back = MenuButton(
            self,
            MenuView(),
            100,
            self.window.WINDOW_HEIGHT - 50,
            200,
            100,
            "Go Back",
            theme=self.theme,
        )
        self.button_list.append(go_back)

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)
        self.setup_buttons()


    def on_key_press(self, key, modifiers):
        self.player_1_sprite.on_key_press_control(key, modifiers)
        self.player_2_sprite.on_key_press_control(key, modifiers)
        self.player_3_sprite.on_key_press_control(key, modifiers)

    def update(self, delta_time):
        self.player_sprite_list.update()
        self.player_sprite_list.update_animation()

    def on_draw(self):
        arcade.start_render()
        super().on_draw()
        self.player_sprite_list.draw()
