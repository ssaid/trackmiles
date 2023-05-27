from datetime import datetime, date, timedelta
import concurrent.futures
import requests
import jq
import traceback
import time


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
        print(currentDate)
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

    try:
        price = jq.jq('.requestedFlightSegmentList[].bestPricing.miles').transform(response_json)
    except Exception:
        print('Unable to parse response...')
        return {}

    dd = {
        'originAirportCode': data['originAirportCode'],
        'destinationAirportCode': data['destinationAirportCode'],
        'departureDate': data['departureDate'],
        'api_req': url,
        'best_price': price,
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
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=33)

    # Submit API requests to the executor
    futures = [executor.submit(make_api_request, data) for data in queue]

    # Retrieve the results of the completed requests locked until all futures are completed
    results = [future.result() for future in concurrent.futures.as_completed(futures)]

    # Filter results to exclude empty dicts
    results = filter(None, results)
    results = filter(lambda x: x.get('best_price'), results)
    print(f'Requests: #{len(futures)}')

    sorted_prices = sorted(results, key=lambda x: x.get('best_price', 1000000))
    print(f'Responss: #{len(sorted_prices)}')

    print('Get the best price...')
    if sorted_prices:
        print(sorted_prices[0])
    # # Process the results
    # for result in results:
    #     # Handle each API response as desired
    #     print(result)


def main(mode='TEST'):
    if mode == 'TEST':
        queue = gen_tasks()
    else:
        raise NotImplementedError()
    queue_processor(queue)


if __name__ == "__main__":
    main()
