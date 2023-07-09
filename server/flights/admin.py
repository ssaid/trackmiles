from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Preference, Region, WaitingList, Provider, Flight, FlightHistory

admin.site.register(User, UserAdmin)
admin.site.register(Preference)
admin.site.register(Region)
admin.site.register(WaitingList)
admin.site.register(Provider)
admin.site.register(Flight)
admin.site.register(FlightHistory)
