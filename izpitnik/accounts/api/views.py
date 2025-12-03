# views.py
from typing import Literal

from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import update_last_login
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.conf import settings

from izpitnik.accounts.mixins import GenerateTokenMixin
from izpitnik.accounts.serializers import CustomTokenObtainPairSerializer
from izpitnik.settings import ENV




class CustomTokenObtainPairView(TokenObtainPairView):

    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh = response.data.pop('refresh', None)
        response = GenerateTokenMixin(response=response, refresh=refresh).issue_token(request)
        return response

# views.py

class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token is None:
            raise AuthenticationFailed('No refresh token found in cookies.')

        serializer = self.get_serializer(data={'refresh': refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'detail': 'Invalid refresh token.'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.validated_data)


class ApiLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:
            refresh_token = request.COOKIES.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        return GenerateTokenMixin().unset_cookie(request)

class ApiSignUpVew(UserPassesTestMixin,APIView):

    permission_classes = [AllowAny]

    def test_func(self):
        return not self.request.user.is_authenticated

    def post(self, request):

        from izpitnik.accounts.forms import MainUserCreationForm

        data = request.data

        form = MainUserCreationForm(data)

        if form.is_valid():
            user = form.save()
            token = CustomTokenObtainPairSerializer.get_token(user)
            return GenerateTokenMixin(refresh=str(token), access=str(token.access_token)).issue_token(request)

        else:
            return Response(form.errors, status=400)


