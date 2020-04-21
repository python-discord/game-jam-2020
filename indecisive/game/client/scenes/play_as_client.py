import arcade
from .base import Base
from .util import arcade_int_to_string
from ..network import run


class PlayAsClient(Base):
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

    def sprite_setup(self):
        self.spritedict = {
            "back": arcade.Sprite(
                "./assets/simple_button.png",
                scale=0.25,
                center_x=160,
                center_y=687.5
            ),
            "ip": arcade.Sprite(
                "./assets/simple_button.png",
                scale=0.25,
                center_x=160,
                center_y=622.5
            ),
            "connect": arcade.Sprite(
                "./assets/simple_button.png",
                scale=0.25,
                center_x=160,
                center_y=557.5
            ),
        }
        self.spritelist.extend(list(self.spritedict.values()))

    def update(self, delta_time: float) -> None:
        self.sceneTime += delta_time

    def draw(self):
        self.spritelist.draw()
        if len(self.ip) < 25:
            buffer = " " * (25 - len(self.ip))
        else:
            buffer = ""
        arcade.draw_text(buffer + self.ip[-25:], 15, 600, color=(255, 255, 255), font_size=35, width=560)
        arcade.draw_text(self.status, 15, 470, color=(150, 100, 100), font_size=35)  # connection status message

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

    def mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if self.spritedict["back"].collides_with_point((x, y)) is True:
            self.display.change_scenes("loading", startup=False)
        elif self.spritedict["ip"].collides_with_point((x, y)) is True:
            self.focus = "ip"
        elif self.spritedict["connect"].collides_with_point((x, y)) is True:
            self.connect()
        else:
            self.focus = None

    def key_press(self, key, modifiers):
        if self.focus == "ip":
            if key == arcade.key.BACKSPACE:
                if self.cursor_index == -1:
                    self.ip = self.ip[:-1]
                else:
                    self.ip = self.ip[:self.cursor_index] + self.ip[self.cursor_index + 1:]
            elif key == arcade.key.DELETE:
                if self.cursor_index == -1:
                    self.ip = self.ip[:-1]
                else:
                    self.ip = self.ip[:self.cursor_index + 1] + self.ip[self.cursor_index:]
            elif key == arcade.key.LEFT:
                self.cursor_index -= 1
                if self.cursor_index <= - (len(self.ip) + 2):
                    self.cursor_index = -1
            elif key == arcade.key.RIGHT:
                self.cursor_index += 1
                if self.cursor_index >= 0:
                    self.cursor_index = - (len(self.ip) + 1)
            else:
                key = arcade_int_to_string(key, modifiers)
                if key != "":
                    if self.cursor_index == -1:
                        self.ip = self.ip + key
                    else:
                        self.ip = self.ip[:self.cursor_index + 1] + key + self.ip[self.cursor_index + 1:]
