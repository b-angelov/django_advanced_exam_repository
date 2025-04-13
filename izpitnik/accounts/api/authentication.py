from rest_framework_simplejwt.tokens import AccessToken


class CustomAccessToken(AccessToken):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        print("CustomAccessToken initialized")

    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        token["is_admin"] = user.is_staff
        token['roles'] = [role.name for role in user.groups.all()]
        token['is_superuser'] = user.is_superuser
        # token['is_active'] = self.user.is_active
        # token['is_verified'] = self.user.is_verified

        print("token issued")
        return token