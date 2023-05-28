from celery import shared_task
from .models import Flight, FlightDetail, FlightHistory, AirLine, Airport
from .fetcher import start


@shared_task
def say_hello():
    import time
    time.sleep(30)
    print("Hello there!")


@shared_task
def process_costs(origin, dest):
    res = start(origin, dest)
    # origin_airport_code = res['airport_origin']['code'].upper().strip()
    # origin_airport_name = res['airport_origin']['name'].capitalize().strip()
    # destin_airport_code = res['airport_destin']['code'].upper().strip()
    # destin_airport_name = res['airport_destin']['name'].capitalize().strip()
    origin_airport = Airport.objects.get(code=origin)
    destin_airport = Airport.objects.get(code=dest)
    flight = Flight.objects.get_or_create(airport_origin = origin_airport, airport_destination = destin_airport)
    history_flights = []
    for data in res:
        fd = FlightDetail.objects.get_or_create(flight_id=flight.pk, flight_date=data['departureDate'])

        airline = data['airline']
        airline_code= airline.get('code').strip().upper()
        airline_name= airline.get('name').strip().capitalize()

        airline_o = AirLine.objects.get_or_create(code=airline_code, defaults={'name': airline_name})
        h = FlightHistory(money=data['money'], miles=data['miles'], airline=airline_o, detail=fd)

        history_flights.append(h)

    FlightHistory.objects.bulk_create(history_flights)
