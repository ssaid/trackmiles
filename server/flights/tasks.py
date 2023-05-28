from celery import shared_task
from datetime import datetime
import logging

from .models import Flight,FlightHistory, AirLine, Airport
from .fetcher import start


logger = logging.getLogger(__name__)

@shared_task
def say_hello():
    import time
    time.sleep(30)
    print("Hello there!")


@shared_task
def process_costs(origin, dest):

    try:
        logger.info("Processing costs for %s to %s" % (origin, dest))

        res = start(origin, dest)
        origin_airport = Airport.objects.get(code=origin)
        destin_airport = Airport.objects.get(code=dest)
        history_flights = []
        for data in res:

            logger.debug("Processing [%s -> %s] - %s" % (origin, dest, data['departureDate']))

            flight, _ = Flight.objects.get_or_create(
                    airport_origin = origin_airport,
                    airport_destination = destin_airport,
                    flight_date = datetime.strptime(data['departureDate'], '%Y-%m-%d')
                    )

            flight.external_link = ""
            flight.save()

            airline = data['airline']
            airline_code = airline.get('code').strip().upper()
            airline_name = airline.get('name').strip().capitalize()

            airline_o, _ = AirLine.objects.get_or_create(
                    code=airline_code,
                    defaults={'name': airline_name}
                    )

            h = FlightHistory(money=data['BestPriceMoney'], miles=data['BestPriceMiles'], airline=airline_o, flight=flight)

            history_flights.append(h)

        logger.info("Bulking into FlightHistory %s regiters" % (len(history_flights)))
        FlightHistory.objects.bulk_create(history_flights)

    except Exception as e:
        logger.error("Error processing costs for %s to %s" % (origin, dest))
        logger.error(e)
        raise e
