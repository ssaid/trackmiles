from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta
from itertools import product
from django.core.exceptions import ValidationError


class Airport(models.Model):
    name = models.CharField(max_length=255)
    code = models.SlugField(max_length=10, unique=True, null=True)
    city = models.CharField(max_length=64)
    country = models.ForeignKey('Country', on_delete=models.PROTECT, related_name="airports", null=True)
    # region = models.ForeignKey('Region', on_delete=models.SET_NULL, related_name="airports", null=True)

    display_name = models.CharField(max_length=255)
    display_name_long = models.CharField(max_length=255)

    class Meta:
        ordering = ['country__name', 'name']

    def __str__(self):
        return '[%s] %s, %s, %s' % (
            self.code,
            self.name,
            self.city,
            self.country and self.country.name or '-',
        )


class Country(models.Model):

    name = models.CharField(max_length=64)
    code = models.SlugField(max_length=10, unique=True, null=True)

    def __str__(self):
        return self.name


class AirLine(models.Model):

    name = models.CharField(max_length=64)
    code = models.SlugField(max_length=10, unique=True)

    def __str__(self):
        return f'[{self.code}] {self.name}'


class Region(models.Model):

    name = models.SlugField(max_length=64)
    airports = models.ManyToManyField(Airport, related_name="regions")

    def __str__(self):
        return f'{self.name}'


class Provider(models.Model):

    name = models.CharField(max_length=64)
    base_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Flight(models.Model):

    origin = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name="flight_outgoing")
    destination = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name="flights_incoming")

    flight_date = models.DateField(null=False, blank=False)

    provider = models.ForeignKey(Provider, on_delete=models.PROTECT, related_name="flights", null=True)

    external_link = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-flight_date']

    def __str__(self):
        return '[%s] %s -> %s' % (self.flight_date, self.origin, self.destination)

    def get_avg_last_six_months(self):
        delta_date = datetime.now() - timedelta(days=180)

        return self.costs.filter(flight_date__gte=delta_date).aggregate(models.Avg('cost'))['cost__avg']

    def get_avg_last_three_months(self):
        delta_date = datetime.now() - timedelta(days=90)
        return self.costs.filter(flight_date__gte=delta_date, ).aggregate(models.Avg('cost'))['cost__avg']

    def get_avg_last_month(self):
        delta_date = datetime.now() - timedelta(days=30)
        return self.costs.filter(flight_date__gte=delta_date).aggregate(models.Avg('cost'))['cost__avg']

    def get_best_price_by_money(self):
        return self.costs.filter(flight_date__gte=datetime.now()).order_by('history__money').first()

    def get_best_price_by_miles(self):
        return self.costs.filter(flight_date__gte=datetime.now()).order_by('history__miles').first()


class FlightHistory(models.Model):

    flight = models.ForeignKey(Flight, on_delete=models.PROTECT, related_name="history")
    airline = models.ForeignKey(AirLine, on_delete=models.PROTECT)

    money = models.FloatField()
    tax_money = models.FloatField(null=True, blank=True)
    miles = models.PositiveIntegerField()
    tax_miles = models.PositiveIntegerField(null=True, blank=True)
    seats = models.PositiveIntegerField(null=True, blank=True)
    duration = models.PositiveIntegerField(null=True, blank=True)
    stops = models.PositiveIntegerField(null=True, blank=True)
    baggage = models.BooleanField(default=False)
    fare_clean = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class User(AbstractUser):
    is_premium = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    flights = models.ManyToManyField(Flight, related_name="users")

    username = models.CharField(max_length=255, unique=True, null=True)

    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Preference(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="preferences")

    region_origin = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="users_origin", null=True, blank=True)
    region_destination = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="users_destination", null=True, blank=True)

    airport_origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="users_origin", null=True, blank=True)
    airport_destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="users_destination", null=True, blank=True)

    country_origin = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="users_origin", null=True, blank=True)
    country_destination = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="users_destination", null=True, blank=True)

    date_from = models.DateField(null=True, blank=True)
    date_to = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        airports = any([self.airport_origin, self.airport_destination])
        regions = any([self.region_origin, self.region_destination])
        countries = any([self.country_origin, self.country_destination])
        all_airports = all([self.airport_origin, self.airport_destination])
        all_regions = all([self.region_origin, self.region_destination])
        all_countries = all([self.country_origin, self.country_destination])
        if airports and not (regions or countries) and all_airports:
            return True
        elif regions and not (airports or countries) and all_regions:
            return True
        elif countries and not (airports or regions) and all_countries:
            return True
        else:
            raise ValidationError('Improperly configured! HINT: Configure the airports OR the region OR the countries')

    def __str__(self):
        if self.airport_origin and self.airport_destination:
            return '[AIRPORT] %s -> %s' % (self.airport_origin.code, self.airport_destination.code)
        elif self.country_origin and self.country_destination:
            return '[COUNTRY] %s -> %s' % (self.country_origin, self.country_destination)
        elif self.region_origin and self.region_destination:
            return '[REGION.] %s -> %s' % (self.region_origin, self.region_destination)
        else:
            return '-'

    @classmethod
    def get_all_routes(self):
        preferences = self.objects.all()
        all_routes = []
        for preference in preferences:
            for route in preference.get_routes():
                if route not in all_routes:
                    all_routes.append(route)
        return all_routes

    def get_routes(self):
        """ <- set(('eze','mex'),('eze','cun'))"""
        a_fr = []
        a_to = []
        # origin
        if self.airport_origin:
            a_fr.append(self.airport_origin.code)
        if self.region_origin:
            a_fr += list(map(lambda x: x.code, self.region_origin.airports.all()))
        if self.country_origin:
            a_fr += list(map(lambda x: x.code, self.country_origin.airports.all()))
        # destination
        if self.airport_destination:
            a_to.append(self.airport_destination.code)
        if self.region_destination:
            a_to += list(map(lambda x: x.code, self.region_destination.airports.all()))
        if self.country_destination:
            a_to += list(map(lambda x: x.code, self.country_destination.airports.all()))

        res = set(product(a_fr, a_to))

        return res



class Suscriptions(models.Model):

    def default_due_date(self):
        return datetime.now() + timedelta(days=30)

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="suscriptions")
    price = models.FloatField()
    date = models.DateField(auto_now_add=True)
    due = models.DateField(default=default_due_date)
    payment_id = models.SlugField(unique=True, blank=True, null=True)

    product = models.ForeignKey('Product', on_delete=models.PROTECT, related_name="suscriptions")


class Product(models.Model):

    name = models.CharField(max_length=64)
    price = models.FloatField()
    description = models.TextField()
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class WaitingList(models.Model):

    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
