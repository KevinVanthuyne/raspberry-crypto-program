class Trade():
    """ A class for containing the information about a trade """

    def __init__(self, trade_type, symbol, price, amount, time, commission, commission_asset):
        self.type = trade_type  # 'buy' or 'sell'
        self.symbol = symbol  # symbol of the coin that was bought or sold
        self.price = float(price)  # price per unit of the coin
        self.amount = float(amount)  # total amount bought or sold
        self.time = time  # Binance timestamp of the trade
        self.commission = float(commission)  # amount of commision payed on trade
        self.commission_asset = commission_asset  # what coin commission was payed with

    def __str__(self):
        price_com = self.format_float(self.get_price_with_commission())
        what_symbol, for_symbol = self.get_split_symbols()
        return "[{}] {}: {} {} - {}".format(self.type, what_symbol, price_com, for_symbol, self.amount)

    def get_price_with_commission(self):
        """ Returns the price per coin with commission deducted """
        actual_price_per_coin = -1.0

        # if the trade is a buy order, some of the bought currency is used as a commission
        # buying a coin is thus actually slightly more expensive
        # for example: when 1000 TRX is bought, 1 TRX is deducted as commission
        # so in fact you have only bought 999 TRX for the price of 1000 TRX
        if self.type == 'buy':
            total_price = self.price * self.amount
            actual_price_per_coin = total_price / (self.amount - self.commission)

        # if the trade is a sell order, some of the profit is deducted
        # for example: 10000 TRX is sold for 1 BTC, but 0.001 BTC is deducted
        if self.type == 'sell':
             total_price = self.price * self.amount
             actual_price_per_coin = (total_price - self.commission) / self.amount

        return actual_price_per_coin

    def format_float(self, float_number):
        """ formats a float to a string without using scientific notation """
        return '{:.8f}'.format(float_number)

    def get_split_symbols(self):
        """ splits the combined symbol in the bought/sold coin symbol
            and the bought with/sold for symbol.
            Example:    LTCBTC -> LTC, BTC
                        QTUMBTC -> QTUM, BTC
                        BTCUSDT -> BTC, USDT """

        # if the trade is a buy type, the bought symbol = the commission symbol
        if self.type == 'buy':
            bought = self.commission_asset
            bought_with = self.symbol.split(bought)[1]
            return bought, bought_with

        # if the trade was a sell, the sold for symbol = the commission symbol
        if self.type == 'sell':
            sold_for = self.commission_asset
            sold = self.symbol.split(sold_for)[0]
            return sold, sold_for
