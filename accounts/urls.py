from django.contrib import admin
from django.urls import path
from .views import RegisterAPIView, LoginAPIView, UserAPIView, RefreshAPIView, LogoutAPIView
urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('userview/', UserAPIView.as_view()),
    path('refreshtoken/', RefreshAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view())
]
