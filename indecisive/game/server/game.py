import multiprocessing
import json
import random


class Game:
    def __init__(self, receive_queue: multiprocessing.Queue, send_queue: multiprocessing.Queue):
        self.receive_queue = receive_queue
        self.send_queue = send_queue
        self.players = [{}, {}, {}]
        self.world = None

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
            pass

    def generate_map(self, x=25, y=10):
        world = [[{"loc": (x, y), "truefalse": True if 0.5 < random.random() else False} for y in range(y)] for x in range(x)]

        self.world = world


def run(receive: multiprocessing.Queue, send: multiprocessing.Queue):
    game = Game(receive, send)
    game.start()
