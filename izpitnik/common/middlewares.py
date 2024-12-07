from http import HTTPStatus

from izpitnik import settings
from izpitnik.common.views import ErrorView


class CommonErrorMiddleware:

    def __init__(self, response):
        self.get_response = response

    def __call__(self, request):
        response = self.get_response(request)
        if settings.DEBUG == False and response.status_code >= 400:
            v = ErrorView(request,status_code=response.status_code)
            return v
        return response