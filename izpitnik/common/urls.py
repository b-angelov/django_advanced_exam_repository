from django.urls import path, include

from izpitnik.common.views import HomePage

urlpatterns = [
    path('', HomePage.as_view(), name='home-page')
]
