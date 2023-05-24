import asyncio
import json
import uuid

import websockets
from pymongo import MongoClient

# SETTINGS
MONGO_CONNECT_STRING = "mongodb+srv://noticy:76BZJDtw6KtzZn1W@cluster0.mlaq4tt.mongodb.net/?retryWrites=true&w=majority"
DEFAULT_PORT = 8001


class Server:
    clients = {}
    mongo = MongoClient(MONGO_CONNECT_STRING)

    def __init__(self) -> None:
        self.db = self.mongo["CritiCat"]
        self.raw_coll = self.db["raw"]

    async def send(self, websocket, client_id: str):
        try:
            # TODO: replace with the Kafka consumer: listen to label ->
            while True:
                # send dummy message
                await websocket.send("ping")

                # delay
                await asyncio.sleep(2)

        except websockets.exceptions.ConnectionClosedOK:
            print("Client disconnected")
            self.clients.pop(client_id)

    async def receive(self, websocket, client_id: str):
        try:
            # TODO: listen to 2 different type of messages: raw text and feedback signals
            while True:
                # read raw response from client
                raw_response = await websocket.recv()

                # convert raw response to json object
                article = json.loads(raw_response)

                # insert new article to database
                id = self.raw_coll.insert_one(article).inserted_id

                # send signal to bigcat

        except websockets.exceptions.ConnectionClosedOK:
            print(f"Client {client_id} disconnected!")
            self.clients.pop(client_id)

    async def handler(self, websocket):
        # * add new client to clients list
        client_id = str(uuid.uuid4())
        self.clients.update({client_id: websocket})
        print(
            f"New client connected -> assigned id: {client_id} | current number of clients: {len(self.clients)}"
        )

        # * create parallel tasks for client
        send_task = asyncio.create_task(self.send(websocket, client_id))
        receive_task = asyncio.create_task(self.receive(websocket, client_id))

        # * terminate both tasks when any of them have completed
        done, pending = await asyncio.wait(
            [send_task, receive_task],
            return_when=asyncio.FIRST_COMPLETED,
        )

        # * cancel them
        for task in pending:
            task.cancel()

    async def communicate(self):
        async with websockets.serve(self.handler, "", DEFAULT_PORT):
            await asyncio.Future()


if __name__ == "__main__":
    print("CritiCat server is running!")
    server = Server()
    asyncio.run(server.communicate())
