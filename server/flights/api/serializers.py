from django.contrib.auth import get_user_model
from rest_framework import serializers

from flights.models import Airport, Country, Region

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )
        return user


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'

class AirportSerializer(serializers.ModelSerializer):

    country = serializers.StringRelatedField()
    class Meta:
        model = Airport
        fields = [ 'id', 'name', 'code', 'city', 'country' ]


