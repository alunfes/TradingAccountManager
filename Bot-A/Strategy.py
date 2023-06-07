from ActionData import ActionData

class Strategy:
    @classmethod
    def initialize(cls):
        pass

    @classmethod
    def get_action(cls):
        ad = ActionData() 
        ad.add_action('buy', '', 'bybit', 'ETHUSDT', 'ETH', 'USDT', 'market', 0, 0.1)
        return ad