from buttons import MenuButton
import arcade

PLAYER_SPEED = 0.5


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

        self.player_1_sprite = arcade.Sprite(":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png")
        self.player_1_sprite.center_x = 100
        self.player_1_sprite.center_y = 100
        self.player_1_sprite.change_y = PLAYER_SPEED
        self.player_sprite_list.append(self.player_1_sprite)

        self.player_2_sprite = arcade.Sprite(":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png")
        self.player_2_sprite.center_x = 1100
        self.player_2_sprite.center_y = 100
        self.player_2_sprite.change_x = -PLAYER_SPEED
        self.player_sprite_list.append(self.player_2_sprite)

        self.player_3_sprite = arcade.Sprite(":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png")
        self.player_3_sprite.center_x = 1100
        self.player_3_sprite.center_y = 700
        self.player_3_sprite.change_y = -PLAYER_SPEED
        self.player_sprite_list.append(self.player_3_sprite)

    def setup_buttons(self):
        from menuscreen import MenuView

        go_back = MenuButton(
            self,
            MenuView(),
            100,
            self.window.WINDOW_HEIGHT-50,
            200,
            100,
            "Go Back",
            theme=self.theme,
        )
        self.button_list.append(go_back)

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)
        self.setup_buttons()

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.UP:
            self.player_1_sprite.change_y = PLAYER_SPEED
            self.player_1_sprite.change_x = 0
        elif key == arcade.key.DOWN:
            self.player_1_sprite.change_y = -PLAYER_SPEED
            self.player_1_sprite.change_x = 0
        elif key == arcade.key.LEFT:
            self.player_1_sprite.change_x = -PLAYER_SPEED
            self.player_1_sprite.change_y = 0
        elif key == arcade.key.RIGHT:
            self.player_1_sprite.change_x = PLAYER_SPEED
            self.player_1_sprite.change_y = 0

        if key == arcade.key.W:
            self.player_2_sprite.change_y = PLAYER_SPEED
            self.player_2_sprite.change_x = 0
        elif key == arcade.key.S:
            self.player_2_sprite.change_y = -PLAYER_SPEED
            self.player_2_sprite.change_x = 0
        elif key == arcade.key.A:
            self.player_2_sprite.change_x = -PLAYER_SPEED
            self.player_2_sprite.change_y = 0
        elif key == arcade.key.D:
            self.player_2_sprite.change_x = PLAYER_SPEED
            self.player_2_sprite.change_y = 0

        if key == arcade.key.I:
            self.player_3_sprite.change_y = PLAYER_SPEED
            self.player_3_sprite.change_x = 0
        elif key == arcade.key.K:
            self.player_3_sprite.change_y = -PLAYER_SPEED
            self.player_3_sprite.change_x = 0
        elif key == arcade.key.J:
            self.player_3_sprite.change_x = -PLAYER_SPEED
            self.player_3_sprite.change_y = 0
        elif key == arcade.key.L:
            self.player_3_sprite.change_x = PLAYER_SPEED
            self.player_3_sprite.change_y = 0

    def update(self, delta_time):
        self.player_sprite_list.update()

    def on_draw(self):
        arcade.start_render()
        super().on_draw()

        self.player_sprite_list.draw()
