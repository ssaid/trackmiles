from server.celery import app
from celery import shared_task
from .models import Flight, FlightDetail, FlightHistory, AirLine


@shared_task
def say_hello():
    import time
    time.sleep(30)
    print("Hello there!")


@shared_tasks
def process_costs(origin, dest):
    res = fetcher(origin, dest)
    flight = Flight.objects.get('airport_origin__code' = origin, 'airport_destination__code' = dest)
    history_flights = []
    for data in res:
        fd = FlightDetail.objects.get_or_create('flight_id'=flight.pk, 'flight_date'=res['departureDate'])
        airline = data['airline']
        airline_code= airline.get('code').strip().upper()
        airline_name= airline.get('name').strip().capitalize()
        airline_o = AirLine.objects.get_or_create(code=airline_code, defaults={'name': airline_name})
        history = FlightHistory(money=data['money'], miles=data['miles'], airline=airline_o, detail=fd)
        history_flights.append(history)
    FlightHistory.objects.bulk_create(history_flights)
