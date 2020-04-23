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

    def start(self):
        starting = True
        while starting:
            data = self.receive_queue.get()
            print(data)
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
        while True:
            # main game loop
            data = self.receive_queue.get()
            if data["type"] == "turnFinal" and data["connection"] == self.turn:
                if data["actionType"] == "moveUnit":
                    pass
                elif data["actionType"] == "createUnit":
                    self.send_queue.put({"type": "newUnit", "data": data["data"]})
                self.next_turn()

    def next_turn(self):
        self.turn += 1
        if self.turn >= len(self.players):
            self.turn = 0
        self.send_queue.put({"type": "turn", "data": self.turn})

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
                "owner": i
            })

        self.world = world


def run(receive: multiprocessing.Queue, send: multiprocessing.Queue):
    game = Game(receive, send)
    game.start()
