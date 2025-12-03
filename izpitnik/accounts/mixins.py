from rest_framework.response import Response
from izpitnik.settings import ENV


class GenerateTokenMixin():

    def __init__(self, *args, **kwargs):
        self.response = kwargs.get('response', args[0] if args else None)
        self.refresh = kwargs.get('refresh', args[1] if len(args) > 1 else None)
        self.access = kwargs.get('access', args[2] if len(args) > 2 else None)
        self.secure = True if ENV == "production" else False
        self.same_site = 'Strict' if ENV == "production" else False

    def issue_token(self, request):
        response = self.response or Response({"access":self.access},status=201)
        if self.refresh:
            response.set_cookie(
                key='refresh_token',
                value=self.refresh,
                httponly=True,
                secure=self.secure,
                samesite=self.same_site,
                max_age=7 * 24 * 60 * 60,  # 7 days
                path='/api/token',
                domain=self.build_domain(request)
            )
        return response

    def unset_cookie(self, request):

        response = Response({"detail": "Logout successful."}, status=200)
        response.delete_cookie(
            key='refresh_token',
            samesite=self.same_site,
            path='/api/token',
            domain=self.build_domain(request)
        )
        return response

    @staticmethod
    def build_domain(request):
        return request.build_absolute_uri('/')[:-1].replace("http://", "").replace("https://", "").split(":")[0]
