from requests.sessions import InvalidSchema
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from flights.models import Airport, Country, Flight, FlightHistory, Preference, Region, WaitingList

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
            fields = ['display_name_long', 'code']


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

class FlightHistorySerializer(serializers.ModelSerializer):

    flight_id = serializers.IntegerField()
    airline_id = serializers.IntegerField()
    airline = serializers.StringRelatedField()

    class Meta:
        model = FlightHistory
        exclude = ['flight', 'id']

class FlightSerializer(serializers.ModelSerializer):

    detail = serializers.SerializerMethodField()

    class Meta:
        model = Flight
        exclude = ['created_at', 'updated_at', 'id', 'origin', 'destination']

    def get_detail(self, instance: Flight):
        flight_history = instance.history.last()
        if flight_history:
            serializer = FlightHistorySerializer(flight_history)
            return serializer.data
        return None



