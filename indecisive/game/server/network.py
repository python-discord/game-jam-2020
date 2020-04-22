import asyncio
import websockets
import json
import multiprocessing
import queue


class Server:
    def __init__(self, receive_queue: multiprocessing.Queue, send_queue: multiprocessing.Queue):
        self.receive = receive_queue
        self.send = send_queue
        self.connections = []
        self.loop = asyncio.get_event_loop()

    async def _send(self):
        while True:
            try:
                data = self.send.get(block=False)
            except queue.Empty:
                pass
            else:
                try:
                    data = json.dumps(data)
                except (TypeError, OverflowError, ValueError):
                    print(f"Error encoding json: {data}")
                else:
                    for connection in self.connections:
                        await connection.send(data)
            await asyncio.sleep(0.05)

    def _websocket(self, ip: str, port: int):
        # noinspection PyTypeChecker
        return websockets.serve(self._recv, ip, port)

    async def _recv(self, websocket, path):
        if len(self.connections) < 3:
            self.connections.append(websocket)
            connection_number = self.connections.index(websocket)
            await websocket.send(json.dumps({"type": "connectionNumber", "data": connection_number}))
            self.receive.put({"type": "newConnection", "connection": connection_number})

            async for message in websocket:
                try:
                    message = json.loads(message)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON {message}")
                else:
                    message["connection"] = connection_number
                    self.receive.put(message)

        await websocket.close()

    def start(self, ip: str, port: int = 10000):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        self.loop.create_task(self._send())
        self.loop.run_until_complete(self._websocket(ip, port))
        self.loop.run_forever()


def run(receive, send, ip, port):
    network = Server(receive, send)
    network.start(ip, port)
