import arcade
from arcade.gui import Theme

import os
import string
import random
import logging

from ..networking.net_interface import Pipe
from ..gameconstants import SCREEN_WIDTH, SCREEN_HEIGHT


class StartGame(arcade.TextButton):
    def __init__(
        self, view_reference, x=0, y=0, width=100, height=40, text="Start!", theme=None
    ):
        super().__init__(x, y, width, height, text, theme=Theme)
        self.view_reference = view_reference

    def on_press(self):
        self.pressed = True

    def on_release(self) -> None:
        if self.pressed:
            self.pressed = False


class RoomView(arcade.View):
    def __init__(self, main_menu_view, room_name: str, username: str, mode: str):
        super().__init__()
        self.room_name = room_name
        self.username = username
        self.mode = mode

        self.pipe = None
        self.theme = None
        self.main_menu_view = main_menu_view

    def on_show(self) -> None:
        pass

    def on_draw(self) -> None:
        arcade.start_render()

        arcade.draw_text(
            f"Room name: {self.room_name} - Username: {self.username}",
            SCREEN_WIDTH * 0.3,
            SCREEN_HEIGHT * 0.9,
            arcade.color.WHITE,
        )

    def switch_back_with_error(self, error: str) -> None:
        """
        In case an error is found during calling setup(), go back to the
        Main Menu View.
        """
        logging.error(error)
        self.main_menu_view.setup()
        self.window.switch_to(self.main_menu_view)

    def setup(self, count: int = 0) -> None:
        error = None

        """
        This count is to avoid recursion errors in case the room_name already
        exists after trying to rename it 5 times
        """
        if count >= 5:
            self.switch_back_with_error(error)

        self.pipe = Pipe(os.getenv("SERVER"), int(os.getenv("PORT")))
        is_login_successful, response = self.pipe.login(
            self.mode, self.room_name, self.username
        )

        if not is_login_successful:
            if response == "rename":
                logging.error("Room name already exists. Renaming...")
                alphabet = string.ascii_letters
                self.room_name = f"{''.join(random.choices(alphabet, k=16))}"

                count += 1
                self.setup(count)
            elif response == "invalid":
                error = "Got an invalid response"
            elif response == "full":
                error = "Room is full"
            else:
                error = response

            if error:
                self.switch_back_with_error(error)

        else:
            if response == "created":
                logging.info("Login successful")
            elif response == "joined":
                logging.info("Successfully joined in a room")

    def set_button_textures(self) -> None:
        """Give the same style to all the buttons using self.theme."""
        normal = ":resources:gui_themes/Fantasy/Buttons/Normal.png"
        hover = ":resources:gui_themes/Fantasy/Buttons/Hover.png"
        clicked = ":resources:gui_themes/Fantasy/Buttons/Clicked.png"
        locked = ":resources:gui_themes/Fantasy/Buttons/Locked.png"
        self.theme.add_button_textures(normal, hover, clicked, locked)

    def set_buttons(self) -> None:
        """Initialize the Start Game button."""
        self.window.button_list.append(
            StartGame(
                self,
                0.5 * SCREEN_WIDTH,
                0.1 * SCREEN_HEIGHT,
                int(0.3 * SCREEN_WIDTH),
                int(0.1 * SCREEN_HEIGHT),
                theme=self.theme,
            )
        )

    def setup_theme(self) -> None:
        self.theme = Theme()
        self.theme.set_font = arcade.color.BLACK

        self.set_button_textures()
        self.set_buttons()
