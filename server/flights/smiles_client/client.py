import requests


class Client:

    _base_url = 'https://api-air-flightsearch-prd.smiles.com.br/v1/airlines/search'

    def get_flights(self, params):
        today = __import__('datetime').datetime.today().strftime('%Y-%m-%d')
        params = {
            'adults': 1,
            'cabinType': 'all',
            'children': 0,
            'currencyCode': "ARS",
            'departureDate': today,
            'destinationAirportCode': 'MEX',
            'infants': 0,
            'isFlexibleDateChecked': False,
            'originAirportCode': 'EZE',
            'tripType': '2',
            'forceCongener': True,
            'r': 'ar',
        }

        res = requests.get(self._base_url, params=params)
        return res




""" TODO: Emulate the following curl request with requests library

query params:
    search?
    adults=1
    & cabinType=all
    & children=0
    & currencyCode=ARS
    & departureDate=2023-04-18
    & destinationAirportCode=MEX
    & infants=0
    & isFlexibleDateChecked=false
    & originAirportCode=EZE
    & tripType=2
    & forceCongener=true
    & r=ar

curl 'https://api-air-flightsearch-prd.smiles.com.br/v1/airlines/search?adults=1&cabinType=all&children=0&currencyCode=ARS&departureDate=2023-04-18&destinationAirportCode=MEX&infants=0&isFlexibleDateChecked=false&originAirportCode=EZE&tripType=2&forceCongener=true&r=ar' \
        -H 'authority: api-air-flightsearch-prd.smiles.com.br' \
        -H 'accept: application/json, text/plain, /' \
        -H 'accept-language: en-US,en;q=0.9' \
        -H 'authorization: Bearer 0MW366WE8AbparaTzZdGmZKI7QGa7UXMp0lxV3CzOpMUUI72mRaguJ' \
        -H 'cache-control: no-cache' \
        -H 'channel: Web' \
        -H 'language: es-ES' \
        -H 'origin: https://www.smiles.com.ar/' \
        -H 'pragma: no-cache' \
        -H 'referer: https://www.smiles.com.ar/' \
        -H 'region: ARGENTINA' \
        -H 'sec-ch-ua: "Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"' \
        -H 'sec-ch-ua-mobile: ?0' \
        -H 'sec-ch-ua-platform: "Linux"' \
        -H 'sec-fetch-dest: empty' \
        -H 'sec-fetch-mode: cors' \
        -H 'sec-fetch-site: cross-site' \
        -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36' \
        -H 'x-api-key: aJqPU7xNHl9qN3NVZnPaJ208aPo2Bh2p2ZV844tw' \
        --compressed
          | jq

"""
