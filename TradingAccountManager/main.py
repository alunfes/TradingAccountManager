import asyncio
import websockets

from WSCommunicator import WSCommunicator
from AccountUpdator import AccountUpdator

'''
WS
・receive orders from bots
・place order to CEX
・response to bot

'''

class TradaingAccountManager:
    def __init__(self) -> None:
        print('init tam')

    async def main(self):
        ws_com = WSCommunicator()
        ac_updator = AccountUpdator()
        await asyncio.gather(
            ws_com.start(),
            ac_updator.start()
        )


# bot1としてインスタンス化し、そのconnectメソッドを呼び出す
tam = TradaingAccountManager()
print('tam starting')
asyncio.run(tam.main())
print('tam ended')