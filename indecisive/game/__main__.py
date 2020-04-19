from server import Server
import asyncio


what = int(input("What are you (0 - server, 1 - client)"))

if what == 0:
    print("You are a Server")
    server = Server()
    loop = asyncio.get_event_loop()
    loop.create_task(server.start())
    loop.run_until_complete(server.websocket())
    loop.run_forever()
    server.close()
else:
    import client
