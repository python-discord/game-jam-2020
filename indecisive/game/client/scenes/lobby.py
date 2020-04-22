import json

import arcade
from .base import Base
from .util import arcade_int_to_string
import queue
import threading

OFFSET = 320


class Lobby(Base):
    def __init__(self, display):
        self.display = display

        self.spritelist = arcade.SpriteList()
        self.spritedict = dict()
        self.sceneTime = 0
        self.name = ""
        self.cursor_index = -1
        self.focus = None
        self.network_thread = None
        self.receive_queue = None
        self.send_queue = None
        self.other = ""
        self.players = [{}, {}, {}]
        self.sprite_setup()

    def reset(self, network_thread: threading.Thread, receive: queue.Queue, send: queue.Queue) -> None:
        self.sceneTime = 0
        self.network_thread = network_thread
        self.receive_queue = receive
        self.send_queue = send

    def sprite_setup(self):
        self.spritedict = {
            "back": arcade.Sprite(
                "./assets/simple_button.png",
                scale=0.25,
                center_x=160,
                center_y=687.5
            ),
            "name": arcade.Sprite(
                "./assets/simple_button.png",
                scale=0.25,
                center_x=160,
                center_y=622.5
            )
        }
        self.spritelist.extend(list(self.spritedict.values()))

    def update(self, delta_time: float) -> None:
        self.sceneTime += delta_time
        try:
            data = self.receive_queue.get(block=False)
        except queue.Empty:
            pass
        else:
            if data["type"] == "playersUpdate":
                self.players = data["data"]

    def draw(self):
        self.spritelist.draw()
        if len(self.name) < 25:
            buffer = " " * (25 - len(self.name))
        else:
            buffer = ""
        arcade.draw_text(buffer + self.name[-25:], 15, 600, color=(255, 255, 255), font_size=35, width=560)
        for c, player in enumerate(self.players):
            if len(player) == 0:
                continue
            arcade.draw_text(player["name"], OFFSET * (c + 1), 600, color=(0, 0, 100), font_size=35)

    def mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if self.spritedict["back"].collides_with_point((x, y)) is True:
            self.display.change_scenes("mainMenu", startup=False)
        elif self.spritedict["name"].collides_with_point((x, y)) is True:
            self.focus = "name"
        else:
            self.focus = None

    def key_press(self, key, modifiers):
        if self.focus == "name":
            if key == arcade.key.BACKSPACE:
                if self.cursor_index == -1:
                    self.name = self.name[:-1]
                else:
                    self.name = self.name[:self.cursor_index] + self.name[self.cursor_index + 1:]
            elif key == arcade.key.DELETE:
                if self.cursor_index == - (len(self.ip) + 1):
                    self.ip = self.ip[1:]
                else:
                    self.ip = self.ip[:self.cursor_index - 1] + self.ip[self.cursor_index:]
            elif key == arcade.key.LEFT:
                self.cursor_index -= 1
                if self.cursor_index <= - (len(self.name) + 2):
                    self.cursor_index = -1
            elif key == arcade.key.RIGHT:
                self.cursor_index += 1
                if self.cursor_index >= 0:
                    self.cursor_index = - (len(self.name) + 1)
            else:
                key = arcade_int_to_string(key, modifiers)
                if key != "":
                    if self.cursor_index == -1:
                        self.name = self.name + key
                    else:
                        self.name = self.name[:self.cursor_index + 1] + key + self.name[self.cursor_index + 1:]
            self.send_queue.put({"type": "nameChange", "newName": self.name})
