from datetime import datetime, date, timedelta
import concurrent.futures
import requests
import traceback
import time
import os


class FlightFetcherSmiles():
    def __init__(self, origin, destination, fdate, ingestor=None, provider='SMILES'):
        self._origin = origin
        self._destination = destination
        self._date = fdate
        self._ingestor = ingestor
        self._provider = provider
        self._max_retries = 3
        self._retries = 0
        self._data_flight = {}
        self._data_flight_cost = {}
        self._best_flight = {}
        self._data = {}
        self._data_fare_uid = None

    def start(self):
        self.do_request_flight()
        self._best_flight = self.get_best_flight()
        self.do_request_cost()
        self.build_data()
        self.finish()

    def _build_buy_url(self):
        url_tmpl = "https://www.smiles.com.ar/emission?originAirportCode=EZE&destinationAirportCode=MEX&departureDate={depDate}&adults=1&infants=0&children=0&cabinType=all&tripType=2"
        date_dt = datetime.strptime(self._date, '%Y-%m-%d')
        tmst_ms = int(date_dt.timestamp() * 1000)
        url = url_tmpl.format(depDate=tmst_ms)
        return url

    def build_data(self):
        # Taxes
        total_tax_money = self._data_flight_cost["totals"]["totalBoardingTax"]["money"]
        total_tax_miles = self._data_flight_cost["totals"]["totalBoardingTax"]["miles"]
        # Amount total in miles
        total_flight_and_tax_miles = self._data_flight_cost["totals"]["total"]["miles"]
        # Base fare on the airline
        airline_fare_amount_wo_tax = self._data_flight_cost['flightList'][0]['airlineFlightMoney']
        # Total in money
        total_flight_and_tax_money = airline_fare_amount_wo_tax + total_tax_money
        # Generic Data
        airline_code = self._best_flight['airline']['code']
        airline_name = self._best_flight['airline']['name']
        seats = self._best_flight['availableSeats']
        stops = self._best_flight['stops']
        baggage = self._best_flight['baggage']
        if baggage['quantity']:
            baggage = True
        else:
            baggage = False
        buy_url = self._build_buy_url()

        self._data = {
            'miles': total_flight_and_tax_miles,
            'money': total_flight_and_tax_money,
            'tax_miles': total_tax_miles,
            'tax_money': total_tax_money,
            'fare_clean': airline_fare_amount_wo_tax,
            'departure_date': self._date,
            'airline_code': airline_code,
            'airline_name': airline_name,
            'seats': seats,
            'stops': stops,
            'baggage': baggage,
            'provider': self._provider,
            'external_link': buy_url,
            'origin_code': self._origin,
            'destination_code': self._destination,
        }

    def notify_ingestor(self, data):
        retry = 0
        max_retries = 100
        done = False
        method = 'POST'
        url = os.environ.get('INGEST_HOST') or self._ingestor
        key = os.environ.get('INGEST_KEY')
        headers = {
            'INGEST_KEY': key,
        }
        while not done and retry < max_retries:
            try:
                response = requests.request(method, url, headers=headers, json=data)
                response.raise_for_status()
                # response_json = response.json()
            except Exception:
                traceback.print_exc()
                print(f'Retrying #{retry + 1}/{self._max_retries}')
                time.sleep(5)
                retry += 1
            else:
                done = True
                print('Ingestor Notified, bye!')

    def finish(self):
        if self._ingestor:
            self.notify_ingestor(self._data)
        else:
            print(f'{self._origin} -> {self._destination} for {self._provider}')
            import pprint; pprint.pprint(self._data)

    def get_api_key(self):
        API_KEY = 'aJqPU7xNHl9qN3NVZnPaJ208aPo2Bh2p2ZV844tw'
        return API_KEY

    def failed(self, reason):
        reason = f"FetcherFailed({self._origin}>{self._destination}@{self._date}/{self._provider}): {reason}"
        if self._ingestor:
            self.notify_ingestor({'reason': reason, 'exception': True})
        raise Exception(f'FetcherFailed({self._origin}>{self._destination}@{self._date}/{self._provider}): {reason}')

    def get_best_flight(self):
        if not self._data_flight:
            print('No data of flights, call the API first(do_request_flight)')
            return None
        flights = []
        if len(self._data_flight['requestedFlightSegmentList']) > 1:
            self.failed('requestedFlightSegmentList lenght > 1: Not Implemented')
        # bestPricing = self._data_flight['requestedFlightSegmentList'][0]['bestPricing']
        flightList = self._data_flight['requestedFlightSegmentList'][0]['flightList']
        for flight in flightList:
            for fare in flight['fareList']:
                if fare['type'] != self._provider:
                    continue
                # if flight["isAirlineTaxWithFlight"]:
                #     tax_amount = fare['airlineTax'] - flight['airlineTax']
                # else:
                #     tax_amount = fare['airlineTax']
                dd = {
                    'flight_uid': flight['uid'],
                    'stops': flight['stops'],
                    'cabin': flight['cabin'],
                    'availableSeats': flight['availableSeats'],
                    'departureDate': flight['departure']['date'],
                    'arrivalDate': flight['arrival']['date'],
                    'airline': flight['airline'],
                    'baggage': flight['baggage'],
                    'duration': flight['durationNumber'],
                    'fare_type': fare['type'],
                    'fare_uid': fare['uid'],
                    'base_amount_money': flight['airlineFlightMoney'],
                    # 'tax_amount': tax_amount,
                    # 'airport_origin': {
                    #     'name': fare['departure']['airport']['name'],
                    #     'code': fare['departure']['airport']['code'],
                    # },
                    # 'airport_destin': {
                    #     'name': fare['arrival']['airport']['name'],
                    #     'code': fare['arrival']['airport']['code'],
                    # },
                    **fare,
                }
                flights.append(dd)
        # return flights
        # Get best price
        # type_of_fare = bestPricing['fare']['type']
        # qty_of_miles = bestPricing['miles']
        # res = next((fare for fare in flights if fare['type'] == type_of_fare and fare['miles'] == qty_of_miles), {})
        best_price_found = sorted(flights, key=lambda x: x["miles"])[0]
        return best_price_found

    def do_request_flight(self):
        ddata = self.build_request_flight()
        # Extract necessary data from the dictionary
        url = ddata['url']
        method = ddata['method']
        headers = ddata['headers']
        payload = ddata['payload']

        # Make the API request
        print(f"Requesting Flights [{self._origin}->{self._destination}] @ {self._date} for {self._provider}")
        done = False
        retry = 0
        while not done and retry < self._max_retries:
            try:
                response = requests.request(method, url, headers=headers, json=payload)
                response.raise_for_status()
                response_json = response.json()
            except Exception:
                traceback.print_exc()
                print(f'Retrying #{retry + 1}/{self._max_retries}')
                time.sleep(5)
                retry += 1
            else:
                done = True

        if not done:
            self.failed('Max Retries exceeded: No data.')

        if not response_json['requestedFlightSegmentList'][0]['flightList']:
            self.failed('No data found in Smiles.')

        print(response_json)
        self._data_flight = response_json

    def do_request_cost(self):
        ddata = self.build_request_cost()
        # Extract necessary data from the dictionary
        url = ddata['url']
        method = ddata['method']
        headers = ddata['headers']
        payload = ddata['payload']

        # Make the API request
        print(f"Requesting Costs [{self._origin}->{self._destination}] @ {self._date} for {self._provider}")
        done = False
        retry = 0
        while not done and retry < self._max_retries:
            try:
                response = requests.request(method, url, headers=headers, json=payload)
                response.raise_for_status()
                response_json = response.json()
            except Exception:
                traceback.print_exc()
                print(f'Retrying #{retry + 1}/{self._max_retries}')
                time.sleep(5)
                retry += 1
            else:
                done = True

        if not done:
            self.failed('Max Retries exceeded: No data.')

        self._data_flight_cost = response_json

    def parse_response_flight(self):
        pass

    def parse_response_cost(self):
        pass

    def build_request_flight(self):
        URL_SINGLE = 'https://api-air-flightsearch-prd.smiles.com.br/v1/airlines/search?adults=1&cabinType=all&children=0&currencyCode=ARS&departureDate={departureDate}&destinationAirportCode={destinationAirportCode}&infants=0&isFlexibleDateChecked=false&originAirportCode={originAirportCode}&tripType=2&forceCongener=false&r=ar'
        data = {
            'departureDate': self._date,
            'originAirportCode': self._origin,
            'destinationAirportCode': self._destination
        }
        url_ready = URL_SINGLE.format(**data)
        request_data = {
            'url': url_ready,
            'headers': {
                'x-api-key': self.get_api_key(),
                'region': 'ARGENTINA'
            },
            'payload': None,
            'method': 'GET',
        }
        return request_data

    def build_request_cost(self):
        if not self._best_flight:
            self.failed('No _best_flight to calculate costs')
            # raise Exception('Not available if not fareId')

        URL_SINGLE = 'https://api-airlines-boarding-tax-prd.smiles.com.br/v1/airlines/flight/boardingtax?adults=1&children=0&infants=0&fareuid={fareUid}&uid={uid}&type=SEGMENT_1&highlightText=SMILES'
        data = {
            'fareUid': self._best_flight['fare_uid'],
            'uid': self._best_flight['flight_uid'],
        }
        url_ready = URL_SINGLE.format(**data)
        request_data = {
            'url': url_ready,
            'headers': {
                'x-api-key': self.get_api_key(),
                'region': 'ARGENTINA'
            },
            'payload': None,
            'method': 'GET',
        }
        return request_data

    def inform_endpoint(self):
        pass

    def inform_endpoint_error(self):
        """ If _retries > _max_retries inform endpoint of that error """
        pass