from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Preference, Region

admin.site.register(User, UserAdmin)
admin.site.register(Preference)
admin.site.register(Region)
