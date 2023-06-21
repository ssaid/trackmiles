from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from flights.models import Airport, Country, Preference, Region, WaitingList

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
    
        class Meta:
            model = Airport
            fields = ['display_name', 'code']

class PreferenceSerializer(serializers.ModelSerializer):

    airport_origin = serializers.SerializerMethodField()
    airport_destinations = serializers.SerializerMethodField()

    class Meta:
        model = Preference
        fields = ['airport_origin', 'airport_destinations']

    def get_airport_origin(self, obj):
        airport_origin = obj.airport_origin
        if airport_origin:
            serializer = AirportSerializer(airport_origin)
            return serializer.data
        return None

    def get_airport_destinations(self, obj):
        airport_origin = obj.airport_origin
        if airport_origin:
            airports_destinations = Airport.objects.filter(users_destination__airport_origin=airport_origin).distinct()
            serializer = AirportSerializer(airports_destinations, many=True)
            return serializer.data
        return []

class WaitingListSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=WaitingList.objects.all(),
                message='El email ya está registrado en el newsletter.'
            )
        ]
    )



    class Meta:
        model = WaitingList
        fields = '__all__'
