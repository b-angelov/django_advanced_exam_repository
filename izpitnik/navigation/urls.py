from django.urls import path, include

from izpitnik.navigation.views import NavigationBarView

urlpatterns = [
    path('<slug:nav_name>/', NavigationBarView.as_view(), name='navigation-bar'),
    path("i18n/", include("django.conf.urls.i18n"))
]
