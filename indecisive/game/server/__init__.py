import multiprocessing
import queue
from .network import Server
from .game import Game


def run(ip: str, port: int = None) -> (multiprocessing.Process, multiprocessing.Queue, multiprocessing.Queue):
    if port is None:
        port = 10000

    receive, send = multiprocessing.Queue(), multiprocessing.Queue()

    network_thread = multiprocessing.Process(target=network.run, name="Server network", args=(receive, send, ip, port))
    network_thread.start()

    game_thread = multiprocessing.Process(target=game.run, name="game", args=(receive, send))
    game_thread.start()
    print("Server started!")
    return game_thread, network_thread
