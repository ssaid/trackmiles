from django.urls import path, include, re_path

from .views import (
    WaitingListView, AirportsView
)


urlpatterns = [
    path('airports/', AirportsView.as_view()),
    path('waitinglist/', WaitingListView.as_view()),
]

