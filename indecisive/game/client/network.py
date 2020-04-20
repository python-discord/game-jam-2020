import asyncio
import websockets


class Client:
    async def run(self):
        self.connection = await websockets.connect("ws://localhost:10000")
        while True:
            print(f"Received: {await self.connection.recv()}")


def run():
    client = Client()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(client.run())
