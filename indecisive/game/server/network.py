import asyncio
import websockets
import json
import threading
import queue


class Server:
    def __init__(self, receive_queue: queue.Queue, send_queue: queue.Queue):
        self.receive = receive_queue
        self.send = send_queue
        self.connections = []
        self.loop = asyncio.get_event_loop()

    async def _start(self):
        while True:
            for connection in self.connections:
                pass
            await asyncio.sleep(0.1)

    async def _recv(self):
        while True:
            data = await self.connection.recv()
            for connection in self.connections:
                await connection.send(data)

    def _websocket(self, ip: str, port: int):
        # noinspection PyTypeChecker
        return websockets.serve(self._connection_manager, ip, port)

    async def _connection_manager(self, websocket, path):
        print(f"Connection from {path}")
        self.connections.append(websocket)
        async for message in websocket:
            pass

    def start(self, ip: str, port: int = 10000):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        self.loop.create_task(self._start())
        self.loop.run_until_complete(self._websocket(ip, port))
        self.loop.run_forever()


def run(ip: str, port: int = None) -> (threading.Thread, queue.Queue, queue.Queue):
    receive, send = queue.Queue(), queue.Queue()
    server = Server(receive, send)
    if port is None:
        port = 10000
    network_thread = threading.Thread(target=server.start, name="network", args=(ip, port))
    network_thread.start()
    print("Network Server started!")
    return network_thread, receive, send
