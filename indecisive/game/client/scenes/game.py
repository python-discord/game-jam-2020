import arcade
from indecisive.game.client.scenes.base import Base
import multiprocessing
import queue
import json


COLOURS = [(200, 100, 100), (100, 200, 100), (100, 100, 200)]
CITIES = ["assets/red_city.png", "assets/green_city.png", "assets/blue_city.png"]


class Game(Base):
    # noinspection PyTypeChecker
    def __init__(self, display):
        self.display = display

        self.sceneTime = 0
        self.initialised = False

        self.network_thread = None
        self.receive_queue: multiprocessing.Queue = None
        self.send_queue: multiprocessing.Queue = None

        # game drawing
        self.background = None
        self.grid = None
        self.city_sprites = arcade.SpriteList()
        self.unit_sprites = arcade.SpriteList()
        self.square = 38
        self.x_buffer = 13
        self.y_buffer_top = 50
        self.y_buffer_bottom = 251

        # game tracking
        self.turn = 0
        self.world = None
        self.players = [dict(), dict(), dict()]
        self.player_id = None
        self.dim = [0, 0]

        # ui
        self.selected = [None, None]
        self.ui_background = None
        self.city_ui = [arcade.SpriteList(), []]
        self.current_ui = [arcade.SpriteList(), []]
        self.empty_ui = [arcade.SpriteList(), []]
        self.selectors = [arcade.SpriteList(), [lambda: None, lambda: None, lambda: None, lambda: None]]
        self.setup_ui()

        with open("data/units.json") as file:
            self.unit_types = json.load(file)

    def reset(self, network_thread: multiprocessing.Process, receive: multiprocessing.Queue, send: multiprocessing.Queue, player_id) \
            -> None:
        print("Game view!")
        self.player_id = player_id
        self.network_thread = network_thread
        self.receive_queue = receive
        self.send_queue = send

        self.sceneTime = 0
        self.initialised = False

        self.unit_sprites = arcade.SpriteList()
        self.city_sprites = arcade.SpriteList()

    def draw(self) -> None:
        if self.initialised is True:
            self.background.draw()
            self.city_sprites.draw()
            self.unit_sprites.draw()
            self.selectors[0].draw()
            self.grid.draw()

            self.ui_background.draw()
            self.current_ui[0].draw()

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
                elif data["type"] == "newCity":
                    self.server_create_city(data["data"])
                elif data["type"] == "newUnit":
                    self.server_create_unit(data["data"])
                elif data["type"] == "turn":
                    self.turn = data["data"]
                else:
                    print(f"SCREAMS IN BRAILLE: {data}")

    # INITIAL DOWNLOAD
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

    # WORLD
    def setup_world(self):

        self.background = arcade.create_rectangle_filled(
            self.x_buffer + self.square * self.dim[0]//2,
            self.y_buffer_bottom + self.square * self.dim[1]//2,
            self.square * self.dim[0],
            self.square * self.dim[1],
            (150, 165, 135)
        )

        lines = []

        for y_line in range(self.dim[0] + 1):
            lines.append([y_line * self.square + self.x_buffer, self.y_buffer_bottom])
            lines.append([y_line * self.square + self.x_buffer, 720 - self.y_buffer_top])

        for x_line in range(self.dim[1] + 1):
            lines.append([self.x_buffer, x_line * self.square + self.y_buffer_bottom])
            lines.append([1280 - self.x_buffer, x_line * self.square + self.y_buffer_bottom])

        self.grid = arcade.create_lines(lines, color=(0, 0, 0), line_width=1)

        for city in self.world["cities"]:
            self._create_city(city)

        self.setup_ui()

    def _create_city(self, city):
        self.city_sprites.append(arcade.Sprite(
            CITIES[city["owner"]],
            center_x=city["loc"][0] * self.square + self.x_buffer + self.square/2,
            center_y=city["loc"][1] * self.square + self.y_buffer_bottom + self.square/2
        ))

    def _create_unit(self, unit):
        self.unit_sprites.append(arcade.Sprite(
            self.unit_types[unit["type"]]["icons"][unit["owner"]],
            center_x=unit["loc"][0] * self.square + self.x_buffer + self.square / 2,
            center_y=unit["loc"][1] * self.square + self.y_buffer_bottom + self.square / 2
        ))

    def client_create_city(self, city):
        self.send_queue.put({"type": "turnFinal", "actionType": "createCity", "data": city})

    def server_create_city(self, city):
        self.world["cities"].append(city)
        self._create_city(city)

    def server_create_unit(self, unit):
        self.world["units"].append(unit)
        self._create_unit(unit)

    def client_create_unit(self, unit):
        self.send_queue.put({"type": "turnFinal", "actionType": "createUnit", "data": unit})

    # UI
    def setup_ui(self):
        self.ui_background = arcade.create_rectangle_filled(640, 95, 1280, 190, color=(150, 150, 150))

        create_unit = arcade.Sprite(
            "assets/create_unit_button.png",
            scale=0.25,
            center_x=200,
            center_y=50
        )
        # selectors
        for selector_number in range(4):
            self.selectors[0].append(arcade.Sprite(
                "assets/selector.png",
                center_x=-100,
                center_y=-100
            ))
            self.selectors[1][selector_number] = lambda: None
        # city UI
        self.city_ui[0].append(create_unit)
        self.city_ui[1] = [self.create_unit]

    def mouse_release(self, x: float, y: float, button: int, modifiers: int) -> None:
        selected = self.is_xy_occupied(x, y)
        if selected is False:
            for ui_num, ui in enumerate(self.current_ui[0]):
                if ui.collides_with_point((x, y)) is True:
                    self.current_ui[1][ui_num](self.world[self.selected[0]][self.selected[1]])
                    return

            for selector_number in range(4):
                if self.selectors[0][selector_number].collides_with_point((x, y)) is True:
                    self.selectors[1][selector_number]()
                    return

            # did not click something new so end statement and hence no need to update ui
            selected = [None, None]
        self.selected = selected
        self.update_ui()

    def create_unit(self, city):
        action_maker = self.action_maker(self.client_create_unit, {"owner": self.player_id, "type": "basic"})
        self.move_selectors_all_block(city["loc"], action_maker)

    @staticmethod
    def action_maker(action, arg: dict):

        def _action_maker(**kwargs):
            arg.update(kwargs)

            def _action():
                action(arg)
            return _action

        return _action_maker

    def update_ui(self):
        if self.selected[0] == "cities" and self.world["cities"][self.selected[1]]["owner"] == self.player_id:
            self.current_ui = self.city_ui
            self.hide_selectors()
        else:
            self.current_ui = self.empty_ui
            self.hide_selectors()

    def hide_selectors(self):
        for selector_number in range(4):
            self.selectors[0][selector_number].center_y = -1000
            self.selectors[1][selector_number] = lambda: None

    def get_xy_centre(self, pos):
        return (
            pos[0] * self.square + self.x_buffer + self.square / 2,
            pos[1] * self.square + self.y_buffer_bottom + self.square / 2
        )

    def set_xy_centre(self, sprite, pos):
        centre = self.get_xy_centre(pos)
        sprite.center_x = centre[0]
        sprite.center_y = centre[1]

    def move_selectors_all_block(self, pos, action_maker):
        for selector_number in range(4):
            new_pos = self._selectors_new_position(pos, selector_number)
            if self.is_xy_occupied(*new_pos) is False:
                self.set_xy_centre(self.selectors[0][selector_number], new_pos)
                self.selectors[1][selector_number] = action_maker(loc=new_pos)

    @staticmethod
    def _selectors_new_position(pos, index):
        pos = pos.copy()
        if index == 0:
            pos[0] += 1
        elif index == 1:
            pos[1] -= 1
        elif index == 2:
            pos[0] -= 1
        elif index == 3:
            pos[1] += 1
        else:
            raise IndexError(f"There are only four Cardinal directions (0-3) yet {index} was given")
        return pos

    def is_xy_occupied(self, x, y):
        for unit_num, unit in enumerate(self.unit_sprites):
            if unit.collides_with_point((x, y)) is True:
                return ["units", unit_num]
        else:
            for city_num, city in enumerate(self.city_sprites):
                if city.collides_with_point((x, y)):
                    return ["cities", city_num]
            else:
                return False
