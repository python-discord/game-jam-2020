import arcade
from .base import Base
from .util import arcade_int_to_string
from ..network import run
from server.network import run as server_run


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
        network_thread, receive, send = server_run("192.168.0.22")
        run("192.168.0.22")
        self.display.change_scenes("lobby", network_thread, receive, send)

    def draw(self):
        arcade.draw_text("Loading?", 15, 470, color=(150, 100, 100), font_size=35)  # connection status message

    def connect(self):
        network_thread, receive, send = run(self.ip)
        status = receive.get()
        if status == 0:
            # goto lobby
            print("tou")
            self.display.change_scenes("lobby", network_thread, receive, send)
        elif status == 1 or status == 5:
            self.status = "Invalid address"
        elif status == 2 or status == 3:
            self.status = "Connection failed"
        elif status == 4:
            self.status = "Invalid Hostname"
        else:
            print(status)
