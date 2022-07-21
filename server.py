import asyncio
from pydoc import doc
from statistics import mode
import websockets
import json
import signal
import os
import pprint

userDetails = {}

connected = set()

async def server(websocket, path):

    connected.add(websocket)
    print("Client connected!") 
    try:
        async for message in websocket:
            message = json.loads(message)
            userId = message["userId"]
            Map = message["Map"]
            Mode = message["Mode"]

            userDetails[websocket]["userId"] = userId
            userDetails[websocket]["Map"] = Map

            if(Mode == "mapChange"):
                for user in connected:
                    if user != websocket:
                        data = {'Mode': 'Disconnect', 'userId': userDetails[websocket]["userId"],
                         'Map': userDetails[websocket]["Map"]}

            elif(Mode == "Move"):
                for user in connected:
                    if user != websocket:
                        if userDetails[user]["Map"] == userDetails[websocket]["Map"]: #On the same map
                            Data = message["Data"]
                            user.send(json.dumps(userId,Mode,Data))
                

            

    finally:
        print("Client disconnected")
        for user in connected:
            if user != websocket:
                data = {'Mode': 'Disconnect', 'userId': userDetails[websocket]["userId"]}
                user.send(json.dumps(data))

        connected.remove(websocket)
        del userDetails[websocket]

async def main():
    async with websockets.serve(server, "localhost", 3000):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())