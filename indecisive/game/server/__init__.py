import socket
import asyncio
import websockets


class Server:
    def __init__(self):
        self.connections = []
        self.loop = asyncio.get_event_loop()

    async def start(self):
        while True:
            for connection in self.connections:
                await connection.send(f"Test. There are {len(self.connections)} connections")
            await asyncio.sleep(1)

    def websocket(self):
        return websockets.serve(self.connection_manager, "localhost", 10000)

    async def connection_manager(self, websocket, path):
        print(f"Connection from {path}")
        self.connections.append(websocket)
        async for message in websocket:
            await asyncio.sleep(0)

    def close(self):
        pass


def run():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server = Server()
    loop.create_task(server.start())
    loop.run_until_complete(server.websocket())
    loop.run_forever()
