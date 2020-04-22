import threading
import queue
from .network import Server
from .game import Game


def run(ip: str, port: int = None) -> (threading.Thread, queue.Queue, queue.Queue):
    if port is None:
        port = 10000

    receive, send = queue.Queue(), queue.Queue()

    network = Server(receive, send)
    network_thread = threading.Thread(target=network.start, name="network", args=(ip, port))
    network_thread.start()

    game = Game(receive, send)
    game_thread = threading.Thread(target=game.start, name="game")
    game_thread.start()
    print("Server started!")
    return game_thread, network_thread
