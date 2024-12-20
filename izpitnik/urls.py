"""
URL configuration for izpitnik project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from izpitnik import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('izpitnik.common.urls')),
    path('navigation/', include('izpitnik.navigation.urls')),
    path('dstyles/', include('izpitnik.styling.urls')),
    path('auth/', include('izpitnik.accounts.urls')),
    path('orth_calendar/', include('izpitnik.orth_calendar.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('articles/', include('izpitnik.articles.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
