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

    country = serializers.StringRelatedField()
    class Meta:
        model = Airport
        fields = [ 'id', 'name', 'code', 'city', 'country' ]



class PreferenceSerializer(serializers.ModelSerializer):


    region_destination_name = serializers.CharField(source='region_destination.name', read_only=True)
    region_origin_name = serializers.CharField(source='region_origin.name', read_only=True)
    airport_origin_name = serializers.CharField(source='airport_origin.name', read_only=True)
    airport_destination_name = serializers.CharField(source='airport_destination.name', read_only=True)
    country_origin_name = serializers.CharField(source='country_origin.name', read_only=True)
    country_destination_name = serializers.CharField(source='country_destination.name', read_only=True)


    def validate(self, data):

        origin_fields = ( 'region_origin', 'airport_origin', 'country_origin' )
        destination_fields = ( 'region_destination', 'airport_destination', 'country_destination' )

        num_origin_fields = sum([field in data for field in origin_fields])
        num_destination_fields = sum([field in data for field in destination_fields])

        if num_origin_fields != 1:
            raise serializers.ValidationError('You must provide one origin field.')
        if num_destination_fields != 1:
            raise serializers.ValidationError('You must provide one destination field.')

        validated_data = super().validate(data)

        return validated_data


    class Meta:
        model = Preference
        exclude = ['user']

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
