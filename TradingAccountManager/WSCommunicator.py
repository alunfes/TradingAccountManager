import asyncio
import websockets


'''
WS
・receive orders from bots
・place order to CEX
・response to bot

'''

class WSCommunicator:
    def __init__(self) -> None:
        self.client_id = 'tam'
        self.bot_name = {} #'bot_name':'status'
        

    async def start(self, client_id):
        uri = f"ws://fastapi:8080/ws/{self.client_id}" 
        async with websockets.connect(uri) as websocket:
            while True:
                #await websocket.send("Hello from the trading_account_manager!")
                message = await websocket.recv()
                if 'type' in message:
                    await self.__process_received_message(message)
                else:
                    print('', message)
                asyncio.sleep(0.5)
            

    
    async def __process_received_message(self, message):
        '''
        message = {'type':'', 'contents':''}
        type: 'init', 'order', 'close'
        init: contents:{'bot_name',}
        order: contents:{'bot_name', 'ex_name', 'symbol', 'base', 'quote', 'action', 'type', 'side', 'price', 'id', 'avg_price', 'status', 'ori_qty', 'executed_qty', 'fee', 'ts'}
        close: contents: {'bot_name'}
        '''
        if message['type'] == 'init':
            self.bot_name[message['contents']['bot_name']] = 'active'
        elif message['type'] == 'order':
            message['contents']
        elif message['type'] == 'close':
            self.bot_name[message['contents']['bot_name']] = 'closed'
            print('Closed bot ', message['contents']['bot_name'])
        else:
            print('Invalid ws message type!', message['type'])

    async def __process_order(self, order):
        
