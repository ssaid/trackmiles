from server.celery import app
from celery import shared_task


@shared_task
def say_hello(origin, destination):
    print("Hello there!")



    # llamo a la funcion que hace el fetch

    # Airport(name="test", city="test", country="test", iata="test", icao="test", latitude=0, longitude=0, altitude=0, timezone=0, dst="test", tz="test", type="test", source="test").save()
    


