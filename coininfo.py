import requests
import json

from coin import Coin

class CoinInfo():
    """Class for getting all necessary information about a list of crypto currencies"""

    def __init__(self, currency):
        self.currency = currency  # The currency to show prices in (EUR/ GBP/...)

    def get_coin(self, id):
        """ get the corresponding Coin object from the CoinMarketCap id """

        # get JSON string from CoinMarketCap API of specific coin
        json_string = requests.get('https://api.coinmarketcap.com/v1/ticker/{}/?convert={}'.format(id, self.currency))
        # load JSON object from the string
        json_object = json.loads(json_string.text)

        try:
            return Coin(json_object[0], self.currency)
        except KeyError:
            return None

    def get_coins(self, coin_ids):
        """ returns the corresponding Coin objects of the given list of coin id's
            if all coin id's are valid. If one id is invalid, returns None """
        coins = []

        # get a Coin object for every given id
        for id in coin_ids:
            coin = self.get_coin(id)

            # if the coin id could be found
            if coin is not None:
                coins.append(coin)
            # if the coin id could not be found
            else:
                print("Invalid coin id: {}".format(id))
                return None

        return coins
