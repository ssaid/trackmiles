
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.utils.timezone import make_aware
import pytz
import datetime
import json


def schedule_trace(origin, dest):

    today = datetime.date.today()
    start_schedule_at = datetime.datetime(today.year, today.month, today.day, 0, 0, 0)

    time_aware = make_aware(start_schedule_at, timezone=pytz.timezone('UTC'))

    day_schedule, _ = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.DAYS,
            )

    _, created = PeriodicTask.objects.get_or_create(
        name=f"Process costs from {origin} to {dest}",
        task="flights.tasks.process_costs",
        interval=day_schedule,
        kwargs=json.dumps({"origin": origin, "dest": dest}),
        defaults={
            'start_time': time_aware,
        },
    )

    return created
