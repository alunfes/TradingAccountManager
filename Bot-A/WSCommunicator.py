import asyncio
import websockets
from websockets.exceptions import *

from WSCommData import WSCommData


class WSCommunicator:
    def __init__(self) -> None:
        self.client_id = 'topbottom'
        self.uri = f"ws://fastapi:8080/ws/{self.client_id}" 
        WSCommData.initialize()
        self.websocket = None


    async def start(self):
        try:
            self.websocket = await websockets.connect(self.uri)
            async with asyncio.TaskGroup() as tg:
                task1 = tg.create_task(self.__send_message_loop())
                task2 = tg.create_task(self.__receive_message_loop())
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if self.websocket:
                await self.websocket.close()
                self.websocket = None


    async def __send_message_loop(self):
        while True:
            try:
                message = WSCommData.get_send_message()
                if len(message) > 0:
                    await self.websocket.send(message)
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"An error occurred while sending: {e}")
                break

    async def send_message(self, message):
        if self.websocket:
            await self.websocket.send(message)
        else:
            print("No active WebSocket connection.")


    async def __receive_message_loop(self):
        while True:
            try:
                response = await self.websocket.recv()
                WSCommData.add_received_message(response)
                print(f"Received message from the server: {response}")
            except Exception as e:
                print(f"An error occurred while receiving: {e}")
                break
            await asyncio.sleep(0.5)
