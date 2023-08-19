from django.db.models import Prefetch 
from rest_framework.views import APIView, Response
from rest_framework import permissions, generics, pagination, status, filters 
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import *
from ..models import *

User = get_user_model()

import logging
logger = logging.getLogger(__name__)


class RegistrationView(APIView):
    """
    View for user management.
    """

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            201: openapi.Response(
                description="User created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'username': openapi.Schema(type=openapi.TYPE_STRING),
                        'email': openapi.Schema(type=openapi.TYPE_STRING),
                        'password': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                    required=['username', 'email', 'password']
                )
            ),
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        user = request.user

        if user.is_anonymous:
            return Response({'msg': 'Not authenticated'})
        return Response({'msg': 'Hi, {}'.format(user.username)})


class RegionView(generics.ListAPIView):

    permission_classes = [permissions.IsAuthenticated]

    serializer_class = RegionSerializer
    queryset = Region.objects.all()


class CountryView(generics.ListAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CountrySerializer
    queryset = Country.objects.all()

    pagination_class = pagination.LimitOffsetPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'code']



class AirportView(generics.ListAPIView):

    serializer_class = AirportSerializer
    queryset = Airport.objects.all()



class AirportsView(APIView):

    @method_decorator(cache_page(60 * 60 * 6)) # 6 hours
    def get(self, request):

        routes = Preference.get_all_routes()

        tmp_dict = {}
        for origin, destination in routes:
            if origin not in tmp_dict:
                tmp_dict[origin] = []

            if destination not in tmp_dict[origin]:
                tmp_dict[origin].append(destination)


        result = []
        for origin, destinations in tmp_dict.items():
            origin = Airport.objects.get(code=origin)
            destinations = Airport.objects.filter(code__in=destinations)

            result.append({
                'airport_origin': AirportSerializer(origin).data,
                'airport_destinations': AirportSerializer(destinations, many=True).data
            })


        return Response(result)


class WaitingListView(generics.CreateAPIView):

    serializer_class = WaitingListSerializer



class FlightDetailView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('origin', openapi.IN_QUERY, description='Origin airport code', type=openapi.TYPE_STRING),
            openapi.Parameter('destination', openapi.IN_QUERY, description='Destination airport code', type=openapi.TYPE_STRING),
            openapi.Parameter('from_date', openapi.IN_QUERY, description='Start date', type=openapi.TYPE_STRING),
            openapi.Parameter('to_date', openapi.IN_QUERY, description='End date', type=openapi.TYPE_STRING),
        ]
    )
    @method_decorator(cache_page(60 * 60 * 6)) # 6 hours
    def get(self, request):
        """
        Retrieve flight details based on origin, destination, and date range.
        """

        origin = request.GET.get('origin')
        destination = request.GET.get('destination')
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')

        if not origin or not destination:
            return Response({'msg': 'Please provide origin and destination'}, status=status.HTTP_400_BAD_REQUEST)

        flights = Flight.objects.filter(
            origin__code__icontains=origin,
            destination__code__icontains=destination
        )

        if not flights.count():
            return Response({'msg': 'No flights found'}, status=status.HTTP_404_NOT_FOUND)

        data = {
            'origin': flights.first().origin.display_name,
            'dest': flights.first().destination.display_name,
            'details': []
        }

        if from_date:
            flights = flights.filter(flight_date__gte=from_date)
        if to_date:
            flights = flights.filter(flight_date__lte=to_date)

        pf_history = Prefetch('history', queryset=FlightHistory.objects.prefetch_related('airline').order_by('-created_at'))

        flights = flights.prefetch_related(pf_history, 'provider',).all()

        import statistics

        newest_history = [ next((fh for fh in f.history.all())) for f in flights if f.history.exists()]
        miles_data = [h.miles for h in newest_history]

        miles_mean = sum(miles_data) / len(miles_data)
        miles_median = statistics.median(miles_data)

        data['miles_mean'] = int(miles_mean)
        data['miles_median'] = int(miles_median)

        data['miles_max'] = int(max(miles_data))
        data['miles_min'] = int(min(miles_data))

        for f in flights:
            # as the default ordering of flight history is -created_at,
            # we know the first record is the newest one
            history = next((fh for fh in f.history.all())) if f.history.exists() else None
            if history:
                porcentual = int((history.miles - miles_median) / miles_median * 100)
                # porcentual = int((history.miles - miles_mean) / miles_mean * 100)
                info = FlightHistorySerializer(history)
                data['details'].append(
                    {
                        'flight_date': f.flight_date,
                        'provider': f.provider.name if f.provider else None,
                        'external_link': f.external_link,
                        'porcentual': porcentual,
                        **info.data,
                    }
                )

        return Response(data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'miles': openapi.Schema(type=openapi.TYPE_INTEGER),
                'tax_miles': openapi.Schema(type=openapi.TYPE_INTEGER),
                'money': openapi.Schema(type=openapi.TYPE_NUMBER),
                'tax_money': openapi.Schema(type=openapi.TYPE_NUMBER),
                'fare_clean': openapi.Schema(type=openapi.TYPE_NUMBER),
                'seats': openapi.Schema(type=openapi.TYPE_INTEGER),
                'stops': openapi.Schema(type=openapi.TYPE_INTEGER),
                'baggage': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                'departure_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                'airline_code': openapi.Schema(type=openapi.TYPE_STRING),
                'airline_name': openapi.Schema(type=openapi.TYPE_STRING),
                'origin_code': openapi.Schema(type=openapi.TYPE_STRING),
                'destination_code': openapi.Schema(type=openapi.TYPE_STRING),
                'provider': openapi.Schema(type=openapi.TYPE_STRING),
                'external_link': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=[
                'miles',
                'money',
                'departure_date',
                'airline_code',
                'airline_name',
                'origin_code',
                'destination_code',
                'provider',
                'external_link',
            ],
        ),
        responses={
            201: openapi.Response(
                description='Flight history created successfully.',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        # Include other response properties if applicable
                    },
                ),
            ),
            # Include other response codes and descriptions if applicable
        },
    )
    def post(self, request):


        a_origin = Airport.objects.get(code=request.data.get('origin_code').upper())
        a_destination = Airport.objects.get(code=request.data.get('destination_code').upper())
        provider, _ = Provider.objects.get_or_create(name=request.data.get('provider'))

        flight, _ = Flight.objects.get_or_create(
            origin=a_origin,
            destination=a_destination,
            provider=provider,
            flight_date= datetime.strptime(request.data.get('departure_date'), '%Y-%m-%d').date(),
        )

        external_link = request.data.get('external_link')
        if external_link != flight.external_link:
            flight.external_link = external_link
            flight.save()


        airline, _ = AirLine.objects.get_or_create(
            code=request.data.get('airline_code'),
            defaults={'name': request.data.get('airline_name')}
        )


        history = FlightHistorySerializer(
            data={
                'flight_id': flight.id,
                'airline_id': airline.id,
                **request.data
            }
        )

        if history.is_valid():
            history.save()
            return Response(history.data, status=status.HTTP_201_CREATED)

        logger.error(history.errors)
        return Response(history.errors, status)
