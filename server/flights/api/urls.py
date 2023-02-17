from django.urls import path, include, re_path


from .views import HelloWorldView

urlpatterns = [
    path('flights/hello_world', HelloWorldView.as_view()),
]

