from django.db.models.signals import post_save
from django.dispatch import receiver
from flights import fetcher
from flights.models import Flight, Preference
from flights.tasks import process_costs
from .utils.schedule_trace import schedule_trace
import logging


logger = logging.getLogger(__name__)


@receiver(post_save, sender=Preference, dispatch_uid="schedule_trace")
def create_task(sender, instance, created, **kwargs):

    if created:
        logger.info("Preference for route user %s created" % instance.user.email)
        routes = instance.get_routes()
        for origin, dest in routes:
            if not Flight.objects.filter(airport_origin__code=origin, airport_destination__code=dest).exists():
                logger.info("Data for [%s -> %s] not found. Scheduling task for this route" % (origin, dest))
                process_costs.delay(origin, dest)
                schedule_trace(origin, dest)
