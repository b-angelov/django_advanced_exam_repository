from django.urls import path, include

from izpitnik.styling.views import DynamicStyleView, DynamicJSView

urlpatterns = [
    path('<slug:style_name>/', include([
            path('css/', DynamicStyleView.as_view(), name="dynamic-css"),
            path('js/', DynamicJSView.as_view(), name="dynamic-js")
         ])
    ),
]
