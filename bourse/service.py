import json
import threading
from datetime import datetime
import time
import requests
from django.forms.models import model_to_dict

from bourse.models import Coin

bourse = {}


def main():
    url = 'https://api.coingecko.com/api/v3/coins/' \
          'markets?vs_currency=try&order=market_cap_desc&per_page=100&page=1&sparkline=false'
    while True:
        data = requests.get(url).json()

        for coin in data:
            obj = Coin.objects.filter(symbol=coin['symbol']).first() or Coin()

            obj.name = coin['name']
            obj.symbol = coin['symbol']

            state = 'state'

            if obj.prices is None:
                price = coin['current_price']
                json_data = {state: {datetime.now().strftime('%d/%m/%Y %H:%M:%S'): price}}
            else:
                json_data = json.loads(str(obj.prices))
                entry = list(json_data['state'].items())[-1]
                price = entry[1]
                now = datetime.now()
                if price == coin['current_price']:
                    del json_data['state'][entry[0]]
                json_data['state'][now.strftime('%d/%m/%Y %H:%M:%S')] = coin['current_price']
                for key, value in dict(json_data['state']).items():
                    key_date = datetime.strptime(key, '%d/%m/%Y %H:%M:%S')
                    if (now - key_date).total_seconds() > 86400:
                        del json_data['state'][key]

            if price > coin['current_price']:
                state = 'fall'
            elif price == coin['current_price']:
                state = 'same'
            elif price < coin['current_price']:
                state = 'raise'

            obj.prices = json.dumps(json_data)
            obj.momentary_up = coin['high_24h']
            obj.momentary_down = coin['low_24h']
            obj.rank = coin['market_cap_rank']
            obj.image = coin['image']

            obj.save()

            obj.prices = coin['current_price']

            new_data = model_to_dict(obj)
            new_data.update({'state': state})
            new_data.update({'history': json_data['state']})

            bourse[obj.name] = new_data
        time.sleep(30)


thread = threading.Thread(target=main)
thread.start()
