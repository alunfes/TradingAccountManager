import asyncio

from bot import Bot
from WSCommunicator import WSCommunicator

class Main:
    def __init__(self) -> None:
        print('init bot-B')

    async def start(self):
        ws_comm = WSCommunicator()
        bot = Bot()
        async with asyncio.TaskGroup() as tg:
            task1 = tg.create_task(ws_comm.start())
            task2 = tg.create_task(bot.start())

# bot1としてインスタンス化し、そのconnectメソッドを呼び出す
bot_main = Main()
asyncio.run(bot_main.start())