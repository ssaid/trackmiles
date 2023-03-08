import csv
from ...models import Airport, Region, Country


def populate_airports():
    data = []
    country_cache = {}
    region_cache = {}
    with open('flights/data/airports.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:

            if row['country'] in country_cache:
                country = country_cache[row['country']]
            else:

                try:
                    country = Country.objects.get(name=row['country'])
                except Country.DoesNotExist:
                    country = None
                country_cache[row['country']] = country


            region = None

            if row['region'] in region_cache:
                region = region_cache[row['region']]
            else:
                if row['region'] != r'\N':
                    region, _ = Region.objects.get_or_create(name=row['region'].split('/')[0])
                    region_cache[row['region']] = region

            airport = Airport(
                    name=row['name'], code=row['code'] if row['code'] != r'\N' else None,
                    city=row['city'], country=country, region=region
                )

            data.append(airport)

    Airport.objects.bulk_create(data)

    return len(data)
