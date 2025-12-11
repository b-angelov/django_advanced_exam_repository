# views.py
from typing import Literal

from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import update_last_login
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.conf import settings

from izpitnik.accounts.api.permissions import IsOwnerPermission, add_or_change_permission_decorator, \
    delete_permission_decorator
from izpitnik.accounts.mixins import GenerateTokenMixin
from izpitnik.accounts.serializers import CustomTokenObtainPairSerializer, UserProfileSerializer
from izpitnik.articles.api.permissions import IsAuthorOnAllMethodsPermission
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

class GetUpdateDeleteProfileAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerPermission]
    lookup_url_kwarg = "user_id"
    serializer_class = UserProfileSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        from izpitnik.accounts.models import User
        user_id = self.rectify_kwarg(self.request, self.kwargs).get(self.lookup_url_kwarg)
        return User.objects.filter(pk=user_id).prefetch_related("profile")

    def get(self, request, *args, **kwargs):
        kwargs = self.rectify_kwarg(request, kwargs)
        response = super().get(request,*args, **kwargs)
        return response

    def rectify_kwarg(self, request, kwargs):
        user_id = kwargs.get(self.lookup_url_kwarg)
        if user_id == 'my':
            kwargs[self.lookup_url_kwarg] = str(request.user.pk)
        return kwargs


    @add_or_change_permission_decorator
    def put(self, request, *args, **kwargs):
        kwargs = self.rectify_kwarg(request, kwargs)
        return super().put(request, *args, **kwargs)

    @add_or_change_permission_decorator
    def patch(self, request, *args, **kwargs):
        kwargs = self.rectify_kwarg(request, kwargs)
        return super().patch(request, *args, **kwargs)

    @delete_permission_decorator
    def delete(self, request, *args, **kwargs):
        kwargs = self.rectify_kwarg(request, kwargs)
        return super().delete(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def perform_update(self, serializer):
        instance = serializer.save()
        uploaded = self.request.FILES.get('image') or self.request.FILES.get('avatar') or self.request.FILES.get(
            'profile_image')
        if uploaded and hasattr(instance, 'profile'):
            instance.profile.image = uploaded
            instance.profile.save()

