import asyncio

from WSCommData import WSCommData

class AccountUpdator:
    def __init__(self) -> None:
        self.main_loop_frequency = 60
    
    async def start(self):
        async with asyncio.TaskGroup() as tg:
            task = tg.create_task(self.__main_loop())
        
    async def __main_loop(self):
        while True:
            #send test message
            WSCommData.send_message('free', 'topbottom', 'hello from tam')
            #get data
            #jude action
            #send message
            await asyncio.sleep(self.main_loop_frequency)