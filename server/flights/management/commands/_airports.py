import csv
from ...models import Airport, Region, Country


def populate_airports():
    data = []
    with open('flights/data/airports.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:

            try:
                country = Country.objects.get(name=row['country'])

            except Country.DoesNotExist:
                country = None

            region = None

            if row['region'] != r'\N':
                region, _ = Region.objects.get_or_create(name=row['region'].split('/')[0])

            airport = Airport(
                    name=row['name'], code=row['code'] if row['code'] != r'\N' else None,
                    city=row['city'], country=country, region=region
                )

            data.append(airport)

    return len(data)
