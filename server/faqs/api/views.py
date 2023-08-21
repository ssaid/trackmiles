from faqs.api.serializers import FaqSerializer
from rest_framework import generics

from faqs.models import Faq


class FaqView(generics.ListAPIView):

    queryset = Faq.objects.filter(is_published=True)
    serializer_class = FaqSerializer
