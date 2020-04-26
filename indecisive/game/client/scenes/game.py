import arcade
from indecisive.game.client.scenes.base import Base
import multiprocessing
import queue
import json


COLOURS = [(200, 100, 100), (100, 200, 100), (100, 100, 200)]
CITIES = ["assets/red_city.png", "assets/green_city.png", "assets/blue_city.png"]
ICONS = ["assets/red_icon.png", "assets/green_icon.png", "assets/blue_icon.png"]


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
        self.y_buffer_top = 70
        self.y_buffer_bottom = 231

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
        self.city2_ui = [arcade.SpriteList(), []]
        self.city3_ui = [arcade.SpriteList(), []]
        self.city4_ui = [arcade.SpriteList(), []]
        self.city5_ui = [arcade.SpriteList(), []]
        self.dcity_ui = [arcade.SpriteList(), []]
        self.dcity2_ui = [arcade.SpriteList(), []]
        self.dcity3_ui = [arcade.SpriteList(), []]
        self.dcity4_ui = [arcade.SpriteList(), []]
        self.dcity5_ui = [arcade.SpriteList(), []]
        self.unit_ui = [arcade.SpriteList(), []]
        self.settler_ui = [arcade.SpriteList(), []]
        self.empty_ui = [arcade.SpriteList(), []]
        self.selectors = [arcade.SpriteList(), [lambda: None, lambda: None, lambda: None, lambda: None]]
        self.current_ui = [arcade.SpriteList(), []]

        self.top_ui = [arcade.SpriteList(), [], dict()]  # list of sprite, list of text kwargs, dict of text indexes

        self.victory_screen = [arcade.SpriteList(), []]
        self.victory_ui = [arcade.SpriteList(), []]

        self.end = True

        with open("data/units.json") as file:
            self.unit_types = json.load(file)

        with open("data/cities.json") as file:
            self.city_types = json.load(file)

    def reset(self, network_thread: multiprocessing.Process, receive: multiprocessing.Queue, send: multiprocessing.Queue, players, player_id) \
            -> None:
        print("Game view!")
        self.player_id = player_id
        self.players = players
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
            self.top_ui[0].draw()
            for text in self.top_ui[1]:
                arcade.draw_text(**text)
            self.victory_screen[0].draw()
            for text in self.victory_screen[1]:
                arcade.draw_text(**text)
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
                elif data["type"] == "moveUnit":
                    self.server_move_unit(data["data"])
                elif data["type"] == "killUnit":
                    self.server_kill_unit(data["data"])
                elif data["type"] == "killCity":
                    self.server_kill_city(data["data"])
                elif data["type"] == "upgradeCity":
                    self.server_upgrade_city(data["data"])
                elif data["type"] == "createCity":
                    self.server_create_city(data["data"])
                elif data["type"] == "turn":
                    self.turn = data["data"]
                    self.top_ui[1][self.top_ui[2]["currentTurn"]]["text"] = f"Current turn: {self.players[self.turn]['name']}"
                elif data["type"] == "victory":
                    self.victory(data["data"])
                elif data["type"] == "updateCityHealth":
                    self.server_repair_city(data["data"])
                else:
                    print(f"SCREAMS IN BRAILLE: {data}")

    def victory(self, winner):
        self.display.change_scenes("victory", self.players[winner]['name'])
        for process in self.display.processes:
            process.terminate()
        self.display.processes.clear()

    # INITIAL DOWNLOAD
    def initialise(self):
        ready = [False, False]
        while not all(ready):
            data = self.receive_queue.get()
            if data["type"] == "world":
                self.world = data["data"]
                ready[0] = True
            if data["type"] == "turn":
                self.turn = data["data"]
                ready[1] = True
            else:
                self.receive_queue.put(data)
        self.dim = self.world["dim"]
        self.setup_world()
        self.setup_ui()
        self.top_ui[1][self.top_ui[2]["currentTurn"]]["text"] = f"Current turn: {self.players[self.turn]['name']}"
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
            self.city_types["icons"][city["level"]][city["owner"]],
            center_x=city["loc"][0] * self.square + self.x_buffer + self.square/2,
            center_y=city["loc"][1] * self.square + self.y_buffer_bottom + self.square/2
        ))

    def _create_unit(self, unit):
        self.unit_sprites.append(arcade.Sprite(
            self.unit_types[unit["type"]]["icons"][unit["owner"]],
            center_x=unit["loc"][0] * self.square + self.x_buffer + self.square / 2,
            center_y=unit["loc"][1] * self.square + self.y_buffer_bottom + self.square / 2
        ))

    def server_create_city(self, city):
        self.world["cities"].append(city)
        self._create_city(city)
        self.selected = ["cities", len(self.world["cities"]) - 1]
        self.update_ui()

    def client_create_city(self, city):
        self.send_queue.put({"type": "turnFinal", "actionType": "createCity", "data": city})

    def server_create_unit(self, unit):
        self.world["units"].append(unit)
        self._create_unit(unit)

    def client_create_unit(self, unit):
        self.send_queue.put({"type": "turnFinal", "actionType": "createUnit", "data": unit})

    def client_move_unit(self, data):
        self.send_queue.put({"type": "turnFinal", "actionType": "moveUnit", "data": data})

    def server_move_unit(self, data):
        self.world["units"][data["unit_id"]]["loc"] = data["loc"]
        self.unit_sprites[data["unit_id"]].position = self.get_xy_centre(data["loc"])

    def server_kill_unit(self, unit_id):
        self.unit_sprites[unit_id].position = self.get_xy_centre((-100, 1000))
        self.world["units"][unit_id] = None
        if self.selected == ["units", unit_id]:
            self.selected = [None, None]
            self.update_ui()

    def server_kill_city(self, city_id):
        self.city_sprites[city_id].position = self.get_xy_centre((-100, 1000))
        self.world["cities"][city_id] = None
        if self.selected == ["cities", city_id]:
            self.selected = [None, None]
            self.update_ui()

    def client_attack_unit(self, data):
        self.send_queue.put({"type": "turnFinal", "actionType": "attackUnit", "data": data})

    def client_attack_city(self, data):
        self.send_queue.put({"type": "turnFinal", "actionType": "attackCity", "data": data})

    def server_upgrade_city(self, data):
        city = self.world["cities"][data["city_id"]]
        city["level"] += 1
        self.city_sprites[data["city_id"]].texture = arcade.load_texture(self.city_types["icons"][city["level"]][city["owner"]])
        self.update_ui()

    def client_upgrade_city(self, data):
        self.send_queue.put({"type": "turnFinal", "actionType": "upgradeCity", "data": data})

    def client_settle_city(self, unit_id):
        self.send_queue.put({"type": "turnFinal", "actionType": "settleCity", "data": unit_id})

    def server_repair_city(self, data):
        city = self.world["cities"][data["city_id"]]
        city["health"] = data["health"]
        if self.selected == ["cities", data["city_id"]]:
            self.update_ui()

    def client_repair_city(self, city_id):
        self.send_queue.put({"type": "turnFinal", "actionType": "repairCity", "data": city_id})

    def setup_ui(self):
        # MAIN UI
        self.ui_background = arcade.create_rectangle_filled(640, 95, 1280, 190, color=(150, 150, 150))

        create_basic = arcade.Sprite(
            "assets/create_unit_button.png",
            scale=0.25,
            center_x=200,
            center_y=50
        )
        create_heavy = arcade.Sprite(
            "assets/create_heavy_button.png",
            scale=0.25,
            center_x=600,
            center_y=50
        )
        create_shield = arcade.Sprite(
            "assets/create_shield_button.png",
            scale=0.25,
            center_x=600,
            center_y=100
        )
        create_settler = arcade.Sprite(
            "assets/create_settler_button.png",
            scale=0.25,
            center_x=600,
            center_y=150
        )
        move_unit = arcade.Sprite(
            "assets/move_button.png",
            scale=0.25,
            center_x=200,
            center_y=50
        )
        attack_unit = arcade.Sprite(
            "assets/attack_unit_button.png",
            scale=0.25,
            center_x=200,
            center_y=100
        )
        settle_city = arcade.Sprite(
            "assets/create_city_button.png",
            scale=0.25,
            center_x=200,
            center_y=100
        )
        attack_city = arcade.Sprite(
            "assets/attack_city_button.png",
            scale=0.25,
            center_x=200,
            center_y=150
        )
        upgrade_city = arcade.Sprite(
            "assets/upgrade_city_button.png",
            scale=0.25,
            center_x=200,
            center_y=100
        )
        repair_city = arcade.Sprite(
            "assets/upgrade_city_button.png",
            scale=0.25,
            center_x=200,
            center_y=150
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
        self.city_ui[0].extend([create_basic, upgrade_city])
        self.city_ui[1] = [self.create_basic, self.upgrade_city]
        self.city2_ui[0].extend([create_basic, upgrade_city, create_shield])
        self.city2_ui[1] = [self.create_basic, self.upgrade_city, self.create_shield]
        self.city3_ui[0].extend([create_basic, upgrade_city, create_shield, create_heavy])
        self.city3_ui[1] = [self.create_basic, self.upgrade_city, self.create_shield, self.create_heavy]
        self.city4_ui[0].extend([create_basic, upgrade_city, create_shield, create_heavy, create_settler])
        self.city4_ui[1] = [self.create_basic, self.upgrade_city, self.create_shield, self.create_heavy, self.create_settler]
        self.city5_ui[0].extend([create_basic, create_shield, create_heavy, create_settler])
        self.city5_ui[1] = [self.create_basic, self.create_shield, self.create_heavy, self.create_settler]
        self.dcity_ui[0].extend([create_basic, repair_city])
        self.dcity_ui[1] = [self.create_basic, self.repair_city]
        self.dcity2_ui[0].extend([create_basic, repair_city, create_shield])
        self.dcity2_ui[1] = [self.create_basic, self.repair_city, self.create_shield]
        self.dcity3_ui[0].extend([create_basic, repair_city, create_shield, create_heavy])
        self.dcity3_ui[1] = [self.create_basic, self.repair_city, self.create_shield, self.create_heavy]
        self.dcity4_ui[0].extend([create_basic, repair_city, create_shield, create_heavy, create_settler])
        self.dcity4_ui[1] = [self.create_basic, self.repair_city, self.create_shield, self.create_heavy, self.create_settler]
        self.dcity5_ui[0].extend([create_basic, repair_city, create_shield, create_heavy, create_settler])
        self.dcity5_ui[1] = [self.create_basic, self.repair_city, self.create_shield, self.create_heavy, self.create_settler]

        # unit UI
        self.unit_ui[0].extend([move_unit, attack_unit, attack_city])
        self.unit_ui[1].extend([self.move_unit, self.attack_unit, self.attack_city])

        # settler UI
        self.settler_ui[0].extend([move_unit, settle_city])
        self.settler_ui[1].extend([self.move_unit, self.settle_city])

        # TOP BAR UI
        player_icon = arcade.Sprite(
            ICONS[self.player_id],
            scale=1.3157,
            center_x=25,
            center_y=695
        )
        self.top_ui[0].append(player_icon)
        self.top_ui[1].append({
            "text": self.players[self.player_id]["name"],
            "start_x": 70, "start_y": 675,
            "color": (0, 0, 0),
            "font_size": 30
        })
        self.top_ui[1].append({
            "text": "",
            "start_x": 800, "start_y": 675,
            "color": (0, 0, 0),
            "font_size": 30
        })
        self.top_ui[1].append({
            "text": "",
            "start_x": 800, "start_y": 10,
            "color": (0, 0, 0),
            "font_size": 20
        })
        self.top_ui[2] = {
            "name": 0,
            "currentTurn": 1,
            "infoBox": 2
        }
    # UI

    def mouse_release(self, x: float, y: float, button: int, modifiers: int) -> None:
        for selector_number in range(4):
            if self.selectors[0][selector_number].collides_with_point((x, y)) is True:
                self.selectors[1][selector_number]()
                return
        selected = self.map_sprite_clicked(x, y)
        if selected is False:
            for ui_num, ui in enumerate(self.current_ui[0]):
                if ui.collides_with_point((x, y)) is True:
                    self.current_ui[1][ui_num](self.world[self.selected[0]][self.selected[1]], self.selected[1])
                    return

            # did not click something new so end statement and hence no need to update ui
            selected = [None, None]
        self.selected = selected
        self.update_ui()

    def create_basic(self, city, city_id):
        action_maker = self.action_maker_maker(self.client_create_unit, {"owner": self.player_id, "type": "basic"})
        self.move_selectors_all_block(city["loc"], action_maker)

    def create_shield(self, city, city_id):
        action_maker = self.action_maker_maker(self.client_create_unit, {"owner": self.player_id, "type": "shield"})
        self.move_selectors_all_block(city["loc"], action_maker)

    def create_heavy(self, city, city_id):
        action_maker = self.action_maker_maker(self.client_create_unit, {"owner": self.player_id, "type": "heavy"})
        self.move_selectors_all_block(city["loc"], action_maker)

    def create_settler(self, city, city_id):
        action_maker = self.action_maker_maker(self.client_create_unit, {"owner": self.player_id, "type": "settler"})
        self.move_selectors_all_block(city["loc"], action_maker)

    def move_unit(self, unit, unit_id):
        action_maker = self.action_maker_maker(self.client_move_unit, {"unit_id": unit_id, "loc": [0, 0]})
        self.move_selectors_all_block(unit["loc"], action_maker)

    def attack_unit(self, unit, unit_id):
        action_maker = self.action_maker_maker(self.client_attack_unit, {"unit_id": unit_id, "loc": [0, 0]})
        self.move_selectors_units_only(unit["loc"], action_maker)

    def attack_city(self, unit, unit_id):
        action_maker = self.action_maker_maker(self.client_attack_city, {"unit_id": unit_id, "loc": [0, 0]})
        self.move_selectors_cites_only(unit["loc"], action_maker)

    def upgrade_city(self, city, city_id):
        self.client_upgrade_city({"city_id": city_id})

    def settle_city(self, unit, unit_id):
        self.client_settle_city(unit_id)

    def repair_city(self, city, city_id):
        self.client_repair_city(city_id)

    def action_maker_maker(self, action, arg: dict, hide_ui=True):
        def _action_maker(**kwargs):
            def _action():

                obj = {**arg, **kwargs}
                action(obj)
                if hide_ui is True:
                    self.hide_selectors()

            return _action
        return _action_maker

    def update_ui(self):
        if self.selected[0] == "cities" and self.world["cities"][self.selected[1]]["owner"] == self.player_id:
            city = self.world["cities"][self.selected[1]]
            level = city["level"]
            if city["max_health"] == city["health"]:
                if level == 0:
                    self.current_ui = self.city_ui
                elif level == 1:
                    self.current_ui = self.city2_ui
                elif level == 2:
                    self.current_ui = self.city3_ui
                elif level == 3:
                    self.current_ui = self.city4_ui
                elif level == 4:
                    self.current_ui = self.city5_ui
            else:
                print("damaged")
                if level == 0:
                    self.current_ui = self.dcity_ui
                elif level == 1:
                    self.current_ui = self.dcity2_ui
                elif level == 2:
                    self.current_ui = self.dcity3_ui
                elif level == 3:
                    self.current_ui = self.dcity4_ui
                elif level == 4:
                    self.current_ui = self.dcity5_ui
        elif self.selected[0] == "units" and self.world["units"][self.selected[1]]["owner"] == self.player_id:
            if self.world["units"][self.selected[1]]["type"] == "settler":
                self.current_ui = self.settler_ui
            else:
                self.current_ui = self.unit_ui
        else:
            self.current_ui = self.empty_ui

        # info box
        if self.selected != [None, None]:
            if self.selected[0] == "cities":
                health = self.world['cities'][self.selected[1]]['health']
                max_health = self.world['cities'][self.selected[1]]['max_health']
                owner = self.players[self.world['cities'][self.selected[1]]['owner']]["name"]
                level = self.world['cities'][self.selected[1]]['level'] + 1
                self.top_ui[1][self.top_ui[2]["infoBox"]]["text"] = f"City\n" \
                                                                    f"Owner: {owner}\n" \
                                                                    f"Defense: {health}\n" \
                                                                    f"Level: {level}\n" \
                                                                    f"Max Defense {max_health}\n\n\n"
            elif self.selected[0] == "units":
                owner = self.players[self.world['units'][self.selected[1]]['owner']]["name"]
                defence = self.unit_types[self.world['units'][self.selected[1]]["type"]]['base_defense']
                attack = self.unit_types[self.world['units'][self.selected[1]]["type"]]['base_attack']
                type = self.unit_types[self.world['units'][self.selected[1]]["type"]]['name']
                self.top_ui[1][self.top_ui[2]["infoBox"]]["text"] = f"Unit\n" \
                                                                    f"Owner: {owner}\n" \
                                                                    f"Type: {type}\n" \
                                                                    f"Attack: {attack}\n" \
                                                                    f"Defence {defence}\n\n\n"

        else:
            self.top_ui[1][self.top_ui[2]["infoBox"]]["text"] = ""

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
            if self.is_xy_occupied(new_pos) is False:
                self.set_xy_centre(self.selectors[0][selector_number], new_pos)
                self.selectors[1][selector_number] = action_maker(loc=new_pos)

    def move_selectors_units_only(self, pos, action_maker):
        for selector_number in range(4):
            new_pos = self._selectors_new_position(pos, selector_number)
            tile = self.is_xy_occupied(new_pos)
            if tile is not False and tile[0] == "units":
                self.set_xy_centre(self.selectors[0][selector_number], new_pos)
                self.selectors[1][selector_number] = action_maker(loc=new_pos, attack=tile[1])

    def move_selectors_cites_only(self, pos, action_maker):
        for selector_number in range(4):
            try:
                new_pos = self._selectors_new_position(pos, selector_number)
            except IndexError:
                continue
            tile = self.is_xy_occupied(new_pos)
            if tile is not False and tile[0] == "cities":
                self.set_xy_centre(self.selectors[0][selector_number], new_pos)
                self.selectors[1][selector_number] = action_maker(loc=new_pos, attack=tile[1])

    def _selectors_new_position(self, pos, index):
        new_pos = pos.copy()
        if index == 0:
            new_pos[0] += 1
            if new_pos[0] >= self.world["dim"][0]:
                new_pos[0] = 0
        elif index == 1:
            new_pos[1] -= 1
            if new_pos[1] < 0:
                new_pos[1] = self.world["dim"][1] - 1
        elif index == 2:
            new_pos[0] -= 1
            if new_pos[0] < 0:
                new_pos[0] = self.world["dim"][0] - 1
        elif index == 3:
            new_pos[1] += 1
            if new_pos[1] >= self.world["dim"][1]:
                new_pos[1] = 0
        else:
            raise IndexError(f"There are only four Cardinal directions (0-3) yet {index} was given")
        return new_pos

    def map_sprite_clicked(self, x, y):
        for unit_num, unit in enumerate(self.unit_sprites):
            if unit.collides_with_point((x, y)) is True:
                return ["units", unit_num]
        else:
            for city_num, city in enumerate(self.city_sprites):
                if city.collides_with_point((x, y)):
                    return ["cities", city_num]
            else:
                return False

    def is_xy_occupied(self, pos):
        for unit_num, unit in enumerate(self.world["units"]):
            if unit is None:
                continue
            if unit["loc"] == pos:
                return ["units", unit_num]
        else:
            for city_num, city in enumerate(self.world["cities"]):
                if city is None:
                    continue
                if city["loc"] == pos:
                    return ["cities", city_num]
            else:
                return False
