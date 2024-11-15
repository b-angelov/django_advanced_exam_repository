from django.urls import path, include

from izpitnik.navigation.views import NavigationBarView

urlpatterns = [
    path('<slug:nav_name>/', NavigationBarView.as_view(), name='navigation-bar'),
]
