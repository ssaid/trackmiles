from django.core.management.base import BaseCommand, CommandError

from flights.models import Preference
from ...utils.schedule_trace import schedule_trace

class Command(BaseCommand):
    help = 'Create schedules for flights'

    def handle(self, *args, **options):

        routes = {(o, d) for p in Preference.objects.all() for o, d in p.get_routes()}
        scheduled = 0
        for o, d in routes:
            if schedule_trace(o, d):
                scheduled += 1

        self.stdout.write(self.style.SUCCESS('Successfully scheduled %s tasks' % scheduled))
