from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta


class Airport(models.Model):

    name = models.CharField(max_length=64)
    code = models.SlugField(max_length=10, unique=True)
    city = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    region = models.ForeignKey('Region', on_delete=models.CASCADE, related_name="airports")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Region(models.Model):

    name = models.CharField(max_length=64)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Flight(models.Model):

    airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="flights")
    users = models.ManyToManyField('User', related_name="flights")
    origin = models.CharField(max_length=64)
    destination = models.CharField(max_length=64)


    created_at = models.DateTimeField(auto_now_add=True)
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
    cost = models.FloatField()
    date = models.DateField(auto_now_add=True)



class User(AbstractUser):
    is_premium = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    flights = models.ManyToManyField(Flight, related_name="users")


class Suscriptions(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="suscriptions")
    price = models.FloatField()
    date = models.DateField(auto_now_add=True)
    due = models.DateField(default=datetime.now() + timedelta(days=30))
    payment_id = models.SlugField(unique=True, blank=True, null=True)


class Product(models.Model):

    name = models.CharField(max_length=64)
    price = models.FloatField()
    description = models.TextField()
    suscription = models.ForeignKey(Suscriptions, on_delete=models.CASCADE, related_name="products")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
