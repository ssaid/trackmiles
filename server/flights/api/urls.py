from django.urls import path, include, re_path


from .views import RegistrationView

urlpatterns = [
    path('register/', RegistrationView.as_view()),
]

