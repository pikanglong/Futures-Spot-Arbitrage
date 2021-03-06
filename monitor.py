import ccxt
import json
import time
import requests

huobi = ccxt.huobipro({
    'urls': {
        'proxies': {
            'http': 'localhost:7890',
            'https': 'localhost:7890',
        }
    },
})
huobi_trade_coin = ['BTC', 'ETH', 'LINK', 'DOT', 'EOS', 'TRX', 'ADA', 'LTC', 'BCH', 'XRP', 'BSV', 'ETC', 'FIL']

okex = ccxt.okex({
    'urls': {
        'proxies': {
            'http': 'localhost:7890',
            'https': 'localhost:7890',
        }
    },
})
okex_trade_coin = ['BTC', 'ETH', 'LTC', 'DOT', 'TRX', 'BCH', 'BSV', 'EOS', 'ETC', 'LINK', 'XRP']

binance = ccxt.binance({
    'urls': {
        'proxies': {
            'http': 'localhost:7890',
            'https': 'localhost:7890',
        }
    },
})
binance_trade_coin = ['BTC', 'ETH', 'LINK', 'BNB', 'DOT', 'ADA', 'LTC', 'BCH', 'XRP']

type = ['_CW', '_NW', '_CQ', '_NQ']
name = ['当周合约：', '次周合约：', '当季合约：', '次季合约：']
date = ['210423', '210430', '210625', '210924']

while True:
    for i in range(4):
        result = {}
        try:
            for tc in huobi_trade_coin:
                spot_symbol = tc + '/USDT'
                spot_ticker = huobi.fetch_ticker(spot_symbol)
                spot_price = spot_ticker['last']

                future_url = 'https://api.btcgateway.pro/market/history/kline?period=1min&size=1&symbol=' + tc + type[i]
                r = requests.get(future_url, timeout = 3)
                r.raise_for_status()
                data = json.loads(r.text)
                future_price = data['data'][0]['close']

                k = '火币 ' + tc
                v = ( future_price / spot_price - 1 ) * 100
                result[k] = v

            for tc in okex_trade_coin:
                spot_symbol = tc + '/USDT'
                spot_ticker = okex.fetch_ticker(spot_symbol)
                spot_price = spot_ticker['last']

                future_symbol = tc + '-USDT-' + date[i]
                future_ticker = okex.fetch_ticker(future_symbol)
                future_price = future_ticker['last']

                k = '欧易 ' + tc
                v = ( future_price / spot_price - 1 ) * 100
                result[k] = v

            if i >= 2:
                for tc in binance_trade_coin:
                    spot_symbol = tc + '/USDT'
                    spot_ticker = binance.fetch_ticker(spot_symbol)
                    spot_price = spot_ticker['last']

                    future_url = 'https://dapi.binance.com/dapi/v1/ticker/price?symbol=' + tc + 'USD_' + date[i]
                    r = requests.get(future_url, timeout = 3)
                    r.raise_for_status()
                    data = json.loads(r.text)
                    future_price = data[0]['price']

                    k = '币安 ' + tc
                    v = ( float(future_price) / float(spot_price) - 1 ) * 100
                    result[k] = v

            print(name[i])
            for res in sorted(result.items(), key = lambda kv:(kv[1], kv[0])):
                print('{:7s} {:+.2f}%'.format(res[0], res[1]))

        except Exception as e:
            print(name[i])
            print('error:', e)

    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    print('-----------------')
