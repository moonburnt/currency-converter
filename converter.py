import logging
import urllib.request as ur
import json

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(fmt='[%(asctime)s][%(name)s][%(levelname)s] %(message)s', datefmt='%H:%M:%S'))
log.addHandler(handler)

class Converter:
    '''Class with functions to convert currencies'''
    def __init__(self):
        self.api = 'https://api.exchangeratesapi.io/latest'

    def get_rates(self, currency):
        '''Getting conversion rates from json api. Receives str(name of currency). Returns python dictionary'''
        url = f"{self.api}?base={currency}"
        log.debug(f"Url is {url}")

        log.debug(f"Fetching {currency} exchange rates from {self.api}")
        response = ur.urlopen(url)

        data = response.read()
        log.debug(f"Got following data: {data}, converting to python dictionary")

        pydic = json.loads(data)
        log.debug(f"Got dictionary: {pydic}, returning")

        return pydic

    def find_price(self, rates, currency):
        '''Receives dic(conversion rates), str(name of currency), returns float(price of that currency)'''

        log.debug(f"Attempting to find price of {currency} in {rates}")
        for item in rates:
            log.debug(f"Processing {item}")
            if item == currency:
                log.debug(f"{item} matches our desired currency!")
                price = float(rates[item])
                log.debug(f"Price of {currency} is {price}!")
                break

        return price

    def convert(self, original_currency, converted_currency, amount):
        '''Receives str(name of currency you want to convert from), str(name of currency to convert to, int/float(amount). Returns price of received amount of original currency in converted currency'''

        amount = float(amount)

        log.info(f"Attempting to convert {amount} {original_currency} to {converted_currency}")
        log.debug(f"Getting conversion rates")
        raw_prices = self.get_rates(original_currency)
        prices = raw_prices['rates']
        log.debug(f"Cleaned up prices dictionary is {prices}")
        log.debug(f"Finding currency's price")
        currency_price = self.find_price(prices, converted_currency)
        log.debug(f"Price of {original_currency} is {currency_price} {converted_currency}")
        log.debug(f"Calculating price per provided amount")
        result_price = amount * currency_price
        log.info(f"Price of {amount} {original_currency} is {result_price} {converted_currency}")

        return result_price
