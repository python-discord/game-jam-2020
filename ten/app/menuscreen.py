from gamescreen import GameView
from instructionsscreen import InstructionView
from arcade.gui import *
from buttons import QuitButton, MenuButton

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        print("Menu Created")

    def setup(self):
        arcade.set_background_color(arcade.color.AMAZON)
        self.setup_theme()
        self.set_buttons()

    def set_buttons(self):
        normal = ":resources:gui_themes/Fantasy/Buttons/Normal.png"
        hover = ":resources:gui_themes/Fantasy/Buttons/Hover.png"
        clicked = ":resources:gui_themes/Fantasy/Buttons/Clicked.png"
        locked = ":resources:gui_themes/Fantasy/Buttons/Locked.png"
        self.theme.add_button_textures(normal, hover, clicked, locked)

        play_button = MenuButton(
            self,
            GameView(),
            int(self.window.WINDOW_WIDTH / 2),
            int(self.window.WINDOW_HEIGHT / 2),
            200,
            100,
            "Play",
            theme=self.theme,
        )
        instructions_button = MenuButton(
            self,
            InstructionView(),
            int(self.window.WINDOW_WIDTH / 2),
            int(self.window.WINDOW_HEIGHT / 3),
            200,
            100,
            "Instructions",
            theme=self.theme,
        )
        quit_button = QuitButton(
            int(self.window.WINDOW_WIDTH / 2),
            int(self.window.WINDOW_HEIGHT / 6),
            200,
            100,
            "Quit",
            theme=self.theme,
        )
        menu_buttons = [play_button, instructions_button, quit_button]
        self.button_list += menu_buttons

    def on_draw(self):
        arcade.start_render()
        super().on_draw()
        arcade.draw_text(
            "Menu Screen",
            self.window.WINDOW_WIDTH / 2,
            (self.window.WINDOW_HEIGHT / 3) * 2,
            arcade.color.BLACK,
            font_size=30,
            anchor_x="center",
        )

    def update(self, delta_time):
        pass

    def setup_theme(self):
        self.theme = Theme()
        self.theme.set_font(24, arcade.color.WHITE)
