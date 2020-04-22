import queue
import json


class Game:
    def __init__(self, receive_queue: queue.Queue, send_queue: queue.Queue):
        self.receive = receive_queue
        self.send = send_queue
        self.players = [{}, {}, {}]

    def start(self):
        while True:
            data = self.receive.get()
            if data["type"] == "newConnection":
                self.players[data["connection"]] = {"connected": True, "name": ""}
            elif data["type"] == "nameChange":
                self.players[data["connection"]]["name"] = data["newName"][:12]
                self.send.put({"type": "playersUpdate", "data": self.players})
