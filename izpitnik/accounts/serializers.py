from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['is_admin'] = user.is_staff
        token['roles'] = [role.name for role in user.groups.all()]
        token['is_superuser'] = user.is_superuser

        return token