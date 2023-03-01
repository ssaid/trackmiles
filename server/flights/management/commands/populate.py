from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Populates the database with some initial data'

    def handle(self, *args, **options):

        from ._countries import populate_countries

        populated = populate_countries()
        self.stdout.write(self.style.SUCCESS('Successfully populated %s countries' % populated))

        from ._airports import populate_airports

        populated = populate_airports()
        self.stdout.write(self.style.SUCCESS('Successfully populated %s airports' % populated))
