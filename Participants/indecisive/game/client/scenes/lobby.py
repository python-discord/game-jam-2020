import json

import arcade
from .base import Base
from .util import arcade_int_to_string
import queue
import multiprocessing

OFFSET = 320
COLOURS = [(200, 100, 100), (100, 200, 100), (100, 100, 200)]


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
        self.players = [{}, {}, {}]
        self.host = False
        self.player_id = None

        self.sprite_setup()

    def reset(self, network_thread: multiprocessing.Process, receive: multiprocessing.Queue, send: multiprocessing.Queue, player_id, host=False) -> None:
        self.network_thread = network_thread
        self.receive_queue = receive
        self.send_queue = send
        self.host = host

        self.sceneTime = 0
        self.name = ""
        self.cursor_index = -1
        self.focus = None
        self.player_id = player_id
        self.players = [{}, {}, {}]

        if self.host is True:
            self.spritedict["start"] = arcade.Sprite(
                "./assets/start_button.png",
                scale=0.25,
                center_x=160,
                center_y=557.5
            )
            self.spritelist.append(self.spritedict["start"])
        else:
            try:
                self.spritedict.pop("start")
            except KeyError:
                pass


    def sprite_setup(self):
        self.spritedict = {
            "back": arcade.Sprite(
                "./assets/back_button.png",
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
            elif data["type"] == "startGame":
                self.start_game()

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
            arcade.draw_text(player["name"], OFFSET * (c + 1), 640, color=(0, 0, 100), font_size=25)
            arcade.draw_rectangle_filled(OFFSET * (c + 1.5), 700, 320, 40, COLOURS[c])

    def mouse_release(self, x: float, y: float, button: int, modifiers: int):
        print(self.host)
        if self.spritedict["back"].collides_with_point((x, y)) is True:
            self.display.change_scenes("mainMenu")
        elif self.spritedict["name"].collides_with_point((x, y)) is True:
            self.focus = "name"
        elif self.host is True and self.spritedict["start"].collides_with_point((x, y)) is True:
            print("starting game")
            self.send_queue.put({"type": "startGame"})
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
                if self.cursor_index == - (len(self.name) + 1):
                    self.name = self.name[1:]
                    self.cursor_index += 1
                elif self.cursor_index < -2:
                    self.name = self.name[:self.cursor_index + 1] + self.name[self.cursor_index + 2:]
                    self.cursor_index += 1
                elif self.cursor_index == -2:
                    self.name = self.name[:-1]
                    self.cursor_index += 1
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

    def start_game(self):
        self.display.change_scenes("game", self.network_thread, self.receive_queue, self.send_queue, self.players, self.player_id)
