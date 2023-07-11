from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Preference, Region, WaitingList, Provider, Flight, FlightHistory, Airport, Country

admin.site.register(User, UserAdmin)
admin.site.register(WaitingList)


class ProviderAdmin(admin.ModelAdmin):
    fields = ['name']


class FlightHistoryInline(admin.TabularInline):
    model = FlightHistory
    fields = ['created_at', 'miles', 'airline', 'seats', 'duration', 'stops', 'baggage']
    readonly_fields = ["created_at", "miles", "airline", "seats", "duration", "stops", "baggage"]
    ordering = ("-created_at",)

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class FlightAdmin(admin.ModelAdmin):
    list_display = ["upper_case_name", "flight_date"]
    inlines = [FlightHistoryInline]
    readonly_fields = ['origin', 'destination', 'flight_date', 'provider', 'external_link']
    fields = [('origin', 'destination', 'provider'), 'external_link']

    @admin.display(description="Name")
    def upper_case_name(self, obj):
        return f"{obj.origin} -> {obj.destination}"


class AirportInline(admin.TabularInline):
    model = Airport
    # fields = ['name']
    # readonly_fields = ['code', 'name', 'city']
    # readonly_fields = ["created_at", "miles", "airline", "seats", "duration", "stops", "baggage"]
    ordering = ("city",)

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class CountryAdmin(admin.ModelAdmin):
    fields = ['code']
    search_fields = ['name', 'code']
    readonly_fields = ['name', 'code']
    inlines = [AirportInline]


class RegionAdmin(admin.ModelAdmin):
    fields = ['name', 'airports']
    search_fields = ['name']
    # inlines = [AirportInline]
    filter_horizontal = ['airports']


class AirportAdmin(admin.ModelAdmin):
    fields = [('country', 'city')]
    search_fields = ['name', 'country__name', 'code']
    readonly_fields = ['country', 'city']


class PreferenceAdmin(admin.ModelAdmin):
    fields = [
        'user',
        ('airport_origin', 'airport_destination'),
        ('country_origin', 'country_destination'),
        ('region_origin', 'region_destination'),
        ('date_from', 'date_to'),
    ]
    autocomplete_fields = [
        'airport_origin', 'airport_destination',
        'country_origin', 'country_destination',
        'region_origin', 'region_destination',
    ]


admin.site.register(Flight, FlightAdmin)
admin.site.register(Airport, AirportAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Preference, PreferenceAdmin)
admin.site.register(Provider, ProviderAdmin)
