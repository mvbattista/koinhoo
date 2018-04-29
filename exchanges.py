import requests
from decimal import Decimal

class BaseExchange(object):
    def __init__(self):
        self.url = ''
        self.name = 'Koinhoo' # This should never show
        self.rate_for = {}

    def _get_all_rates(self):
        raise NotImplementedError('get_all_rates required for all processors.')

    def get_rates(self, currencies=None):
        if not currencies:
            return []
        result = []
        for currency in currencies:
            x = {
                'network': self.name,
                'currency': currency,
                'rate': self.rate_for.get(currency)
            }
            if x['rate']:
                result.append(x)
        return result

    def get_rate(self, currency=None):
        if not currency:
            return {}
        param = []
        param.append(currency)
        return self.get_rates(currencies=param)[0]


class CoinMarketCapExchange(BaseExchange):
    def __init__(self):
        super().__init__()
        self.url = 'https://api.coinmarketcap.com/v1/ticker/'
        self.name = 'CoinMarketCap'
        self._get_all_rates()

    def _get_all_rates(self):
        raw_data = requests.get(self.url).json()
        for x in raw_data:
            self.rate_for[x['symbol']] = x['price_usd']

class BinanceExchange(BaseExchange):
    def __init__(self):
        super().__init__()
        self.url = 'https://api.binance.com/api/v3/ticker/price'
        self.name = 'Binance'
        self._get_all_rates()

    def _get_all_rates(self):
        raw_data = requests.get(self.url).json()
        usd_rates = [x for x in raw_data if 'USDT' in x['symbol']]
        for x in usd_rates:
            symbol = x['symbol'].replace('USDT','')
            self.rate_for[symbol] = x['price']

class KuCoinExchange(BaseExchange):
    def __init__(self):
        super().__init__()
        self.url = 'https://kitchen-5.kucoin.com/v1/market/open/symbols'
        self.name = 'KuCoin'
        self._get_all_rates()

    def _get_all_rates(self):
        raw_data = requests.get(self.url).json()['data']
        usd_rates = [x for x in raw_data if x['coinTypePair'] == 'USDT']
        for x in usd_rates:
            self.rate_for[x['coinType']] = str(x['lastDealPrice'])
        for x in raw_data:
            if x['coinTypePair'] == 'USDT' or x['coinType'] in self.rate_for:
                continue
            self.rate_for[x['coinType']] = str(Decimal(str(x['lastDealPrice'])) * \
                                           Decimal(self.rate_for[x['coinTypePair']]))

