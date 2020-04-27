import arcade

import socket
import os
import string
import random
import logging
from threading import Thread

from .gameview import GameView
from ..networking.net_interface import Pipe
from ..gameconstants import SCREEN_WIDTH, SCREEN_HEIGHT


class RoomView(arcade.View):
    def __init__(
        self, main_menu_view: arcade.View, room_name: str, username: str, mode: str
    ):
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
        self.window.show_view(self.main_menu_view)

    def setup(self, count: int = 0) -> None:
        error = None
        """
        This count is to avoid recursion errors in case the room_name already
        exists after trying to rename it 5 times
        """
        if count >= 5:
            self.switch_back_with_error(error)

        self.pipe = Pipe(socket.gethostname(), int(os.getenv("PORT")))
        is_login_successful, response = self.pipe.login(
            self.mode, self.room_name, self.username
        )

        if not is_login_successful:
            if response == "rename":
                logging.error("Room name already exists. Renaming...")
                alphabet = string.ascii_letters
                self.room_name = f"{''.join(random.choices(alphabet, k=6))}"

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
                logging.info("Room created successfully")
            elif response == "joined":
                logging.info("Successfully joined in a room")

            self.waiting_room_thread = Thread(
                target=self.await_start, args=[self.pipe, response]
            )
            self.waiting_room_thread.start()

    def await_start(self, pipe: Pipe, response: str) -> None:
        while True:
            packet = self.pipe.await_response()
            logging.debug(f"Receiving packet in RoomView: {packet}")

            if packet[0] == "Start":
                logging.info("Starting the game...")

                char = packet[3].split().index(str(self.username)) + 1
                game_view = GameView(self.pipe, char)
                game_view.setup()
                self.window.show_view(game_view)

                break
