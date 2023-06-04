from django.urls import path, include, re_path

from .routers import router




from .views import (
    RegistrationView, UserView, RegionView,
    CountryView, AirportView, WaitingListView,
)

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('whoami/', UserView.as_view()),
    path('regions/', RegionView.as_view()),
    path('countries/', CountryView.as_view()),
    path('airports/', AirportView.as_view()),
    path('waitinglist/', WaitingListView.as_view()),
    path('', include(router.urls)),
]

