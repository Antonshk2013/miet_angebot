from django.urls import path

from src.users.views import (
    LoginUserAPIView,
    LogoutUserAPIView,
    CreateUserApiView
)

urlpatterns = [
    path('login/', LoginUserAPIView.as_view(), name='login'),
    path('logout/', LogoutUserAPIView.as_view(), name='logout'),
    path('user_create/', CreateUserApiView.as_view(), name='user_create'),
]