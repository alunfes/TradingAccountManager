import ccxt.async_support as ccxt
import time
import datetime
import itertools
import asyncio
import os
import yaml
import pprint
import requests

from DisplayMessage import DisplayMessage



class CCXTRestAPI:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self):
        self.exchanges = ['bybit', 'okx']
        self.__read_api_key()
        self.ccxt_exchanges = {}
        loop = asyncio.get_event_loop()
        for ex in self.exchanges:
            self.ccxt_exchanges[ex] = self.__get_exchanges(ex)
        self.ex_num_downloads = {'okx':100, 'bybit':100}
    
    async def initialize(self):
        for ex in self.exchanges:
            await self.ccxt_exchanges[ex].load_markets()


    def __read_api_key(self):
        self.public_keys = {}
        self.secret_keys = {}
        self.password = {}
        with open('./ignore/api.yaml', 'r') as f:
            api_keys = yaml.load(f, Loader=yaml.FullLoader)
            for ex in self.exchanges:
                self.public_keys[ex] = api_keys[ex]['public_key']
                self.secret_keys[ex] = api_keys[ex]['secret_key']
                if ex == 'okx':
                    self.password[ex] = api_keys[ex]['password']
                else:
                    self.password[ex] = ''

    def __get_exchanges(self, ex_name:str):
        #return getattr(ccxt, ex_name)({ 'enableRateLimit': True })
        exchange_class = getattr(ccxt, ex_name)
        exchange_instance = exchange_class({
            'apiKey': self.public_keys[ex_name],
            'secret': self.secret_keys[ex_name],
            'password': self.password[ex_name],
            'enableRateLimit': True,
        })
        return exchange_instance
    
    
    '''
    id	symbol	base	quote	baseId	quoteId	active	type	linear	inverse	spot	swap	future	option	margin	contract	contractSize	expiry	expiryDatetime	optionType	strike	settle	settleId	precision	limits	info	percentage	feeSide	tierBased	taker	maker	lowercaseId
    '''
    async def get_tickers(self, ex_name):
        res = await self.ccxt_exchanges[ex_name].load_markets()
        df = pd.DataFrame(res).transpose()
        return df[df['active'] == True]
    
    
    async def send_order(self, ex_name, symbol, order_type:str, side:str, price, amount):
        """
        指定されたsymbolに対して、指定されたorder_typeの注文を出し、約定情報を返す関数
        Args:
            symbol (str): 注文するトレードペアのシンボル
            order_type (str): 'limit'または'market'のいずれか。注文タイプを指定する。
            price (float, optional): リミット注文の場合、注文価格を指定する。マーケット注文の場合は不要。
            amount (float, optional): 注文する数量を指定する。リミット注文の場合、base通貨での数量を指定する。
                                    マーケット注文の場合は、base通貨またはquote通貨での数量を指定できる。
        Returns:
            dict: 約定情報を含む辞書。注文が失敗した場合はNoneを返す。
            binance: 
            limit: {'orderId': '4695181725', 'symbol': 'ALICEUSDT', 'status': 'NEW', 'clientOrderId': '3OBMscMBHWcBXmXnzJ7deT', 'price': '1', 'avgPrice': '0.0000', 'origQty': '10', 'executedQty': '0', 'cumQty': '0', 'cumQuote': '0', 'timeInForce': 'GTC', 'type': 'LIMIT', 'reduceOnly': False, 'closePosition': False, 'side': 'BUY', 'positionSide': 'BOTH', 'stopPrice': '0', 'workingType': 'CONTRACT_PRICE', 'priceProtect': False, 'origType': 'LIMIT', 'updateTime': '1681263917931'}
            market: {'orderId': '9446494975', 'symbol': 'TRXUSDT', 'status': 'NEW', 'clientOrderId': 'Y4QrMXGPVAkCTsllqGLXsV', 'price': '0', 'avgPrice': '0.00000', 'origQty': '100', 'executedQty': '0', 'cumQty': '0', 'cumQuote': '0', 'timeInForce': 'GTC', 'type': 'MARKET', 'reduceOnly': False, 'closePosition': False, 'side': 'SELL', 'positionSide': 'BOTH', 'stopPrice': '0', 'workingType': 'CONTRACT_PRICE', 'priceProtect': False, 'origType': 'MARKET', 'updateTime': '1681288077482'}
            bybit:
            limit: {'info': {'orderId': '0c5cd103-df4c-4e44-844f-a7c12d722f7f', 'orderLinkId': ''}, 'id': '0c5cd103-df4c-4e44-844f-a7c12d722f7f', 'clientOrderId': None, 'timestamp': None, 'datetime': None, 'lastTradeTimestamp': None, 'symbol': None, 'type': None, 'timeInForce': None, 'postOnly': None, 'reduceOnly': None, 'side': None, 'price': None, 'stopPrice': None, 'triggerPrice': None, 'amount': None, 'cost': None, 'average': None, 'filled': None, 'remaining': None, 'status': None, 'fee': None, 'trades': [], 'fees': []}
            market: {'info': {'orderId': 'b1a18135-5982-4758-ada4-58026d1a2c8a', 'orderLinkId': ''}, 'id': 'b1a18135-5982-4758-ada4-58026d1a2c8a', 'clientOrderId': None, 'timestamp': None, 'datetime': None, 'lastTradeTimestamp': None, 'symbol': None, 'type': None, 'timeInForce': None, 'postOnly': None, 'reduceOnly': None, 'side': None, 'price': None, 'stopPrice': None, 'triggerPrice': None, 'amount': None, 'cost': None, 'average': None, 'filled': None, 'remaining': None, 'status': None, 'fee': None, 'trades': [], 'fees': []}
            okx:
            limit: {'info': {'clOrdId': 'e847386590ce4dBCd067c185e0d4da43', 'ordId': '566281938647322631', 'sCode': '0', 'sMsg': 'Order placed', 'tag': 'e847386590ce4dBC'}, 'id': '566281938647322631', 'clientOrderId': 'e847386590ce4dBCd067c185e0d4da43', 'timestamp': None, 'datetime': None, 'lastTradeTimestamp': None, 'symbol': 'BSV/USDT:USDT', 'type': 'limit', 'timeInForce': None, 'postOnly': None, 'side': 'sell', 'price': None, 'stopLossPrice': None, 'takeProfitPrice': None, 'stopPrice': None, 'triggerPrice': None, 'average': None, 'cost': None, 'amount': None, 'filled': None, 'remaining': None, 'status': None, 'fee': None, 'trades': [], 'reduceOnly': False, 'fees': []}
            market: {'info': {'clOrdId': 'e847386590ce4dBC6b998cb4b173f5e2', 'ordId': '566286360827858944', 'sCode': '0', 'sMsg': 'Order placed', 'tag': 'e847386590ce4dBC'}, 'id': '566286360827858944', 'clientOrderId': 'e847386590ce4dBC6b998cb4b173f5e2', 'timestamp': None, 'datetime': None, 'lastTradeTimestamp': None, 'symbol': 'DOGE/USDT:USDT', 'type': 'market', 'timeInForce': None, 'postOnly': None, 'side': 'sell', 'price': None, 'stopLossPrice': None, 'takeProfitPrice': None, 'stopPrice': None, 'triggerPrice': None, 'average': None, 'cost': None, 'amount': None, 'filled': None, 'remaining': None, 'status': None, 'fee': None, 'trades': [], 'reduceOnly': False, 'fees': []}
        """
        try:
            amount = abs(amount) #sellの時はマイナス表示なのでqtyを参照して反対売買するときにエラーにならないように。
            order = None
            if order_type == 'limit':
                if price == 0: #limit orderでpriceが0の時は一番近いbid/askにorderを出す。
                    book = await self.fetch_order_book(ex_name, symbol)
                    price = float(book['bids'][0][0]) if side == 'buy' else float(book['asks'][0][0])
                if ex_name=='binance':
                    order = await self.ccxt_exchanges[ex_name].fapiPrivatePostOrder({'symbol':symbol,'type':'LIMIT','side':side.upper(),'price':price,'quantity':amount, 'timeInForce':'GTC'})
                else:
                    order = await self.ccxt_exchanges[ex_name].create_order(symbol, 'limit', side.lower(), amount, price)
                    order['orderId'] = order['info']['ordId'] if ex_name == 'okx' else order['info']['orderId']
                return order
            elif order_type == 'market':
                # 数量を指定して注文を出す
                if ex_name=='binance':
                    order = await self.ccxt_exchanges[ex_name].fapiPrivatePostOrder({'symbol':symbol,'type':'MARKET','side':side.upper(), 'quantity':amount})
                else:
                    order = await self.ccxt_exchanges[ex_name].create_market_order(symbol, side, amount)
                    order['orderId'] = order['info']['ordId'] if ex_name == 'okx' else order['info']['orderId']
                return order
            else:
                raise ValueError('Invalid order type')
        except ccxt.InsufficientFunds as e:
            # 残高不足の場合はエラーを出す
            DisplayMessage.display_message('CCXTRestApi', 'send_order', 'error', 
                                           [e,
                                            ex_name + ':'+symbol,
                                            'side='+side,
                                            'price='+str(price),
                                            'lot='+str(amount)])
            #CommunicationData.add_message('Error', 'CCXTRestAPI', 'send_order', e)
            return e
        except ccxt.InvalidOrder as e:
            # 注文が不正
            DisplayMessage.display_message('CCXTRestApi', 'send_order', 'error', 
                                           [e,
                                            ex_name + ':'+symbol,
                                            'side='+side,
                                            'price='+str(price),
                                            'lot='+str(amount)])
            #CommunicationData.add_message('Error', 'CCXTRestAPI', 'send_order', e)
            return e
        except Exception as e:
            DisplayMessage.display_message('CCXTRestApi', 'send_order', 'error', 
                                           [e,
                                            ex_name + ':'+symbol,
                                            'side='+side,
                                            'price='+str(price),
                                            'lot='+str(amount)])
            #CommunicationData.add_message('Error', 'CCXTRestAPI', 'send_order', e)
            return e
        

    async def get_ohlc(self, ex_name:str, symbol:str, ohlc_min:int, since_ts:int):
        ohlcv = []
        timeframe = {1:'1m', 5:'5m', 60:'1h', 240:'4h', 480:'8h', 1440:'1d'}[ohlc_min]
        num_downloads = self.ex_num_downloads[ex_name]
        while True:
            res = await self.__get_ohlc(ex_name, symbol, timeframe, since_ts, num_downloads)
            await asyncio.sleep(0.1)
            if len(res) > 0:
                ohlcv.extend(res)
                since_ts = res[-1][0] + ohlc_min
                #print(ex_name, '-', symbol, ' len=', len(res), ', since_ts=',since_ts, ', res last=', res[-1][0])
            if len(res) < num_downloads*0.5:
                print('ohlc download completed - ', ex_name, ' : ', symbol, ', res=',len(res), ':', num_downloads)
                break
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['dt'] = pd.to_datetime(df['timestamp'], unit='ms')
        df = df.reindex(columns=['timestamp','dt','open','high','low','close','volume'])
        df.set_index('timestamp', inplace=True)
        # ダウンロードしたデータをCSVファイルに保存
        filename = ex_name+'-'+symbol.replace('/','').split(':')[0]+'.csv'
        df.to_csv('./Data/ohlcv/'+filename, index=False)
        return {'symbol':symbol, 'ohlcv':ohlcv}