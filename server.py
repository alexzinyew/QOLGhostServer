import asyncio
import websockets
import json
import os

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

            userDetails[websocket] = {}
            userDetails[websocket]["userId"] = userId
            userDetails[websocket]["Map"] = Map

            print(message)
            print(userDetails)

            if(Mode == "mapChange"):
                for user in connected:
                    if user != websocket:
                        data = {'Mode': 'Disconnect', 'userId': userDetails[websocket]["userId"],
                         'Map': userDetails[websocket]["Map"]}
                        await user.send(json.dumps(data))

            elif(Mode == "Move"):
                for user in connected:
                    if user != websocket:
                        if userDetails[user]["Map"] == userDetails[websocket]["Map"]: #On the same map
                            Data = message["Data"]
                            data = {'userId': userDetails[websocket]["userId"], 'Mode': "Move", 'Data': Data}
                            await user.send(json.dumps(data))
                

            

    finally:
        print("Client disconnected")
        for user in connected:
            if user != websocket:
                data = {'Mode': 'Disconnect', 'userId': userDetails[websocket]["userId"]}
                await user.send(json.dumps(data))

        connected.remove(websocket)
        del userDetails[websocket]

async def main():
    async with websockets.serve(server, "", int(os.environ["PORT"])):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())