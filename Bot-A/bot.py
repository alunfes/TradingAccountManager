import asyncio
import json
import aiohttp

from WSCommData import WSCommData
from Strategy import Strategy

'''
ws messageのやり取りは全てWSCommDataに入れて・参照して行う。
・get data and judge action, then send it using ws
・
'''
class Bot:
    def __init__(self) -> None:
        self.main_loop_frequency = 5
        Strategy.initialize()
    
    async def start(self):
        async with asyncio.TaskGroup() as tg:
            task = tg.create_task(self.__main_loop())
        
    async def __main_loop(self):
        while True:
            #send test message
            WSCommData.send_message('free', 'topbottom', 'hello from topbottom')
            #get data
            #jude action
            #send message
            await asyncio.sleep(self.main_loop_frequency)

    async def update_order(order_id: int, order_data: dict):
        url = f"http://localhost:8000/orders/{order_id}"
        headers = {'Content-Type': 'application/json'}

        async with aiohttp.ClientSession() as session:
            async with session.put(url, headers=headers, data=json.dumps(order_data)) as response:
                print("Status:", response.status)
                print("Content:", await response.text())

order_data = {
    'bot_name': 'Bot-A',
    'ex_name': 'Exchange1',
    'symbol': 'BTC/USD',
    'base': 'BTC',
    'quote': 'USD',
    'action': 'BUY',
    'type': 'LIMIT',
    'side': 'BUY',
    'price': 50000.0,
    'avg_price': 50000.0,
    'status': 'FILLED',
    'ori_qty': 0.1,
    'executed_qty': 0.1,
    'fee': 0.001,
    'ts': 1640995200
}