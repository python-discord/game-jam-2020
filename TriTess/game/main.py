import os

import arcade
from arcade import Theme

from TriTess.game.gui_elements import SkipTurnBtn, PlayHex2Btn, PlayTri3Btn


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 800


SCREEN_TITLE = "TriChess"
data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)).rsplit(os.sep, 1)[0], 'data')


class TriTess(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Set up the application.
        """

        super().__init__(width, height, title)
        self.game_type = None
        self.trigrid = None  # gets initialized when PlayTri3Btn or PlayHex2Btn is pressed
        self.info_text = None
        self.info_player = None
        self.background = None
        self.theme = None
        self.button_list = None

    def setup(self):
        self.background = arcade.load_texture(os.path.join(data_dir, "background.png"))
        self.info_text = arcade.TextLabel("Left click to select piece,"
                                          "right click to move piece,"
                                          "be last player with a king to win.", 60, 700)
        self.info_player = None
        self.setup_theme()
        self.set_buttons()

    def set_buttons(self):
        self.button_list = []
        self.button_list.append(PlayHex2Btn(self, 60, 625, 110, 50, theme=self.theme))
        self.button_list.append(PlayTri3Btn(self, 60, 570, 110, 50, theme=self.theme))
        self.button_list.append(SkipTurnBtn(self, 60, 515, 110, 50, theme=self.theme))

    def set_button_textures(self):
        normal = ":resources:gui_themes/Fantasy/Buttons/Normal.png"
        hover = ":resources:gui_themes/Fantasy/Buttons/Hover.png"
        clicked = ":resources:gui_themes/Fantasy/Buttons/Clicked.png"
        locked = ":resources:gui_themes/Fantasy/Buttons/Locked.png"
        self.theme.add_button_textures(normal, hover, clicked, locked)

    def setup_theme(self):
        self.theme = Theme()
        self.theme.set_font(24, arcade.color.WHITE)
        self.set_button_textures()

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        super().on_draw()

        # Draw the grid
        if self.game_type is not None:
            self.trigrid.on_draw(grid_coord=False)

        if self.trigrid is not None:
            arcade.draw_text(f"{self.trigrid.cur_player_name}", 60, 750, arcade.color.BLACK, 24)

    def on_mouse_press(self, coord_x, coord_y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        self.check_mouse_press_for_buttons(coord_x, coord_y)
        self.trigrid.on_mouse_press(coord_x, coord_y, button, modifiers)
        self.info_player.text = f"{self.trigrid.PLAYER_COLOR[self.trigrid.cur_player]}'s turn"
        self.on_draw()

    def check_mouse_press_for_buttons(self, x, y):
        """ Given an x, y, see if we need to register any button clicks. """
        for button in self.button_list:
            if x > button.center_x + button.width / 2:
                continue
            if x < button.center_x - button.width / 2:
                continue
            if y > button.center_y + button.height / 2:
                continue
            if y < button.center_y - button.height / 2:
                continue
            button.on_press()


def main():
    tritess_window = TriTess(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    tritess_window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
