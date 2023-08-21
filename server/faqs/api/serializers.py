from rest_framework import serializers

from faqs.models import Faq


class FaqSerializer(serializers.ModelSerializer):

    class Meta:
        model = Faq
        fields = ('id', 'question', 'answer')
