import asyncio
import websockets

from WSCommunicator import WSCommunicator

'''
WS
・receive orders from bots
・place order to CEX
・response to bot

'''

class TradaingAccountManager:
    def __init__(self) -> None:
        pass

    async def main():
        ws_com = WSCommunicator()
        await asyncio.gather(
            ws_com.start(),
        )


# bot1としてインスタンス化し、そのconnectメソッドを呼び出す
tam = TradaingAccountManager()
asyncio.run(tam.main())