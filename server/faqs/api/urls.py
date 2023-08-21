from django.urls import path

from .views import FaqView


urlpatterns = [
    path('faqs/', FaqView.as_view()),
]
