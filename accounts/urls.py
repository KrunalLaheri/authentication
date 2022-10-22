from django.urls import path
from .views import RegisterAPIView, LoginAPIView, ResetAPIView, UserAPIView, RefreshAPIView, LogoutAPIView, ForgotAPIView
urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('userview/', UserAPIView.as_view()),
    path('refreshtoken/', RefreshAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('forgot/', ForgotAPIView.as_view()),
    path('reset/', ResetAPIView.as_view()),
]
