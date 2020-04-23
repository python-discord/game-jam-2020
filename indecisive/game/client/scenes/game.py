import arcade
from indecisive.game.client.scenes.base import Base
import multiprocessing
import queue


COLOURS = [(200, 100, 100), (100, 200, 100), (100, 100, 200)]


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

        # game drawing
        self.shapes: arcade.ShapeElementList = arcade.ShapeElementList()

        # game tracking
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
            self.shapes.draw()

    def update(self, delta_time: float) -> None:
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
        print(self.world)
        self.setup_world()
        self.initialised = True

    def setup_world(self):
        self.shapes = arcade.ShapeElementList()

        dim = self.world["dim"]
        square = 38
        x_buffer = 13
        y_buffer = 151

        self.shapes.append(arcade.create_rectangle_filled(
            x_buffer + square * dim[0]//2,
            y_buffer + square * dim[1]//2,
            square * dim[0],
            square * dim[1],
            (150, 165, 135)
        ))

        for city in self.world["cities"]:
            self.shapes.append(arcade.create_rectangle_filled(
                city["loc"][0] * square + x_buffer + square/2,
                city["loc"][1] * square + y_buffer + square/2,
                square - 2, square - 2,
                COLOURS[city["owner"]]
            ))

        lines = []

        for y_line in range(dim[0] + 1):
            lines.append([y_line * square + x_buffer, y_buffer])
            lines.append([y_line * square + x_buffer, 720 - y_buffer])

        for x_line in range(dim[1] + 1):
            lines.append([x_buffer, x_line * square + y_buffer])
            lines.append([1280 - x_buffer, x_line * square + y_buffer])

        self.shapes.append(arcade.create_lines(lines, color=(0, 0, 0), line_width=1))
