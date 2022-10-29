import datetime
import random
import string
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.views import Response
from django.core.mail import send_mail
from accounts.auth import JWTAuthentication, create_access_token, create_refresh_token, decode_access_token, decode_refresh_token
from .models import User, UserToken, Reset,Student,Teacher
from accounts.serializers import UserSerializer,StudentSerializer,TeacherSerializer
# Create your views here.

# ===========================================================================================================
# Write dummy code here
# ============================================================================================================
class RegisterAPIView(APIView):
    # authentication_classes = [JWTAuthentication]

    def post(self, request):
        data = request.data
        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Both passwords are not same!')
        user_data={'email': data['email'], 'password': data['password'], 'password_confirm': data['password_confirm'],'is_student': data['is_student'],'is_teacher':data['is_teacher']}
        print(user_data)
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        if data['is_student']=="True":
            user_student = User.objects.get(email=data['email'])
            student_data={'student':user_student,'name':data['name'],'admission_date':data['admission_date']}
            print(student_data)
            student_serializer = StudentSerializer(data=student_data)
            student_serializer.is_valid(raise_exception=True)
            student_serializer.save()
        if data['is_teacher']=="True":
            user_teacher = User.objects.get(email=data['email'])
            teacher_data={'teacher':user_teacher,'name':data['name'],'joining_date':data['joining_date']}
            print(teacher_data)
            teacher_serializer = TeacherSerializer(data=teacher_data)
            teacher_serializer.is_valid(raise_exception=True)
            teacher_serializer.save()
        return Response(user_serializer.data)



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
        data=serializer.data
        if data['is_student']==True:
            student=Student.objects.get(student_id=request.user.id)
            student_serializer=StudentSerializer(instance=student).data
            data.update(student_serializer)
            
        if data['is_teacher']==True:
            teacher=Teacher.objects.get(teacher_id=request.user.id)
            teacher_serializer=TeacherSerializer(instance=teacher).data
            data.update(teacher_serializer)
        return Response(data)

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
        access_token = request.COOKIES.get('access_token')
        print(request.COOKIES.get('refresh_token'))
        print(access_token)
        UserToken.objects.filter(refresh_token=refresh_token).delete()
        response = Response()
        response.delete_cookie('refresh_token')
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

        # send_mail('Password Reset',
        #           f'Click here to reset your password'+url, 'laherikrunal10@gmail.com', [request.data['email']], fail_silently=False)
        return Response({
            'message': 'success',
            # 'token': token
            'token': url
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
