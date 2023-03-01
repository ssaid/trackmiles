from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta


class Airport(models.Model):

    name = models.CharField(max_length=255)
    code = models.SlugField(max_length=10, unique=True, null=True)
    city = models.CharField(max_length=64)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name="airports")
    region = models.ForeignKey('Region', on_delete=models.CASCADE, related_name="airports")


class Country(models.Model):
    
    name = models.CharField(max_length=64)
    code = models.SlugField(max_length=10, unique=True, null=True)

class AirLine(models.Model):
    
    name = models.CharField(max_length=64)
    code = models.SlugField(max_length=10, unique=True)


class Region(models.Model):

    name = models.SlugField(max_length=64)


class Flight(models.Model):

    airport_origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="flight_outgoing")
    airport_destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="flights_incoming")

    external_link = models.URLField()

    updated_at = models.DateTimeField(auto_now=True)


    def get_avg_last_six_months(self):
        delta_date = datetime.now() - timedelta(days=180)
        return self.costs.filter(date__gte=delta_date).aggregate(models.Avg('cost'))['cost__avg']


    def get_avg_last_three_months(self):
        delta_date = datetime.now() - timedelta(days=90)
        return self.costs.filter(date__gte=delta_date).aggregate(models.Avg('cost'))['cost__avg']


    def get_avg_last_month(self):
        delta_date = datetime.now() - timedelta(days=30)
        return self.costs.filter(date__gte=delta_date).aggregate(models.Avg('cost'))['cost__avg']



class FlightCost(models.Model):

    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="costs")
    airline = models.ForeignKey(AirLine, on_delete=models.CASCADE, related_name="flight_costs")

    money = models.FloatField()
    miles = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']



class User(AbstractUser):
    is_premium = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    flights = models.ManyToManyField(Flight, related_name="users")

    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Preference(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="preferences")

    region_destination = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="users_destination", null=True)
    region_origin = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="users_origin", null=True)

    airport_origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="users_origin", null=True)
    airport_destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="users_destination", null=True)

    country_origin = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="users_origin", null=True)
    country_destination = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="users_destination", null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Suscriptions(models.Model):

    def default_due_date(self):
        return datetime.now() + timedelta(days=30)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="suscriptions")
    price = models.FloatField()
    date = models.DateField(auto_now_add=True)
    due = models.DateField(default=default_due_date)
    payment_id = models.SlugField(unique=True, blank=True, null=True)



class Product(models.Model):

    name = models.CharField(max_length=64)
    price = models.FloatField()
    description = models.TextField()
    suscription = models.ForeignKey(Suscriptions, on_delete=models.CASCADE, related_name="products")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
