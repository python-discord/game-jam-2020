import arcade
from indecisive.game.client.scenes.base import Base
import multiprocessing
import queue


class Game(Base):
    def __init__(self, display):
        self.display = display

        self.spritelist = arcade.SpriteList()
        self.spritedict = dict()
        self.sceneTime = 0
        self.initialised = False

        self.network_thread = None
        self.receive_queue = None
        self.send_queue = None

        self.world = None
        self.players = [dict(), dict(), dict()]
        self.id = None

    def reset(self, network_thread: multiprocessing.Process, receive: multiprocessing.Queue, send: multiprocessing.Queue, id) -> None:
        print("Game view!")
        self.id = id
        self.network_thread = network_thread
        self.receive_queue = receive
        self.send_queue = send

        self.sceneTime = 0
        self.initialised = False
        arcade.set_background_color((250, 100, 100))

        self.world = None

    def draw(self) -> None:
        if self.initialised is True:
            for x, row in enumerate(self.world):
                for y, data in enumerate(row):
                    arcade.draw_rectangle_filled((x + 5) * 10, (y + 5) * 10, 10, 10, (0, 0, 0) if data["truefalse"] is False else (255, 255, 255))

    def update(self, delta_time: float) -> None:
        print(delta_time)
        self.sceneTime += delta_time
        if self.initialised is False:
            self.initialise()
        else:
            try:
                data = self.receive_queue.get(block=False)
            except queue.Empty:
                pass
            else:
                if data["type"] == "world":
                    self.world = data["data"]
                elif data["type"] == "playersUpdate":
                    self.players = data["data"]

    def initialise(self):
        ready = [False]
        while not all(ready):
            data = self.receive_queue.get()
            if data["type"] == "world":
                self.world = data["data"]
                ready[0] = True
            else:
                self.receive_queue.put(data)
        self.initialised = True
