from django.urls import path, include

from izpitnik.styling.views import DynamicStyleView

urlpatterns = [
    path('<slug:style_name>/', DynamicStyleView.as_view(), name="dynamic-style"),
]
