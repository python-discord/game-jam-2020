import os
from os.path import join, dirname, realpath
import arcade


from TriTess.game.gui_elements import SkipTurnBtn, PlayHex2Btn, PlayTri3Btn

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 800

SCREEN_TITLE = "TriChess"
data_dir = join(dirname(realpath(__file__)).rsplit(os.sep, 1)[0], 'data')
party_horn = arcade.Sound(join(data_dir, 'party_horn.mp3'))


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
        self.button_list = None

    def setup(self):
        self.background = arcade.load_texture(join(data_dir, "background.png"))
        self.set_buttons()

    def set_buttons(self):
        self.button_list = [PlayHex2Btn(self, 90, 740, 165, 75),
                            PlayTri3Btn(self, 90, 640, 165, 75),
                            SkipTurnBtn(self, 90, 540, 165, 75)]

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
            self.button_list[2].active = True
            arcade.draw_text(f"Instructions:\n\n"
                             f"left click to select\n\n"
                             f"right click to move\n\n"
                             f"kill their king to win",
                             20, SCREEN_HEIGHT*.04, arcade.color.WHITE, 24, bold=True,
                             align="left")

            if self.trigrid.finished:
                party_horn.play()
                arcade.draw_text(f"{self.trigrid.cur_player_name()} WINS",
                                 SCREEN_WIDTH / 2, SCREEN_HEIGHT * .9, arcade.color.WHITE, 30, bold=True,
                                 align="center", anchor_x="center", anchor_y="center")
            else:
                arcade.draw_text(f"{self.trigrid.cur_player_name()}'s turn",
                                 SCREEN_WIDTH / 2, SCREEN_HEIGHT * .95, arcade.color.WHITE, 30, bold=True,
                                 align="center", anchor_x="center", anchor_y="center")

    def on_mouse_press(self, coord_x, coord_y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        self.check_mouse_press_for_buttons(coord_x, coord_y)
        if self.trigrid is not None:
            self.trigrid.on_mouse_press(coord_x, coord_y, button, modifiers)
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
