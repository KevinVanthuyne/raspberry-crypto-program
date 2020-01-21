
class Coin():
    """Class to contain all information about a specific crypto currency"""

    def __init__(self, json, currency):
        """ Create a coin from a JSON string of the CoinMarketCap API """

        if self.is_valid_currency(currency):
            currency = currency.lower()

            # convert all JSON info to object variables
            self.id = json['id']
            self.name = json['name']
            self.symbol = json['symbol']
            self.rank = json['rank']
            self.price = json['price_{}'.format(currency)]
            self.price_btc = json['price_btc']
            self.volume_24h = json['24h_volume_{}'.format(currency)]
            self.market_cap = json['market_cap_{}'.format(currency)]
            self.available_supply = json['available_supply']
            self.total_supply = json['total_supply']
            self.max_supply = json['max_supply']
            self.percent_change_1h = self.get_percent_formatted(json['percent_change_1h'])
            self.percent_change_24h = self.get_percent_formatted(json['percent_change_24h'])
            self.percent_change_7d = self.get_percent_formatted(json['percent_change_7d'])

        else:
            print("Invalid currency to convert to")

    def get_price(self):
        # returns the first 5 numbers of the price as a string
        return str(self.price)[:5]

    def get_percent_formatted(self, percent):
        """ add a + to the percentage when it's positive """
        if float(percent) > 0:
            return "+{}".format(percent)
        return percent

    def is_valid_currency(self, currency):
        valid = ["AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK", "EUR",
                "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN",
                "MYR", "NOK", "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD",
                "THB", "TRY", "TWD", "ZAR"]

        return currency.upper() in valid

    def get_info(self):
        return "{} €{} {}%".format(self.symbol, self.get_price(), self.percent_change_24h)
