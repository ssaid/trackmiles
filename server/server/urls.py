from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path


from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="TrackMiles API",
        default_version="v1",
        description="API for TrackMiles App",
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('flights.api.urls')),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-json",
    ),
    path(
        "api/v1/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
