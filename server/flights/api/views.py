from rest_framework.views import APIView, Response

class HelloWorldView(APIView):

    def get(self, _):

        return Response({'message': 'Hello, world!'})
