import asyncio
import websockets
import json
import signal
import os

connected = set()

async def server(websocket, path):

    connected.add(websocket)
    print("Client connected!") 
    try:
        async for message in websocket:
            message = json.loads(message)
            print(message)
    finally:
        print("Client disconnected")
        connected.remove(websocket)

async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with websockets.serve(
        server,
        host="localhost",
        port=int(os.environ["PORT"]),
    ):
        await stop


if __name__ == "__main__":
    asyncio.run(main())