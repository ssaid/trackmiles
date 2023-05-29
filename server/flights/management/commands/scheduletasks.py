from django.core.management.base import BaseCommand, CommandError

from django_celery_beat.models import ClockedSchedule, PeriodicTask, IntervalSchedule
from django.utils.timezone import make_aware
import pytz
from flights.models import Airport, Preference
import datetime
import json

class Command(BaseCommand):
    help = 'Create schedules for flights'

    def handle(self, *args, **options):
        today = datetime.date.today()
        start_schedules_at = datetime.datetime(today.year, today.month, today.day, 0, 0, 0)
        i_between_schedules = datetime.timedelta(minutes=0)

        time = start_schedules_at
        day_schedule, _ = IntervalSchedule.objects.get_or_create(
                every=1,
                period=IntervalSchedule.DAYS,
                )
        scheduled = 0
        routes = {(o, d) for p in Preference.objects.all() for o, d in p.get_routes()}
        for o, d in routes:
            time_aware = make_aware(time, timezone=pytz.timezone('UTC'))
            clock, _ = ClockedSchedule.objects.get_or_create(
                clocked_time=time_aware,
                )

            PeriodicTask.objects.get_or_create(
                name=f"Process costs from {o} to {d}",
                task="flights.tasks.process_costs",
                interval=day_schedule,
                kwargs=json.dumps({"origin": o, "dest": d}),
                defaults={
                    'start_time': time_aware,
                },
            )

            time += i_between_schedules
            scheduled += 1

        self.stdout.write(self.style.SUCCESS('Successfully scheduled %s tasks' % scheduled))
