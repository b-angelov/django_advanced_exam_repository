# views.py
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.conf import settings

from izpitnik.settings import ENV


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['is_admin'] = user.is_staff
        token['roles'] = [role.name for role in user.groups.all()]
        token['is_superuser'] = user.is_superuser

        return token

class CustomTokenObtainPairView(TokenObtainPairView):

    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh = response.data.pop('refresh', None)

        secure = False
        samesite = False

        if ENV == "production":
            secure = True
            samesite = True

        if refresh:
            response.set_cookie(
                key='refresh_token',
                value=refresh,
                httponly=True,
                secure=secure,
                samesite=samesite,
                max_age=7 * 24 * 60 * 60,  # 7 days
                path='/api/token',
                domain=request.build_absolute_uri('/')[:-1].replace("http://","").replace("https://","").split(":")[0]
            )
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

        secure = False
        samesite = False

        if ENV == "production":
            secure = True
            samesite = "Strict"

        try:
            print(request.COOKIES.get("refresh_token"))
            refresh_token = request.COOKIES.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        response = Response({"detail": "Logout successful."}, status=200)
        response.delete_cookie(
            key='refresh_token',
            samesite=samesite,
            path='/api/token',
            domain=request.build_absolute_uri('/')[:-1].replace("http://", "").replace("https://", "").split(":")[0]
        )
        return response


