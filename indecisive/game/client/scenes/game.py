import arcade
from indecisive.game.client.scenes.base import Base
import multiprocessing
import queue


COLOURS = [(200, 100, 100), (100, 200, 100), (100, 100, 200)]
CITIES = ["assets/red_city.png", "assets/green_city.png", "assets/blue_city.png"]


class Game(Base):
    def __init__(self, display):
        self.display = display

        self.sceneTime = 0
        self.initialised = False

        self.network_thread = None
        self.receive_queue = None
        self.send_queue = None

        # game drawing
        self.shapes: arcade.ShapeElementList = arcade.ShapeElementList()
        self.city_sprites = arcade.SpriteList()
        self.square = 38
        self.x_buffer = 13
        self.y_buffer = 151

        # game tracking
        self.world = None
        self.players = [dict(), dict(), dict()]
        self.id = None
        self.dim = [0, 0]

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
            self.city_sprites.draw()

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
        self.dim = self.world["dim"]
        self.setup_world()
        self.initialised = True

    def setup_world(self):
        self.shapes = arcade.ShapeElementList()

        self.shapes.append(arcade.create_rectangle_filled(
            self.x_buffer + self.square * self.dim[0]//2,
            self.y_buffer + self.square * self.dim[1]//2,
            self.square * self.dim[0],
            self.square * self.dim[1],
            (150, 165, 135)
        ))

        lines = []

        for y_line in range(self.dim[0] + 1):
            lines.append([y_line * self.square + self.x_buffer, self.y_buffer])
            lines.append([y_line * self.square + self.x_buffer, 720 - self.y_buffer])

        for x_line in range(self.dim[1] + 1):
            lines.append([self.x_buffer, x_line * self.square + self.y_buffer])
            lines.append([1280 - self.x_buffer, x_line * self.square + self.y_buffer])

        self.shapes.append(arcade.create_lines(lines, color=(0, 0, 0), line_width=1))

        for city in self.world["cities"]:
            self.create_city(city)

    def create_city(self, city):
        self.city_sprites.append(arcade.Sprite(
            CITIES[city["owner"]],
            center_x=city["loc"][0] * self.square + self.x_buffer + self.square/2,
            center_y=city["loc"][1] * self.square + self.y_buffer + self.square/2,
        ))
