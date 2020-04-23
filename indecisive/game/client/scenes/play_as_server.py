import arcade
from .base import Base
from .util import arcade_int_to_string
from ..network import run
from server import run as server_run
import socket


class PlayAsServer(Base):
    def __init__(self, display: arcade.Window):
        self.display = display

        self.spritelist = arcade.SpriteList()
        self.spritedict = dict()
        self.sceneTime = 0
        self.ip = ""
        self.status = ""
        self.cursor_index = -1
        self.focus = None

        self.sprite_setup()

    def update(self, delta_time: float) -> None:
        self.sceneTime += delta_time
        network_thread, receive, send = run(socket.gethostbyname(socket.gethostname()))
        server_run(socket.gethostbyname(socket.gethostname()))

        status = receive.get()["status"]
        connection_number = receive.get()["data"]
        print(connection_number)
        self.display.change_scenes("lobby", network_thread, receive, send, connection_number, host=True)

    def draw(self):
        arcade.draw_text("Loading", 15, 670, color=(150, 100, 100), font_size=35)  # connection status message
