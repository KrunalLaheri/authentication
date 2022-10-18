from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.views import Response

from accounts.serializers import UserSerializer
# Create your views here.


class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data
        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Both passwords are not same!')
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
