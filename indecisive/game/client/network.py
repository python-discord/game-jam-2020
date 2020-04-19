import asyncio
import websockets


async def run():
    connection = await websockets.connect("ws://localhost:10000")
    while True:
        print(f"Received: {await connection.recv()}")

asyncio.run(run())
