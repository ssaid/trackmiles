from rest_framework.views import APIView, Response

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .middlewares import CustomTokenAuthentication
from .serializers import UserSerializer

User = get_user_model()




class RegistrationView(APIView):
    """
    View for user management
    """

    authentication_classes = [CustomTokenAuthentication]

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

    from rest_framework import permissions
    permission_classes = [permissions.IsAuthenticated]


    def get(self, request):

        user = request.user

        if user.is_anonymous:
            return Response({'msg': 'Not authenticated'})
        return Response({'msg': 'Hi, {}'.format(user.username)})
