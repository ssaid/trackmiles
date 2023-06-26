from django.db.models import Prefetch, Subquery, OuterRef
from rest_framework.views import APIView, Response
from rest_framework import permissions, generics, pagination, status, filters, viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import *
from ..models import *

User = get_user_model()




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



class AirportsView(generics.ListAPIView):

    # permission_classes = [permissions.IsAuthenticated]

    serializer_class = PreferenceSerializer
    queryset = Preference.objects.distinct('airport_origin').filter(airport_origin__isnull=False)

    # def get_queryset(self):
    #     return Preference.objects.filter(user=self.request.user)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class WaitingListView(generics.CreateAPIView):

    serializer_class = WaitingListSerializer



class FlightDetailView(APIView):

    def get(self, request):

        origin = request.GET.get('origin')
        destination = request.GET.get('destination')
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')

        if not origin or not destination:
            return Response({'msg': 'Please provide origin and destination'}, status=status.HTTP_400_BAD_REQUEST)

        flight = Flight.objects.filter(
            origin__code__icontains=origin, 
            destination__code__icontains=destination
        ).first()

        if not flight:
            return Response({'msg': 'No flights found'}, status=status.HTTP_404_NOT_FOUND)

        data = {
            'origin': flight.origin.code,
            'dest': flight.destination.code,
            'details': []
        }

        flights = Flight.objects.filter(
            origin__code__icontains=origin, 
            destination__code__icontains=destination
        )

        if from_date:
            flights = flights.filter(flight_date__gte=from_date)
        if to_date:
            flights = flights.filter(flight_date__lte=to_date)



        for f in flights:
            info = FlightHistorySerializer(f.history.last())
            data['details'].append(
                { 
                    'flight_date': f.flight_date, 
                    'provider': f.provider,
                    'external_link': f.external_link,
                    **info.data, 
                }
            )

        return Response(data)
