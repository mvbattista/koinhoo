import argparse
from battprefs import BattPrefs

class Koinhoo(BattPrefs):
    def __init__(self):
        super().__init__('koinhoo')
        all_prefs = self._get_prefs()

    def get_all_rates(self):
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--networks', nargs='+', type=str, required=False)
    args = parser.parse_args()
    kh = Koinhoo()
    kh.get_all_rates()
