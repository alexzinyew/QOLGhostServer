import asyncio
import string
import websockets
import json
import os

config = open("config.txt",'r').read()
coopServer = False
if "coopserver" in config:
    coopServer = True

userDetails = {}

connected = set()

async def server(websocket, path):

    if coopServer:
        if len(connected) > 2:
            data = {}
            data["Status"] = "Full"
            await websocket.send(json.dumps(data))
        else:
            connected.add(websocket)
            data = {}
            data["Status"] = "Connected"
            data["Role"] = len(connected)
            await websocket.send(json.dumps(data))

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
                    if user != websocket or userDetails[user]["userId"] != userId:
                        data = {'Mode': 'mapChange', 'userId': userId,
                         'Map': Map}
                        await user.send(json.dumps(data))

            elif(Mode == "Move"):
                for user in connected:
                    if user != websocket:
                        try:
                            if userDetails[user]["Map"] == userDetails[websocket]["Map"]:
                                Data = message["Data"]
                                data = {'userId': userDetails[websocket]["userId"], 'Mode': "Move", 'Data': Data}
                                await user.send(json.dumps(data))
                        except:
                            continue
                

            

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