import asyncio
import websockets


class Bot:
    def __init__(self) -> None:
        self.client_id = 'b'

    async def connect(self, client_id):
        uri = f"ws://fastapi:8080/ws/{client_id}" 
        async with websockets.connect(uri) as websocket:
            await websocket.send("Hello from the bot-b!")
            response = await websocket.recv()
            print(f"Received message from the server: {response}")


# bot1としてインスタンス化し、そのconnectメソッドを呼び出す
bot = Bot()
asyncio.get_event_loop().run_until_complete(bot.connect('b'))