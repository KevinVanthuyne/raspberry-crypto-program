import sys
from binance.exceptions import BinanceAPIException
import time

from coininfo import CoinInfo
import binance_info
import peripherals


# def current_info():
#     info = CoinInfo('EUR')
#     coins = info.get_coins(['tron', 'bitcoin', 'stellar', 'raiblocks', 'cardano', 'ripple', 'iota', 'vechain', 'request-network', 'status', 'experience-points', 'neo', 'quantstamp'])
#
#     if coins is not None:
#         for coin in coins:
#             print(coin.get_info())

if __name__ == '__main__':
    try:
        binance = binance_info.BinanceInfo('key', 'key')
        p = peripherals.Peripherals()

        balances = binance.get_balances()

        print("------------------------")
        print("Current account balance:")
        print("------------------------")

        for symbol, balance in balances.items():
            print("{}: {}".format(symbol, balance))

            price, price_symbol = binance.get_current_price(symbol)

            # symbol of the currency and current account balance on Binance
            line1 = "[{}] B: {}".format(symbol, str(balance)[:10]) # show only the first 10 characters of the balance
            line2 = "Cur: {} {}".format(price[:9], price_symbol)
            line3 = "Val: {} {}".format(str(float(price) * balance)[:10], price_symbol)
            #p.add_page(line1, line2, line4=line3)

        print("------------------------")
        print("Trades:")
        print("------------------------")

        trades = binance.get_all_trades()

        for t in trades:
            print(t)

        while True:
            time.sleep(5)

    except BinanceAPIException as e:
        print(e)
    except KeyboardInterrupt:
        print("Stopped")
