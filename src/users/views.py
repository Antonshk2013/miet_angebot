from datetime import datetime

from django.contrib.auth import authenticate
from django.utils.timezone import make_aware
from rest_framework import status
from rest_framework.request import Request

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from src.users.serializers import UserApiSerializer


class CreateUserApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserApiSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginUserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs) -> Response:
        login = request.data.get('login')
        password = request.data.get('password')

        try:
            user = authenticate(
                request=request,
                password=password,
                username=login
            )

            if user is None:
                return Response(
                    data={
                        'error': 'Invalid username or password'
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )
            else:
                response = Response(status=status.HTTP_200_OK)
                refresh = RefreshToken.for_user(user)
                access = refresh.access_token

                refresh_exp = make_aware(
                    datetime.fromtimestamp(refresh.payload['exp'])
                )
                access_exp = make_aware(
                    datetime.fromtimestamp(access.payload['exp'])
                )

                response.set_cookie(
                    key='refresh',
                    value=str(refresh),
                    httponly=True,
                    secure=True,
                    samesite='Lax',
                    expires=refresh_exp
                )

                response.set_cookie(
                    key='access',
                    value=str(access),
                    httponly=True,
                    secure=True,
                    samesite='Lax',
                    expires=access_exp
                )

                return response

        except Exception as e:
            return Response(
                data={
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class LogoutUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs) -> Response:
        try:
            refresh_token = request.COOKIES.get('refresh')

            if refresh_token:
                token = RefreshToken(refresh_token)

                token.blacklist()

            response = Response(status=status.HTTP_200_OK)
        except Exception as e:
            response = Response(
                data={
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        finally:
            response.delete_cookie('access')
            response.delete_cookie('refresh')
            return response
