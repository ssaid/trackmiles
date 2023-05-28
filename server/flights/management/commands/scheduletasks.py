from django.core.management.base import BaseCommand, CommandError

from django_celery_beat.models import ClockedSchedule, PeriodicTask, IntervalSchedule
from django.utils.timezone import make_aware
import pytz
from flights.models import Airport
import datetime
import json

class Command(BaseCommand):
    help = 'Create schedules for flights'

    def handle(self, *args, **options):

        o_airports = (
                "EZE",
                )

        d_airports = (
                "MEX",
                "LIM",
                )

        today = datetime.date.today()
        start_schedules_at = datetime.datetime(today.year, today.month, today.day, 22, 0, 0)
        i_between_schedules = datetime.timedelta(minutes=2)

        time = start_schedules_at
        day_schedule, _ = IntervalSchedule.objects.get_or_create(
                every=1,
                period=IntervalSchedule.DAYS,
                )
        scheduled = 0
        for o in Airport.objects.filter(code__in=o_airports):
            for d in Airport.objects.filter(code__in=d_airports):

                time_aware = make_aware(time, timezone=pytz.timezone('UTC'))
                clock, _ = ClockedSchedule.objects.get_or_create(
                    clocked_time=time_aware,
                    )

                PeriodicTask.objects.get_or_create(
                    name=f"Process costs from {o.code} to {d.code}",
                    task="flights.tasks.process_costs",
                    start_time=time_aware,
                    interval=day_schedule,
                    kwargs=json.dumps({"origin": o.code, "dest": d.code}),
                    )

                time += i_between_schedules
                scheduled += 1

        self.stdout.write(self.style.SUCCESS('Successfully scheduled %s tasks' % scheduled))
