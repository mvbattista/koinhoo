import requests


class BaseExchange(object):
    def __init__(self):
        self.url = ''

    def get_all_rates(self):
        raise NotImplementedError('get_all_rates required for all processors.')

    def get_rates(self, currencies=None):
        if not currencies:
            return []

    def get_rate(self, currency=None):
        if not currency:
            return {}


class CoinMarketCapExchange(BaseExchange):
    def __init__(self):
        super().__init__()
        self.url = 'https://coinmarketcap.com'

    def get_all_rates(self):
        return []
