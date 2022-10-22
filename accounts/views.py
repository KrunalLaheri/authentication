import datetime
import random
import string
from urllib import response
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.views import Response
from accounts import serializers
from django.core.mail import send_mail


from accounts.auth import JWTAuthentication, create_access_token, create_refresh_token, decode_access_token, decode_refresh_token
from .models import User, UserToken, Reset
from accounts.serializers import UserSerializer
from rest_framework.authentication import get_authorization_header
# Create your views here.


class RegisterAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        data = request.data
        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Both passwords are not same!')
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginAPIView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed('Invalid credentials...')

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Invalid password...')

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        UserToken.objects.create(user_id=user.id, refresh_token=refresh_token,
                                 expired_at=datetime.datetime.utcnow()+datetime.timedelta(days=7))

        response = Response()
        response.set_cookie(key='refresh_token',
                            value=refresh_token, httponly=True)
        response.data = {
            'token': access_token,

        }

        return response


class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class RefreshAPIView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        id = decode_refresh_token(refresh_token)

        if not UserToken.objects.filter(user_id=id, refresh_token=refresh_token, expired_at__gt=datetime.datetime.now(tz=datetime.timezone.utc)).exists():
            raise exceptions.AuthenticationFailed('Unauthenticated')

        access_token = create_access_token(id)
        return Response({'token': access_token})


class LogoutAPIView(APIView):

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        print(request.COOKIES.get('refresh_token'))
        UserToken.objects.filter(refresh_token=refresh_token).delete()
        response = Response()
        response.delete_cookie(key='refresh_token')
        response.data = {
            'message': 'success'
        }
        return response


class ForgotAPIView(APIView):
    def post(self, request):
        token = ''.join(random.choice(string.ascii_lowercase +
                        string.digits) for _ in range(10))
        Reset.objects.create(
            email=request.data['email'],
            token=token
        )

        url = 'http://127.0.0.1:8000/reset/' + token

        send_mail('Password Reset',
                  f'Click here to reset your password'+url, 'laherikrunal10@gmail.com', [request.data['email']], fail_silently=False)
        return Response({
            'message': 'success',
            'token': token
        })


class ResetAPIView(APIView):
    def post(self, request):
        if request.data['password'] != request.data['password_confirm']:
            raise exceptions.APIException('Both password atre not match!')
        reset_password = Reset.objects.filter(
            token=request.data['token']).first()
        if not reset_password:
            raise exceptions.APIException('Invalid link!')
        user = User.objects.filter(email=reset_password.email).first()

        if not user:
            raise exceptions.APIException('User does not exist')

        user.set_password(request.data['password'])
        user.save()

        return Response({
            'message': 'success'
        })
