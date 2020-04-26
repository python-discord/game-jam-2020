import arcade
import logging

from ..gameconstants import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_PATH
from multiprocessing import Process, Queue

from .gameview import GameView
from ..networking.net_interface import Pipe

import os
from textwrap import dedent

DATA_PATH = f"{GAME_PATH}/data"


def networking(forward, feedback):
    while True:
        pipe = Pipe(server=os.getenv("PORT"), port=int(os.getenv("PORT")))
        response = pipe.login()
        feedback.put(response)
        if response:
            break

    while True:
        response = pipe.await_response()
        if response[0] == "Team count":
            feedback.put(response[:2])
        elif response[0] == "Start":
            feedback.put(["Start", response[1]])
            break
    while True:
        items_no = forward.qsize()

        for _ in range(items_no - 2):
            forward.get()
        data = list(forward.get())
        feedback.put(pipe.transport(data))


class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.theme = None
        self.half_width = SCREEN_WIDTH / 2
        self.half_height = SCREEN_HEIGHT / 2

        self.background = None
        self.status = "Connecting to server..."

        self.connected = False
        self.forward = Queue()
        self.feedback = Queue()

        self.start = arcade.load_sound(f"{DATA_PATH}/start.wav")

    def on_show(self) -> None:
        pass

    def on_draw(self) -> None:
        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(
            0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background
        )
        arcade.draw_text(
            dedent(self.status),
            550,
            100,
            arcade.color.WHITE,
            font_size=15,
            anchor_x="center",
        )

    def setup(self) -> None:
        """Initialize the menu."""
        self.background = arcade.load_texture(f"{DATA_PATH}/b2.gif")
        sync = Process(target=networking, args=(self.forward, self.feedback,))
        sync.start()

    def on_update(self, delta_time: float):
        if not self.feedback.empty():
            success = self.feedback.get()
            if not self.connected:
                if success:
                    logging.info("Connected")
                    self.status = "Waiting for other players... (1)"
                    self.connected = True
                else:
                    logging.info("Cannot connect to server")
                    self.status = "Error in connection (Retrying)"
            else:
                if success[0] == "Team count":
                    self.status = f"Waiting for other players... ({success[1]})"
                elif success[0] == "Start":
                    logging.info("Starting game")
                    self.status = "Launching game"
                    self.start.play(volume=0.5)

                    game_view = GameView()
                    self.window.show_view(game_view)
                    game_view.setup(self.forward, self.feedback, success[1])
