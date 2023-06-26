from django.urls import path, include, re_path

from .views import (
    FlightDetailView, WaitingListView, AirportsView
)


urlpatterns = [
    path('airports/', AirportsView.as_view()),
    path('flights/', FlightDetailView.as_view()),
    path('waitinglist/', WaitingListView.as_view()),
]

