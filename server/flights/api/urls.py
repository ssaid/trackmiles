from django.urls import path, include, re_path


from .views import RegistrationView, UserView

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('whoami/', UserView.as_view()),
]

