import csv
from ...models import Country


def populate_countries():
    data = []
    with open('flights/data/countries.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            country = Country(name=row['name'], code=row['iso3'])
            data.append(country)

    Country.objects.bulk_create(data)
    return len(data)
