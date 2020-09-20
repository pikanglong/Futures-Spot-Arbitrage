import ccxt
import json
import requests

exchange = ccxt.huobipro({
    'urls': {
        'api': {
            'market': 'https://api.huobi.pro',
            'public': 'https://api.huobi.pro',
            'private': 'https://api.huobi.pro',
        },
    },
    'proxies': {
        'http': 'http://localhost:1087',
        'https': 'http://localhost:1087',
    },
})

trade_coin = ['BTC', 'ETH', 'EOS', 'LINK', 'BCH', 'BSV', 'LTC', 'XRP', 'ETC', 'TRX', 'ADA']

for tc in trade_coin:
    spot_symbol = tc + '/USDT'
    spot_ticker = exchange.fetch_ticker(spot_symbol)
    spot_price = spot_ticker['last']

    future_url = 'https://api.btcgateway.pro/market/history/kline?period=1min&size=1&symbol=' + tc + '_CQ'
    r = requests.get(future_url, timeout = 3)
    r.raise_for_status()
    data = json.loads(r.text)
    future_price = data['data'][0]['close']

    diff = ( future_price / spot_price - 1 ) * 100
    print('{:5s} {:+.2f}%'.format(tc, diff))