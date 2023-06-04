from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta
from itertools import product


class Airport(models.Model):


    name = models.CharField(max_length=255)
    code = models.SlugField(max_length=10, unique=True, null=True)
    city = models.CharField(max_length=64)
    country = models.ForeignKey('Country', on_delete=models.PROTECT, related_name="airports", null=True)
    region = models.ForeignKey('Region', on_delete=models.SET_NULL, related_name="airports", null=True)

    display_name = models.CharField(max_length=255)
    display_name_long = models.CharField(max_length=255)

    class Meta:
        ordering = ['country__name', 'name']

    def __str__(self):
        return '[%s] %s' % (self.country and self.country.code or '-', self.code)

class Country(models.Model):

    name = models.CharField(max_length=64)
    code = models.SlugField(max_length=10, unique=True, null=True)


    def __str__(self):
        return self.name

class AirLine(models.Model):

    name = models.CharField(max_length=64)
    code = models.SlugField(max_length=10, unique=True)


class Region(models.Model):

    name = models.SlugField(max_length=64)


class Flight(models.Model):

    airport_origin = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name="flight_outgoing")
    airport_destination = models.ForeignKey(Airport, on_delete=models.PROTECT, related_name="flights_incoming")

    flight_date = models.DateField(null=False, blank=False)

    external_link = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-flight_date']


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
    miles = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)


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
