from celery import shared_task
from datetime import datetime, date, timedelta
import logging

from .models import Flight,FlightHistory, AirLine, Airport, Preference, Provider
from .fetcher import start
from .fetcher_class import FlightFetcherSmiles


logger = logging.getLogger(__name__)

@shared_task
def say_hello():
    import time
    time.sleep(30)
    print("Hello there!")


# @shared_task
# def process_costs(origin, dest):

#     try:
#         logger.info("Processing costs for %s to %s" % (origin, dest))

#         res = start(origin, dest)
#         origin_airport = Airport.objects.get(code=origin)
#         destin_airport = Airport.objects.get(code=dest)
#         history_flights = []
#         for data in res:

#             logger.debug("Processing [%s -> %s] - %s" % (origin, dest, data['departureDate']))

#             flight, _ = Flight.objects.get_or_create(
#                     airport_origin = origin_airport,
#                     airport_destination = destin_airport,
#                     flight_date = datetime.strptime(data['departureDate'], '%Y-%m-%d')
#                     )

#             flight.external_link = ""
#             flight.save()

#             airline = data['airline']
#             airline_code = airline.get('code').strip().upper()
#             airline_name = airline.get('name').strip().capitalize()

#             airline_o, _ = AirLine.objects.get_or_create(
#                     code=airline_code,
#                     defaults={'name': airline_name}
#                     )

#             h = FlightHistory(money=data['BestPriceMoney'], miles=data['BestPriceMiles'], airline=airline_o, flight=flight)

#             history_flights.append(h)

#         logger.info("Bulking into FlightHistory %s regiters" % (len(history_flights)))
#         FlightHistory.objects.bulk_create(history_flights)

#     except Exception as e:
#         logger.error("Error processing costs for %s to %s" % (origin, dest))
#         logger.error(e)
#         raise e

@shared_task
def fetch(origin, dest, date_flight, provider='SMILES_CLUB'):
    try:
        logger.info("Calling FFS %s->%s(%s)[%s]" % (origin, dest, date_flight, provider))
        fetcher = FlightFetcherSmiles(origin, dest, date_flight, provider=provider, ingestor=True)
        fetcher.start()
    except Exception as e:
        logger.error("FFS %s->%s(%s)[%s]" % (origin, dest, date_flight, provider))
        logger.error(e)
        raise e


@shared_task
def smiles_club_refresher():
    routes = Preference.get_all_routes()
    today = date.today()
    today_next_year = today.replace(year=today.year + 1)
    currentDateStart = today + timedelta(days=1)
    providers = Provider.objects.all()
    for provider in providers:
        currentDate = currentDateStart
        while currentDate < today_next_year:
            for route in routes:
                origin, destin = route
                a_origin = Airport.objects.get(code=origin)
                a_destin = Airport.objects.get(code=destin)
                # Get or Create the Flight
                flight, _ = Flight.objects.get_or_create(
                    origin=a_origin,
                    destination=a_destin,
                    provider=provider,
                    flight_date=currentDate,
                )
                # Schedule task
                fetch.delay(origin, destin, str(currentDate), provider.name)
            # Do next day
            currentDate = currentDate + timedelta(days=1)


# @shared_task
# def smiles_club_refresher():
#     """
#     Generates Flights for today til today+365
#     """
#     preferences = Preference.objects.all()
#     routes = set([p.get_routes() for p in preferences])
    # try:
    #     logger.info("Calling FFS %s->%s(%s)[%s]" % (origin, dest, date, provider))
    #     fetcher = FlightFetcherSmiles(origin, dest, date, provider=provider, ingestor=True)
    #     fetcher.start()
    # except Exception as e:
    #     logger.error("FFS %s->%s(%s)[%s]" % (origin, dest, date, provider))
    #     logger.error(e)
    #     raise e
