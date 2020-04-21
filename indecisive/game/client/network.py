import asyncio
import websockets
import queue
import threading
import socket


class Client:
    def __init__(self, receive_queue: queue.Queue, send_queue: queue.Queue):
        self.receive = receive_queue
        self.send = send_queue
        self.connection = None
        self.loop = None
        self.ip = None
        self.port = None

    def start(self, ip: str, port: int = 10000):
        self.ip = ip
        self.port = port
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._start())

    async def _start(self):
        try:
            self.connection = await websockets.connect(f"ws://{self.ip}:{self.port}")
            self.receive.put(0)
            while True:
                self.receive.put(await self.connection.recv())
        except websockets.InvalidURI:
            self.receive.put(1)
        except websockets.InvalidHandshake:
            self.receive.put(2)
        except ConnectionRefusedError:
            self.receive.put(3)
        except socket.gaierror:
            self.receive.put(4)
        except OSError:
            self.receive.put(5)


def run(ip: str, port: int = None) -> (threading.Thread, queue.Queue, queue.Queue):
    receive, send = queue.Queue(), queue.Queue()
    client = Client(receive, send)
    if port is None:
        port = 10000
    network_thread = threading.Thread(target=client.start, name="network", args=(ip, port))
    network_thread.start()
    print("Network Client started!")

    return network_thread, receive, send
