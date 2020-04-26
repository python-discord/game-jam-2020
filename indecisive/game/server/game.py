import multiprocessing
import json
import random


class Game:
    def __init__(self, receive_queue: multiprocessing.Queue, send_queue: multiprocessing.Queue):
        self.receive_queue = receive_queue
        self.send_queue = send_queue
        self.players = [{}, {}, {}]
        self.world = None
        self.turn = 0
        with open("data/units.json") as file:
            self.unit_types = json.load(file)
        with open("data/cities.json") as file:
            self.city_types = json.load(file)

        self.lost = None

    def start(self):
        starting = True
        while starting:
            data = self.receive_queue.get()
            if data["type"] == "newConnection":
                self.players[data["connection"]] = {"connected": True, "name": ""}
                self.send_queue.put({"type": "playersUpdate", "data": self.players})
            elif data["type"] == "nameChange":
                self.players[data["connection"]]["name"] = data["newName"][:12]
                self.send_queue.put({"type": "playersUpdate", "data": self.players})
            elif data["type"] == "startGame" and data["connection"] == 0:
                self.send_queue.put({"type": "startGame"})
                break
        self.generate_map()
        self.send_queue.put({"type": "world", "data": self.world})
        self.send_queue.put({"type": "turn", "data": self.turn})
        while True:
            # main game loop
            data = self.receive_queue.get()
            if data["type"] == "turnFinal" and data["connection"] == self.turn:
                if data["actionType"] == "moveUnit":
                    self.send_queue.put({"type": "moveUnit", "data": data["data"]})
                    self.world["units"][data["data"]["unit_id"]]["loc"] = data["data"]["loc"]
                elif data["actionType"] == "createUnit":
                    self.send_queue.put({"type": "newUnit", "data": data["data"]})
                    self.world["units"].append(data["data"])
                elif data["actionType"] == "attackUnit":
                    self.attack_unit(data["data"])
                elif data["actionType"] == "attackCity":
                    self.attack_city(data["data"])
                elif data["actionType"] == "upgradeCity":
                    self.upgrade_city(data["data"])
                elif data["actionType"] == "settleCity":
                    self.create_city(data["data"])
                elif data["actionType"] == "repairCity":
                    self.repair_city(data["data"])

                self.next_turn()

    def repair_city(self, city_id):
        city = self.world["cities"][city_id]
        city["health"] += 50
        if city["max_health"] < city["health"]:
            city["health"] = city["max_health"]
        self.send_queue.put({"type": "updateCityHealth", "data": {"city_id": city_id, "health": city["health"]}})

    def next_turn(self):
        self.turn += 1
        if self.lost is not None and self.turn == self.lost:
            self.turn += 1
        if self.turn >= len(self.players):
            self.turn = 0
        self.send_queue.put({"type": "turn", "data": self.turn})
        self.check_victory()

    def generate_map(self, x=33, y=11):
        world = {
            "cities": [],
            "units": [],
            "dim": [x, y]
        }
        for i in range(3):
            # noinspection PyTypeChecker
            world["cities"].append({
                "loc": [i * 11 + 5, 5],
                "level": 0,
                "owner": i,
                "health": self.city_types["health"][0],
                "max_health": self.city_types["health"][0]
            })

        self.world = world

    def create_city(self, unit_id):
        unit = self.world["units"][unit_id]
        city = {
            "loc": unit["loc"],
            "owner": unit["owner"],
            "level": 0,
            "health": self.city_types["health"][0],
            "max_health": self.city_types["health"][0]
        }
        self.world["cities"].append(city)
        self.send_queue.put({"type": "createCity", "data": city})
        self.send_queue.put({"type": "killUnit", "data": unit_id})

    def attack_unit(self, data):
        defending = self.world["units"][data["attack"]]
        attacking = self.world["units"][data["unit_id"]]
        attack = random.randint(1, 101) + self.unit_types[attacking["type"]]["base_attack"]
        defend = random.randint(1, 101) + self.unit_types[defending["type"]]["base_defense"]
        if attack >= defend:
            self.send_queue.put({"type": "killUnit", "data": data["attack"]})
            self.world["units"][data["attack"]] = None
            self.send_queue.put({"type": "moveUnit", "data": data})
        else:
            print("Attack failed")

    def attack_city(self, data):
        print(self.world["units"])
        attacking = self.world["units"][data["unit_id"]]
        defending = self.world["cities"][data["attack"]]
        attack = random.randint(1, 101) + self.unit_types[attacking["type"]]["base_attack"]
        defending["health"] -= attack
        self.send_queue.put({"type": "updateCityHealth", "data": {"city_id": data["attack"], "health": defending["health"]}})
        print(defending["health"])
        if defending["health"] <= 0:
            self.send_queue.put({"type": "killCity", "data": data["attack"]})
            self.send_queue.put({"type": "moveUnit", "data": data})
            self.world["cities"][data["attack"]] = None
        else:
            print("Attack failed")

    def upgrade_city(self, data):
        city = self.world["cities"][data["city_id"]]
        city["level"] += 1
        city["max_health"] = self.city_types["health"][city["level"]]
        health = city["health"]/city["max_health"]
        city["health"] = health * city["max_health"]
        self.send_queue.put({"type": "upgradeCity", "data": data})

    def check_victory(self):
        lost = [True, True, True]
        for city in self.world["cities"]:
            if city is None:
                continue
            else:
                lost[city["owner"]] = False
        print(lost)
        if sum(lost) == 2:
            self.send_queue.put({"type": "victory", "data": lost.index(False)})
        elif sum(lost) == 1:
            self.lost = lost.index(True)


def run(receive: multiprocessing.Queue, send: multiprocessing.Queue):
    game = Game(receive, send)
    game.start()
