from rest_framework import routers

from flights.api.views import PreferenceViewSet


router = routers.SimpleRouter()

router.register('preferences', PreferenceViewSet, basename='preferences')

