from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from izpitnik.accounts.models import User, Profile


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['is_admin'] = user.is_staff
        token['roles'] = [role.name for role in user.groups.all()]
        token['is_superuser'] = user.is_superuser

        return token

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['description', 'image', 'birth_date']

class UserProfileSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        depth = 1
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        profile = instance.profile

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if profile_data is not None:
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance