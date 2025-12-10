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
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from izpitnik import settings
from izpitnik.accounts.api.views import CustomTokenObtainPairView, CookieTokenRefreshView, ApiLogoutView, ApiSignUpVew, \
    GetUpdateDeleteProfileAPIView
from izpitnik.articles.api.views import ArtilceAPIView, CreateArticleAPIView, GetUpdateDeleteArticleAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('izpitnik.common.urls')),
    path('api/', include([
        path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
        path( 'register/', ApiSignUpVew.as_view(), name='api_register'),
        path( 'profile/<slug:user_id>/', GetUpdateDeleteProfileAPIView.as_view(), name='api_profile'),
        path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
        path('token/logout/', ApiLogoutView.as_view(), name='logout-api'),
        path('articles/', ArtilceAPIView.as_view(), name='articles-api'),
        path('articles/create', CreateArticleAPIView.as_view(), name='articles-create-api'),
        path('articles/<int:id>/edit', GetUpdateDeleteArticleAPIView.as_view(), name='articles-edit-api'),
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ])),
    path('navigation/', include('izpitnik.navigation.urls')),
    path('dstyles/', include('izpitnik.styling.urls')),
    path('auth/', include('izpitnik.accounts.urls')),
    path('orth_calendar/', include('izpitnik.orth_calendar.urls')),
    # Optional UI:
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('articles/', include('izpitnik.articles.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
