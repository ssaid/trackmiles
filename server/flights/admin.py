from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Preference, Region, WaitingList

admin.site.register(User, UserAdmin)
admin.site.register(Preference)
admin.site.register(Region)
admin.site.register(WaitingList)
