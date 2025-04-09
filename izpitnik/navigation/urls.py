from django.urls import path, include

from izpitnik.navigation.api_views import NavigationApiView
from izpitnik.navigation.views import NavigationBarView

urlpatterns = [
    path('<slug:nav_name>/', include([
        path('', NavigationBarView.as_view(), name='navigation-bar'),
        path('api/', NavigationApiView.as_view(), name='navigation-api'),
    ])
         ),
    path("i18n/", include("django.conf.urls.i18n"))
]
