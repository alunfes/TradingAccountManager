import asyncio
import websockets
import json

from CCXTRestAPI import CCXTRestAPI
from WSCommData import WSCommData


'''
WS
・receive orders from bots
・place order to CEX
・response to bot
・requst for ohlcv

'''

class WSCommunicator:
    def __init__(self) -> None:
        self.client_id = 'tam'
        self.uri = f"ws://fastapi:8080/ws/{self.client_id}" 
        self.websocket = None
        self.bot_name = {} #'bot_name':'status'
        self.crp = CCXTRestAPI()
        WSCommData.initialize()
        

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
                if message != None:
                    await self.websocket.send(message)
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"An error occurred while sending: {e}")
                break

    async def send_message(self, message):
        if self.websocket:
            print('tam sending message.')
            await self.websocket.send(json.dumps(message))
        else:
            print("No active WebSocket connection.")
    

    async def __receive_message_loop(self):
        while True:
            try:
                response = await self.websocket.recv()
                WSCommData.add_received_message(response)
                print('tam receiced message from ', response)
            except Exception as e:
                print(f"An error occurred while receiving: {e}")
                break
            await asyncio.sleep(0.5)




    async def __process_received_message(self, message):
        '''
        message = {'type':'', 'contents':''}
        type: 'init', 'order', 'close'
        init: contents:{'bot_name',}
        order: contents:{'bot_name', 'ex_name', 'symbol', 'base', 'quote', 'action', 'type', 'side', 'price', 'id', 'avg_price', 'status', 'ori_qty', 'executed_qty', 'fee', 'ts'}
        close: contents: {'bot_name'}
        ohlcv: contents: {'bot_name', 'ex_name', 'symbol', 'ohlc_min', 'since_ts'}
        free: contents: {'bot_name', 'message'}
        '''
        if message['type'] == 'init':
            self.bot_name[message['contents']['bot_name']] = 'active'
        elif message['type'] == 'order':
            message['contents']
        elif message['type'] == 'close':
            self.bot_name[message['contents']['bot_name']] = 'closed'
            print('Closed bot ', message['contents']['bot_name'])
        elif message['type'] == 'ohlcv':
            #get ohlcv using ccxt
            return 0
        elif message['type'] == 'free':
            print('free message from ', )
            return 0
        else:
            print('Invalid ws message type!', message['type'])

    async def __process_order(self, order):
        pass

    async def __get_ohlc(self, ex_name:str, symbol:str, ohlc_min:int, since_ts):
        return 0
        
