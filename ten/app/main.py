from gamescreen import GameView
from arcade.gui import *

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800


class MenuButton(TextButton):
    def __init__(self, current_view, next_view, x, y, width, height, text, theme=None):
        super().__init__(x, y, width, height, text, theme=theme)
        self.next_view = next_view
        self.current_view = current_view

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            self.current_view.window.show_view(self.next_view)


class QuitButton(TextButton):
    def __init__(self, x, y, width, height, text, theme=None):
        super().__init__(x, y, width, height, text, theme=theme)

    def on_press(self):
        self.pressed = True

    def on_release(self):
        if self.pressed:
            arcade.close_window()


class InstructionView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.BABY_BLUE)

    def update(self, delta_time):
        pass

    def on_draw(self):
        arcade.start_render()
        super().on_draw()


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
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
            int(WINDOW_WIDTH / 2),
            int(WINDOW_HEIGHT / 2),
            200,
            100,
            "Play",
            theme=self.theme,
        )
        instructions_button = MenuButton(
            self,
            InstructionView(),
            int(WINDOW_WIDTH / 2),
            int(WINDOW_HEIGHT / 3),
            200,
            100,
            "Instructions",
            theme=self.theme,
        )
        quit_button = QuitButton(
            int(WINDOW_WIDTH / 2),
            int(WINDOW_HEIGHT / 6),
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
            WINDOW_WIDTH / 2,
            (WINDOW_HEIGHT / 3) * 2,
            arcade.color.BLACK,
            font_size=30,
            anchor_x="center",
        )

    def update(self, delta_time):
        pass

    def setup_theme(self):
        self.theme = Theme()
        self.theme.set_font(24, arcade.color.WHITE)


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, "Main Menu")
    menu_view = MenuView()
    menu_view.setup()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
