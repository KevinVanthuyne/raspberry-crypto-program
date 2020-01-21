from binance.client import Client
import json

from trade import Trade

class BinanceInfo():
    """ Class for all information about your Binance account """

    def __init__(self, api_key, api_secret):
        print("Making connection to Binance API...")
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = Client(self.api_key, self.api_secret)

    def get_balances(self):
        """ returns a dictionary of all assets and their balance if they are not empty """
        # get JSON object with all account info
        j = self.client.get_account()

        # get the entire balances array
        all_balances = j['balances']
        # dictionary for not-empty balances
        balances = {}

        # get only balances that are not empty
        for balance in all_balances:
            free = float(balance['free']) # free amount of currency
            locked = float(balance['locked'])  # locked amount of currenct

            if free + locked != 0:
                symbol = balance['asset']
                balances[symbol] = free

        return balances

    def get_symbols(self):
        """ returns a list of symbols of the currencies you currently own """
        symbols = []
        # list of non-empty balances
        balances = self.get_balances()

        for b in balances.items():
            symbols.append(b)

        return symbols


    def get_current_price(self, symbol):
        """ Get the current price of a coin on Binance
            and the symbol of the price it is in """

        # TODO this isn't entirely flexible yet
        # BTC gets compared to USD
        # all other currencies to BTC
        if (symbol == 'BTC'):
            price_symbol = 'USDT'
        else:
            price_symbol = 'BTC'

        j = self.client.get_symbol_ticker(symbol=symbol+price_symbol)

        return j['price'], price_symbol

    def get_my_trades(self, symbol, trade_type='all_trades'):
        """ Get up to 500 trades you have made of a specific coin.
            (500 is the API limit)
            Default: returns both buy and sell trades
            trade_type can be 'sell' or 'buy' to only get sell or buy trades
            Returns: list of Trade objects """

        all_trades = self.client.get_my_trades(symbol=symbol)

        # if no type is given, return all trades (buy and sell)
        if trade_type == 'all_trades':
            return self.get_formatted_trades(symbol, all_trades)
        # array for adding either buy or sell trades
        selection = []

        # check for every trade if it is the desired type
        for trade in all_trades:
            # add buy orders if trade_type == 'buy'
            if trade_type == 'buy' and trade['isBuyer']:
                selection.append(trade)
            # add sell orders if trade_type == 'sell'
            if trade_type == 'sell' and not trade['isBuyer']:
                selection.append(trade)

        return self.get_formatted_trades(symbol, selection)

    def get_formatted_trades(self, symbol, trades):
        """ Takes a JSON dictionary and formats the info to a list of Trade objects """
        formatted = []

        for t in trades:
            # determine the type of trade (buy/sell)
            if t['isBuyer']:
                trade_type = 'buy'
            else:
                trade_type = 'sell'

            # create a new Trade object and add it to the list
            trade = Trade(trade_type, symbol, t['price'], t['qty'], t['time'],
                            t['commission'], t['commissionAsset'])
            formatted.append(trade)

        return formatted

    def get_all_trades(self):
        """ Get one long list of every trade for all currencies you own """
        symbols = self.get_symbols()
        combined_symbols = []
        trades = []

        # add the value currency to which the symbols gets compared to
        for s in symbols:
            # TODO this isn't entirely flexible yet
            # BTC gets compared to USD
            # all other currencies to BTC
            if (s == 'BTC'):
                s = 'BTCUSDT'
            else:
                s += 'BTC'

            combined_symbols.append(s)

        # get all trades for the combined symbol
        for s in combined_symbols:
            # add al trades seperately to trades[], not as an array
            for trade in self.get_my_trades(s):
                trades.append(trade)

        return trades
