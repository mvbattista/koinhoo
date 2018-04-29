import argparse
from pprint import pprint
from collections import defaultdict

from koinprefs import KoinPrefs
from exchanges import *


class Koinhoo(KoinPrefs):
    def __init__(self):
        super().__init__('koinhoo')
        self.all_exchanges = self._get_prefs()
        self.processor_for = {
            'CMC': CoinMarketCapExchange,
            'BINANCE': BinanceExchange,
            'KUCOIN': KuCoinExchange,
        }

    def _setup_exchange(self, exch):
        constructor = self.processor_for[exch['exchange']]
        return constructor

    def get_all_rates(self, by_rates=False):
        all_rates = []
        for exch in self.all_exchanges:
            constructor = self._setup_exchange(exch)
            print('{}'.format(exch['exchange']))
            exch_processor = constructor()
            exch_rates = exch_processor.get_rates(exch['currencies'])
            all_rates.extend(exch_rates)
        if by_rates:
            result = defaultdict(list)
            for x in all_rates:
                data = {'rate': x['rate'], 'network': x['network']}
                result[x['currency']].append(data)
            return dict(result)

        return all_rates

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--networks', nargs='+', type=str, required=False)
    args = parser.parse_args()
    kh = Koinhoo()
    pprint(kh.get_all_rates(by_rates=True))
