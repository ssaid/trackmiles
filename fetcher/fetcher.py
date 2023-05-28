from datetime import datetime, date, timedelta
import concurrent.futures
import requests
import jq
import traceback
import time


def parse_data(json_response):
    """
{'uid': 'syu6wop9a6',
 'stops': 2,
 'cabin': 'ECONOMIC',
 'availableSeats': 9,
 'departureDate': '2023-10-01T12:20:00',
 'arrivalDate': '2023-10-02T14:30:00',
 'airline': {'code': 'AC', 'name': 'AIR CANADA'},
 'baggage': {'free': 'true', 'quantity': 1, 'code': 'N'},
 'duration': 2310,
 'fare_type': 'SMILES_CLUB',
 'congener': {'fareReference': 'TLYA02TG/KLZT72TG',
  'fareInfo': 'RP',
  'negotiatedFareCode': None},
 'type': 'SMILES_CLUB',
 'baseMiles': 350000,
 'money': 0,
 'miles': 330900,
 'airlineFareAmount': '4780.87',
 'airlineFare': 0,
 'airlineTax': 2507.46,
 'legListCost': '',
 'legListCurrency': 'BRL',
 'marginRecalc': None,
 'recalculate': False}
    """
    flights = []
    bestPricing = json_response['bestPricing']
    flightList = json_response['flightList']
    for flight in flightList:
        for fare in flight['fareList']:
            dd = {
                'uid': flight['uid'],
                'stops': flight['stops'],
                'cabin': flight['cabin'],
                'availableSeats': flight['availableSeats'],
                'departureDate': flight['departure']['date'],
                'arrivalDate': flight['arrival']['date'],
                'airline': flight['airline'],
                'baggage': flight['baggage'],
                'duration': flight['durationNumber'],
                'fare_type': fare['type'],
                **fare
            }
            flights.append(dd)

    # Get best price
    type_of_fare = bestPricing['fare']['type']
    qty_of_miles = bestPricing['miles']
    res = next((fare for fare in flights if fare['type'] == type_of_fare and fare['miles'] == qty_of_miles), {})
    return res


def gen_tasks(afrom='EZE', adest='MEX'):
    """ Generate a list of 365 tasks for the given source and destination"""
    res = []
    today = date.today()
    today_next_year = today.replace(year=today.year + 1)
    currentDate = today + timedelta(days=1)
    while currentDate < today_next_year:
        dd = {
            'originAirportCode': afrom,
            'destinationAirportCode': adest,
            'departureDate': currentDate.strftime('%Y-%m-%d'),
        }
        res.append(dd)
        currentDate = currentDate + timedelta(days=1)
    return res


def make_api_request(data):
    ddata = build_request(data)
    # Extract necessary data from the dictionary
    url = ddata['url']
    method = ddata['method']
    headers = ddata['headers']
    payload = ddata['payload']

    # Make the API request
    print(f"Requesting [{data['originAirportCode']}->{data['destinationAirportCode']}] @ {data['departureDate']}")
    done = False
    retry = 0
    max_retry = 3
    while not done and retry < max_retry:
        try:
            response = requests.request(method, url, headers=headers, json=payload)
            response.raise_for_status()
            response_json = response.json()
        except Exception:
            traceback.print_exc()
            print(f'Retrying #{retry + 1}/{max_retry}')
            time.sleep(5)
            retry += 1
        else:
            done = True

    if not done:
        print('Max Retries exceeded, returning empty')
        return {}

    response_json_flights = jq.jq('.requestedFlightSegmentList[]').transform(response_json)

    data_parsed = parse_data(response_json_flights)

    dd = {
        'originAirportCode': data['originAirportCode'],
        'destinationAirportCode': data['destinationAirportCode'],
        'departureDate': data['departureDate'],
        'api_req': url,
        'BestPriceMiles': data_parsed['miles'],
        'BestPriceMoney': data_parsed['money'],
        'airline': data_parsed['airline'],
        'url': f"https://www.smiles.com.ar/emission?originAirportCode={data['originAirportCode']}&destinationAirportCode={data['destinationAirportCode']}&departureDate=1696129200000&adults=1&children=0&infants=0&isFlexibleDateChecked=false&tripType=2&cabinType=all&currencyCode=BRL"
    }

    return dd


URL_SINGLE = 'https://api-air-flightsearch-prd.smiles.com.br/v1/airlines/search?adults=1&cabinType=all&children=0&currencyCode=ARS&departureDate={departureDate}&destinationAirportCode={destinationAirportCode}&infants=0&isFlexibleDateChecked=false&originAirportCode={originAirportCode}&tripType=2&forceCongener=false&r=ar'


def build_request(data, url=URL_SINGLE):
    url_ready = URL_SINGLE.format(**data)
    request_data = {
        'url': url_ready,
        'headers': {
            'x-api-key': 'aJqPU7xNHl9qN3NVZnPaJ208aPo2Bh2p2ZV844tw'
        },
        'payload': None,
        'method': 'GET',
    }
    return request_data


def queue_processor(queue=[]):
    # Create a thread or process pool based on the number of requests you want to perform in parallel
    # By default, the ThreadPoolExecutor is used for threads, and ProcessPoolExecutor for processes.
    # You can specify the number of workers as an argument to the executor (e.g., max_workers=5)
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=12)

    # Submit API requests to the executor
    futures = [executor.submit(make_api_request, data) for data in queue[:10]]

    # Retrieve the results of the completed requests locked until all futures are completed
    results = [future.result() for future in concurrent.futures.as_completed(futures)]

    # Filter results to exclude empty dicts
    results = filter(None, results)
    results = filter(lambda x: x.get('BestPriceMiles'), results)
    print(f'Requests: #{len(futures)}')

    sorted_prices = sorted(results, key=lambda x: x.get('BestPriceMiles', 1000000))
    print(f'Responss: #{len(sorted_prices)}')

    print('Getting the best price...')

    if sorted_prices:
        print(sorted_prices[0])

    return sorted_prices


def start(origin, destination):
    print('Start')
    queue = gen_tasks(afrom=origin, adest=destination)
    res = queue_processor(queue)
    print('Success')
    return res


def main(mode='TEST'):
    if mode == 'TEST':
        queue = gen_tasks()
    else:
        raise NotImplementedError()
    queue_processor(queue)


if __name__ == "__main__":
    main()


